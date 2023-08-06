import os
from typing import List, Literal, Optional, Tuple, Union, overload

from pydantic import BaseModel, ValidationError
from yaml import YAMLError, load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from ..constants import (
    _CONFIG_YAML_FILENAME,
    _TASK_TYPE_FIRE_AND_FORGET,
    RUNTIME_TYPE,
    TASK_TYPE,
)
from ..exceptions import InvalidSprinklerConfigException


class SprinklerFailureTask(BaseModel):
    target: str
    task: str


class SprinklerTaskConfig(BaseModel):
    task: str
    entrypoint: str
    schedule: Optional[str]
    timeout: Optional[int]
    type: TASK_TYPE = _TASK_TYPE_FIRE_AND_FORGET
    failure_task: Optional[SprinklerFailureTask] = None


class SprinklerConfig(BaseModel):
    tasks: List[SprinklerTaskConfig]
    runtime: RUNTIME_TYPE
    version: str
    failure_task: Optional[SprinklerFailureTask] = None
    os: Optional[str] = None


@overload
def load_targets(
    targets_dir: str, include_errors: Literal[False]
) -> List[Tuple[str, SprinklerConfig]]:
    ...


@overload
def load_targets(
    targets_dir: str, include_errors: Literal[True]
) -> List[Tuple[str, Union[SprinklerConfig, str]]]:
    ...


def load_targets(targets_dir: str, include_errors: bool = False):
    targets = []
    for target in os.listdir(targets_dir):
        if target == ".git":
            continue
        target_dir = os.path.join(targets_dir, target)
        if not os.path.isdir(target_dir):
            continue
        try:
            config = load_target(targets_dir, target)
        except InvalidSprinklerConfigException as e:
            if include_errors:
                targets.append((target, str(e)))
            continue
        targets.append((target, config))
    return targets


def load_target(targets_dir: str, target: str) -> SprinklerConfig:
    target_dir = os.path.join(targets_dir, target)
    if not os.path.isdir(target_dir):
        raise InvalidSprinklerConfigException("Target doesn't exist.")

    config_file = os.path.join(target_dir, _CONFIG_YAML_FILENAME)
    if not os.path.isfile(config_file):
        raise InvalidSprinklerConfigException(f"No {_CONFIG_YAML_FILENAME}")

    with open(config_file, "r") as f:
        try:
            config_yaml = load(f, Loader)
        except YAMLError:
            raise InvalidSprinklerConfigException("Invalid YAML")

    try:
        config = SprinklerConfig(**config_yaml)
    except ValidationError as e:
        raise InvalidSprinklerConfigException(f"YAML did not pass validation. {e}")
    return config
