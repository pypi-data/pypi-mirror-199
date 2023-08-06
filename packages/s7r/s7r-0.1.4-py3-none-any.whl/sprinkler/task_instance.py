import asyncio
import json
import logging
import os
import re
import sqlite3
from typing import Optional
from uuid import uuid4

import docker.errors
import redis.asyncio as redis
import smart_open
from docker import DockerClient
from docker.models.containers import Container

from .constants import (
    _EXECUTE_TASK_INSTANCE_CHANNEL,
    _SPRINKLER_BODY_ENV_VAR,
    _TASK_EXECUTE_LOOP_DELAY_FAST,
    _TASK_EXECUTE_LOOP_DELAY_SLOW,
    _TASK_INSTANCE_LOGGER,
    _TASK_INSTANCE_STATUS_COMPLETE,
    _TASK_INSTANCE_STATUS_ERROR,
    _TASK_INSTANCE_STATUS_RUNNING,
    _TASK_INSTANCE_STATUS_TIMEOUT,
    _TASK_INSTANCE_STATUS_WAITING,
    _TASK_TYPE_CALL_AND_RESPONSE,
    _TRIGGER_TYPE_WEBHOOK,
    TASK_INSTANCE_STATUS_TYPE,
    TRIGGER_TYPE,
)
from .db_interfaces import (
    _CONFIG_FAILURE_TASK,
    _CONFIG_FAILURE_TASK_TARGET,
    _CONFIG_LOG_LOCATION,
    Config,
    Secrets,
    TaskInstanceModel,
    TaskInstances,
)
from .targets import SprinklerFailureTask, Task
from .utils import now

logger = logging.getLogger(_TASK_INSTANCE_LOGGER)


RESPONSE_REGEXP = re.compile(
    r"SPRINKLER\*_\*RESPONSE\*_\*START\*([\s\S]*)\*SPRINKLER\*_\*RESPONSE\*_\*END"
)


