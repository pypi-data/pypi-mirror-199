import os
from typing import Optional

from ..constants import _TASK_TYPE_FIRE_AND_FORGET, RUNTIME_TYPE, TASK_TYPE
from ..exceptions import TaskCreationException
from ..utils import make_target_image_name
from .sprinkler_config import (
    InvalidSprinklerConfigException,
    SprinklerFailureTask,
    load_target,
)


class Task:
    target: str
    task: str
    timeout: Optional[int]
    entrypoint_file: str
    image: str
    task_type: TASK_TYPE
    runtime: RUNTIME_TYPE
    version: str
    failure_task: Optional[SprinklerFailureTask] = None

    def __init__(
        self,
        target: str,
        task: str,
        timeout: Optional[int],
        entrypoint_file: str,
        image: str,
        runtime: RUNTIME_TYPE,
        version: str,
        task_type: TASK_TYPE = _TASK_TYPE_FIRE_AND_FORGET,
        failure_task: Optional[SprinklerFailureTask] = None,
    ):
        self.target = target
        self.task = task
        self.timeout = timeout
        self.entrypoint_file = entrypoint_file
        self.image = image
        self.task_type = task_type
        self.runtime = runtime
        self.version = version
        self.failure_task = failure_task


def get_task(targets_dir: Optional[str], target: str, task: str) -> Task:
    if targets_dir is None:
        raise TaskCreationException("TARGETS DIRECTORY is not set")

    try:
        config = load_target(targets_dir, target)

    except InvalidSprinklerConfigException as e:
        raise TaskCreationException(e)

    task_config_list = [t for t in config.tasks if t.task == task]
    if len(task_config_list) == 0:
        raise TaskCreationException(
            f"Failed to find a task with the name {task} in the target {target}"
        )
    if len(task_config_list) > 1:
        raise InvalidSprinklerConfigException(
            f"Found multiple tasks with the name {task} in the target {target}"
        )
    task_config = task_config_list[0]

    failure_task = None
    if config.failure_task is not None:
        failure_task = config.failure_task
    if task_config.failure_task is not None:
        failure_task = task_config.failure_task

    return Task(
        target=target,
        task=task,
        timeout=task_config.timeout,
        entrypoint_file=task_config.entrypoint,
        task_type=task_config.type,
        runtime=config.runtime,
        version=config.version,
        image=make_target_image_name(target),
        failure_task=failure_task,
    )
