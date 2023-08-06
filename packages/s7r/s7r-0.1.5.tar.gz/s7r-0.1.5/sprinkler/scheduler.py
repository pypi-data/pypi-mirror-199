import asyncio
import json
import logging
import sqlite3
from multiprocessing import Process
from typing import Dict, List, Optional, Tuple

import docker
import redis.asyncio as redis
from croniter import croniter

from .constants import (
    _EXECUTE_TASK_INSTANCE_CHANNEL,
    _SCHEDULER_LOGGER,
    _TRIGGER_TYPE_SCHEDULED,
)
from .db import get_db
from .db_interfaces import _CONFIG_TARGETS_DIRECTORY, Config, Images, TaskInstances
from .exceptions import GitException, TargetsDirectoryUnsetException
from .git import Git
from .targets import SprinklerConfig, load_targets
from .utils import now

logger = logging.getLogger(_SCHEDULER_LOGGER)

_SCHEDULER_EXECUTE_LOOP_DELAY = 1
_SCHEDULER_ERROR_LOOP_DELAY = 5

_GIT_PULL_INTERVAL = 30 * 60  # 30 minutes in seconds


class Scheduler:
    redis_client: redis.Redis
    db: sqlite3.Connection
    git: Git
    config: Config
    task_instances: TaskInstances
    images: Images
    targets: List[Tuple[str, SprinklerConfig]]
    build_queue: List[Process]

    last_git_pull: float = 0
    current_git_hash: Optional[str] = None
    recently_started_tasks: Dict[str, float]  # target_task: expiration

    def __init__(self):
        self.redis_client = redis.Redis()
        self.db = get_db()
        self.config = Config(self.db)
        self.git = Git(self.db)
        self.task_instances = TaskInstances(self.db)
        self.images = Images(self.db, docker.from_env())
        self.targets = []
        self.build_queue = []
        self.recently_started_tasks = {}

    async def execute(self):
        self._startup()
        await asyncio.gather(self._queue_loop(), self._execution_loop())

    def _startup(self):
        targets_dir = self.config.get_value(_CONFIG_TARGETS_DIRECTORY)
        if targets_dir is None:
            return
        self.images.build_target_images(targets_dir=targets_dir)
        self.targets = load_targets(targets_dir, include_errors=False)
        self.git_hash = self.git.get_git_hash()
        self.last_git_pull = now()

    async def _queue_loop(self):
        while True:
            await asyncio.sleep(_SCHEDULER_EXECUTE_LOOP_DELAY)
            if len(self.build_queue) == 0:
                continue
            current_process = self.build_queue[0]
            if current_process.pid is None:
                current_process.start()
                continue
            if current_process.is_alive():
                continue
            self.build_queue.pop(0)

    async def _execution_loop(self):
        while True:
            targets_dir = self.config.get_value(_CONFIG_TARGETS_DIRECTORY)
            if targets_dir is None:
                logger.error("TARGETS_DIRECTORY is unset.")
                await asyncio.sleep(_SCHEDULER_ERROR_LOOP_DELAY)
                continue
            if now() - self.last_git_pull > _GIT_PULL_INTERVAL:
                logger.warning("Pulling from remote.")
                try:
                    self.git.pull()
                    self.last_git_pull = now()
                except GitException as e:
                    logger.error(e)
            try:
                git_hash = self.git.get_git_hash()
            except GitException as e:
                logger.error(e)
                await asyncio.sleep(_SCHEDULER_ERROR_LOOP_DELAY)
                continue
            except TargetsDirectoryUnsetException:
                logger.error("TARGETS_DIRECTORY is unset.")
                await asyncio.sleep(_SCHEDULER_ERROR_LOOP_DELAY)
                continue

            if git_hash != self.current_git_hash:
                self.current_git_hash = git_hash
                self.build_queue.append(
                    Process(
                        target=self.images.build_target_images,
                        args=(targets_dir,),
                        daemon=True,
                    )
                )
                self.targets = load_targets(targets_dir, include_errors=False)

            current_time = now()

            cleanup = set()
            for target_task, expiration in self.recently_started_tasks.items():
                if current_time >= expiration:
                    cleanup.add(target_task)
            for target_task in cleanup:
                del self.recently_started_tasks[target_task]

            minute_start_boundary = int(current_time // 60 * 60)
            minute_end_boundary = minute_start_boundary + 60
            for target, config in self.targets:
                for task_config in config.tasks:
                    if task_config.schedule is None:
                        continue
                    if not croniter.match(task_config.schedule, current_time):
                        continue

                    if f"{target}__{task_config.task}" in self.recently_started_tasks:
                        continue

                    existing_task_instances = self.task_instances.get_task_instances(
                        target=[target],
                        task=[task_config.task],
                        trigger_type=[_TRIGGER_TYPE_SCHEDULED],
                        created_at_time_start=minute_start_boundary,
                        created_at_time_end=minute_end_boundary,
                    )
                    if len(existing_task_instances) > 0:
                        continue
                    logger.info(f"Triggering {target} {task_config.task}")
                    self.recently_started_tasks[
                        f"{target}__{task_config.task}"
                    ] = minute_end_boundary

                    asyncio.create_task(
                        self.redis_client.publish(
                            _EXECUTE_TASK_INSTANCE_CHANNEL,
                            json.dumps(
                                {
                                    "target": target,
                                    "task": task_config.task,
                                    "trigger_type": _TRIGGER_TYPE_SCHEDULED,
                                    "response_channel": "null",
                                }
                            ),
                        )
                    )
            await asyncio.sleep(_SCHEDULER_EXECUTE_LOOP_DELAY)