class TaskInstance:
    docker_client: DockerClient
    redis_client: redis.Redis
    db: sqlite3.Connection
    config: Config
    secrets: Secrets
    task_instances: TaskInstances
    id: str
    task: Task
    trigger_type: TRIGGER_TYPE
    git_hash: str
    status: TASK_INSTANCE_STATUS_TYPE
    is_failure_task: bool
    response_channel: str

    start_time: Optional[float]
    end_time: Optional[float]
    container: Optional[Container]

    def __init__(
        self,
        task: Task,
        trigger_type: TRIGGER_TYPE,
        git_hash: str,
        docker_client: DockerClient,
        redis_client: redis.Redis,
        db: sqlite3.Connection,
        response_channel: str,
        is_failure_task: bool = False,
        id: Optional[str] = None,
    ):
        self.docker_client = docker_client
        self.redis_client = redis_client
        self.task = task
        self.trigger_type = trigger_type
        self.git_hash = git_hash
        if id is None:
            self.id = TaskInstance._make_task_task_instance_id(
                job=task, trigger_type=trigger_type, git_hash=git_hash
            )
        else:
            self.id = id
        self.response_channel = response_channel
        self.status = _TASK_INSTANCE_STATUS_WAITING
        self.container = None
        self.start_time = None
        self.end_time = None
        self.db = db
        self.is_failure_task = is_failure_task
        self.config = Config(self.db)
        self.secrets = Secrets(self.db)
        self.task_instances = TaskInstances(self.db)

    def store_logs(self, logs: str):
        log_location = self.config.get_value(_CONFIG_LOG_LOCATION)
        log_path = os.path.join(log_location, f"{self.id}.log")
        with smart_open.open(log_path, "w") as log_file:
            log_file.write(logs)
        self.task_instances.update_task_instance(self.id, log_location=log_path)

    def _start_execution(
        self,
        body: str = "",
    ):
        self.task_instances.insert_task_instance(
            self.id,
            self.task,
            self.status,
            self.trigger_type,
            self.git_hash,
            self.response_channel,
            self.is_failure_task,
        )
        logger.info(f"{self.id} | STARTED")
        env = self.secrets.get_secrets_for_execution()
        env[_SPRINKLER_BODY_ENV_VAR] = body
        container = self.docker_client.containers.run(
            self.task.image,
            self.task.entrypoint_file,
            detach=True,
            environment=env,
        )
        if not isinstance(container, Container):
            raise Exception(
                "Starting the docker container did not return a Container object."
            )
        self.container = container
        self.status = _TASK_INSTANCE_STATUS_RUNNING
        self.start_time = now()
        self.task_instances.update_task_instance(
            self.id,
            start_time=self.start_time,
            container_id=self.container.id,
            status=self.status,
        )

    async def _revive(self, task_instance: TaskInstanceModel):
        self.start_time = task_instance.start_time
        self.status = task_instance.status
        self.id = task_instance.id
        if task_instance.container_id is not None:
            try:
                self.container = self.docker_client.containers.get(
                    task_instance.container_id
                )
            except docker.errors.NotFound:
                logger.info(f"{self.id} | REVIVED-DEAD")
                self.end_time = now()
                self.status = _TASK_INSTANCE_STATUS_ERROR
                self.task_instances.update_task_instance(
                    self.id, end_time=self.end_time, status=self.status
                )
                return
        logger.info(f"{self.id} | REVIVED")
        await self._execution_loop()
        await self._after_execution()

    async def _execution_loop(self):
        if self.container is None:
            logger.info(f"{self.id} | CONTAINER ERROR")
            self.status = _TASK_INSTANCE_STATUS_ERROR
            raise Exception("Container object doesn't exist.")
        delay = (
            _TASK_EXECUTE_LOOP_DELAY_FAST
            if self.task.task_type == _TASK_TYPE_CALL_AND_RESPONSE
            else _TASK_EXECUTE_LOOP_DELAY_SLOW
        )

        while True:
            self.container.reload()
            if self.container.status == "exited":
                if self.container.attrs["State"]["ExitCode"] == 0:
                    logger.info(f"{self.id} | COMPLETE")
                    self.status = _TASK_INSTANCE_STATUS_COMPLETE
                    break
                else:
                    logger.info(f"{self.id} | ERROR")
                    self.status = _TASK_INSTANCE_STATUS_ERROR
                    break
            if (
                self.task.timeout is not None
                and self.start_time is not None
                and now() - self.start_time > self.task.timeout
            ):
                logger.info(f"{self.id} | TIMEOUT")
                self.container.kill()
                self.status = _TASK_INSTANCE_STATUS_TIMEOUT
                break
            await asyncio.sleep(delay)

    async def _after_execution(self):
        if self.container is None:
            raise Exception("Container object doesn't exist.")
        self.end_time = now()
        self.task_instances.update_task_instance(
            self.id, end_time=self.end_time, status=self.status
        )
        task_logs = self.container.logs().decode()
        self.container.remove()
        if self.task.task_type == _TASK_TYPE_CALL_AND_RESPONSE:
            response = ""
            response_match = RESPONSE_REGEXP.search(task_logs)
            if response_match is not None:
                response = response_match.group(1)
            await self.redis_client.publish(
                self.response_channel,
                json.dumps({"type": "response", "message": response}),
            )
        if (
            self.status in {_TASK_INSTANCE_STATUS_ERROR, _TASK_INSTANCE_STATUS_TIMEOUT}
            and not self.is_failure_task
        ):
            if self.task.failure_task is not None:
                await self.trigger_failure_task(self.task.failure_task, task_logs)
            else:
                failure_target = self.config.get_value(_CONFIG_FAILURE_TASK_TARGET)
                failure_task = self.config.get_value(_CONFIG_FAILURE_TASK)
                if failure_target is not None and failure_task is not None:
                    await self.trigger_failure_task(
                        SprinklerFailureTask(task=failure_task, target=failure_target),
                        task_logs,
                    )

        self.store_logs(task_logs)

    async def trigger_failure_task(self, failure_task: SprinklerFailureTask, logs: str):
        failure_body = {
            "target": self.task.target,
            "task": self.task.task,
            "id": self.id,
            "runtime": self.task.runtime,
            "version": self.task.version,
            "entrypoint": self.task.entrypoint_file,
            "status": self.status,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "git_hash": self.git_hash,
            "logs": logs,
        }
        await self.redis_client.publish(
            _EXECUTE_TASK_INSTANCE_CHANNEL,
            json.dumps(
                {
                    "target": failure_task.target,
                    "task": failure_task.task,
                    "is_failure_task": True,
                    "trigger_type": _TRIGGER_TYPE_WEBHOOK,
                    "response_channel": "none",
                    "body": json.dumps(failure_body),
                }
            ),
        )

    async def execute(
        self,
        body: str = "",
    ):
        self._start_execution(body=body)
        await self._execution_loop()
        await self._after_execution()

    @staticmethod
    def _make_task_task_instance_id(
        job: Task, trigger_type: TRIGGER_TYPE, git_hash: str
    ):
        return f"{job.target}__{job.task}__{trigger_type}__{round(now())}__{git_hash[:12]}__{uuid4().hex[:12]}"
