import asyncio
import json
import logging
import sqlite3
from typing import Dict, Optional, Union

import docker
import redis.asyncio as redis

from .constants import (
    _EXECUTE_TASK_INSTANCE_CHANNEL,
    _TASK_INSTANCE_STATUS_RUNNING,
    _TASK_MANAGER_LOGGER,
    TASK_TYPE,
)
from .db import get_db
from .db_interfaces import _CONFIG_TARGETS_DIRECTORY, Config, TaskInstances
from .git import Git
from .targets import Task, get_task
from .task_instance import TRIGGER_TYPE, TaskInstance

logger = logging.getLogger(_TASK_MANAGER_LOGGER)


class TaskManager:
    docker_client: docker.DockerClient
    redis_client: redis.Redis
    db: sqlite3.Connection
    config: Config
    git: Git
    tasks: Dict[str, TaskInstance]

    def __init__(self):
        self.docker_client = docker.from_env()
        self.redis_client = redis.Redis()
        self.db = get_db()
        self.config = Config(self.db)
        self.git = Git(self.db)

    async def _revive(self):
        task_instances = TaskInstances(self.db)
        orphan_task_instances = task_instances.get_task_instances(
            limit=10_000_000, status=[_TASK_INSTANCE_STATUS_RUNNING]
        )
        for orphan in orphan_task_instances:
            task_instance = self._create_task_instance(
                orphan.target,
                orphan.task,
                orphan.trigger_type,
                orphan.response_channel,
                is_failure_task=orphan.is_failure_task,
            )

            asyncio.create_task(task_instance._revive(orphan))

    async def execute(self):
        await self._revive()
        async with self.redis_client.pubsub() as pub_sub:
            await pub_sub.subscribe(_EXECUTE_TASK_INSTANCE_CHANNEL)
            logger.info(f"Subscribed to {_EXECUTE_TASK_INSTANCE_CHANNEL}")
            while True:
                message = await pub_sub.get_message(ignore_subscribe_messages=True)
                if message is None:
                    await asyncio.sleep(0.01)
                    continue
                decoded_message = message["data"].decode()
                try:
                    message_data = json.loads(decoded_message)
                except json.JSONDecodeError:
                    logger.error(
                        f"Failed to parse subscription message: '{decoded_message}'"
                    )
                    continue
                if "response_channel" not in message_data:
                    logger.error("No response channel given in the message.")
                try:
                    task_instance = self._create_task_instance(
                        message_data["target"],
                        message_data["task"],
                        message_data["trigger_type"],
                        message_data["response_channel"],
                        message_data.get("is_failure_task", False),
                    )
                except Exception as e:
                    logger.error(f"Failed to create task instance: {e}")
                    await self.send_trigger_response(
                        message_data["response_channel"],
                        False,
                        message=f"Failed to create task instance: {e}",
                    )
                    continue
                asyncio.create_task(
                    task_instance.execute(
                        body=message_data.get("body", ""),
                    )
                )
                await self.send_trigger_response(
                    message_data["response_channel"],
                    True,
                    job_type=task_instance.task.task_type,
                    message=task_instance.id,
                )

    async def send_trigger_response(
        self,
        response_channel: str,
        success: bool,
        job_type: Optional[TASK_TYPE] = None,
        message: Optional[str] = None,
    ):
        response_message: Dict[str, Union[str, bool]] = {
            "success": success,
            "type": "receipt",
        }
        if message is not None:
            response_message["message"] = message
        if job_type is not None:
            response_message["job_type"] = job_type

        await self.redis_client.publish(response_channel, json.dumps(response_message))

    def _create_task_instance(
        self,
        target: str,
        task: str,
        trigger_type: TRIGGER_TYPE,
        response_channel: str,
        is_failure_task: bool,
    ):
        _task = get_task(self.config.get_value(_CONFIG_TARGETS_DIRECTORY), target, task)
        git_hash = self.git.get_git_hash()
        return TaskInstance(
            task=_task,
            trigger_type=trigger_type,
            docker_client=self.docker_client,
            db=self.db,
            redis_client=self.redis_client,
            git_hash=git_hash,
            is_failure_task=is_failure_task,
            response_channel=response_channel,
        )
