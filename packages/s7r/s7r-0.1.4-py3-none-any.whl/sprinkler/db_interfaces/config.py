import os
import sqlite3
from typing import List, Literal, Optional, Tuple, Union, overload

from ..db import db_execute, db_select, get_sprinkler_directory
from ..exceptions import InvalidConfigKey


class Config:
    db: sqlite3.Connection

    def __init__(self, db: sqlite3.Connection):
        self.db = db

    def set_value(self, key: str, value: str):
        if key not in _CONFIG_KEYS:
            raise InvalidConfigKey(key)
        db_execute(
            self.db,
            "INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)",
            (key, value),
        )

    @overload
    def get_value(self, key: Literal["GIT_BRANCH", "LOG_LOCATION"]) -> str:
        ...

    @overload
    def get_value(self, key: str) -> Union[str, None]:
        ...

    def get_value(self, key: str):
        key = key.upper()
        if key not in _CONFIG_KEYS:
            raise InvalidConfigKey(key)
        results = db_select(
            self.db, "select value from config where key = ? limit 1;", (key,)
        )
        if len(results) == 0:
            return _CONFIG_DEFAULT_VALUES.get(key)
        return str(results[0][0])

    def ls(self) -> List[Tuple[str, Optional[str]]]:
        return [(key, self.get_value(key)) for key in _CONFIG_KEYS]

    def delete_value(self, key: str):
        key = key.upper()
        if key not in _CONFIG_KEYS:
            raise InvalidConfigKey(key)
        db_execute(self.db, "delete from config where key = ?;", (key,))


_CONFIG_LOG_LOCATION = "LOG_LOCATION"
_CONFIG_TARGETS_DIRECTORY = "TARGETS_DIRECTORY"
_CONFIG_GIT_BRANCH = "GIT_BRANCH"
_CONFIG_FAILURE_TASK_TARGET = "FAILURE_TASK_TARGET"
_CONFIG_FAILURE_TASK = "FAILURE_TASK"
_CONFIG_SSH_KEY = "SSH_KEY"

_CONFIG_KEYS = {
    _CONFIG_LOG_LOCATION,
    _CONFIG_TARGETS_DIRECTORY,
    _CONFIG_GIT_BRANCH,
    _CONFIG_FAILURE_TASK_TARGET,
    _CONFIG_FAILURE_TASK,
    _CONFIG_SSH_KEY,
}

_CONFIG_DEFAULT_VALUES = {
    _CONFIG_LOG_LOCATION: os.path.join(get_sprinkler_directory(), "logs"),
    _CONFIG_GIT_BRANCH: "main",
}
