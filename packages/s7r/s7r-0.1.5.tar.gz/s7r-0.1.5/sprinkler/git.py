import logging
import os
import sqlite3
import subprocess

from .constants import _GIT_LOGGER
from .db_interfaces import (
    _CONFIG_GIT_BRANCH,
    _CONFIG_SSH_KEY,
    _CONFIG_TARGETS_DIRECTORY,
    Config,
)
from .exceptions import GitException, TargetsDirectoryUnsetException
from .utils import get_sprinkler_directory

logger = logging.getLogger(_GIT_LOGGER)


class Git:
    db: sqlite3.Connection
    config: Config

    def __init__(self, db: sqlite3.Connection):
        self.db = db
        self.config = Config(self.db)

    def _get_targets_dir(self):
        targets_directory = self.config.get_value(_CONFIG_TARGETS_DIRECTORY)
        if targets_directory is None:
            raise TargetsDirectoryUnsetException()
        return targets_directory

    def _ensure_correct_branch(self) -> str:
        self.fetch()
        branch = self.config.get_value(_CONFIG_GIT_BRANCH)
        if self.get_current_branch() != branch:
            logger.info(f"Checking out {branch}.")
            self.checkout(branch)
        return branch

    def _ssh_key_override(self):
        ssh_key = self.config.get_value(_CONFIG_SSH_KEY)
        if ssh_key is None:
            return {}
        return {"GIT_SSH_COMMAND": f"ssh -i {ssh_key} -o IdentitiesOnly=yes"}

    def pull(self):
        branch = self._ensure_correct_branch()
        targets_directory = self._get_targets_dir()
        try:
            return subprocess.check_output(
                ["git", "pull", "origin", branch],
                text=True,
                cwd=targets_directory,
                env=self._ssh_key_override(),
                stderr=subprocess.STDOUT,
            )
        except subprocess.CalledProcessError as e:
            raise GitException(e)

    def get_git_hash(self):
        targets_directory = self._get_targets_dir()
        try:
            git_hash = subprocess.check_output(
                ["git", "rev-parse", "HEAD"], text=True, cwd=targets_directory
            )
        except subprocess.CalledProcessError as e:
            raise GitException(e)
        return git_hash

    def get_current_branch(self):
        targets_directory = self._get_targets_dir()
        try:
            return subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                text=True,
                cwd=targets_directory,
            ).strip()
        except subprocess.CalledProcessError as e:
            raise GitException(e)

    def checkout(self, branch: str):
        targets_directory = self._get_targets_dir()
        try:
            return subprocess.check_output(
                ["git", "checkout", branch],
                text=True,
                cwd=targets_directory,
                stderr=subprocess.STDOUT,
            )
        except subprocess.CalledProcessError as e:
            raise GitException(e)

    def fetch(self):
        targets_directory = self._get_targets_dir()
        try:
            return subprocess.check_output(
                ["git", "fetch"],
                text=True,
                cwd=targets_directory,
                env=self._ssh_key_override(),
                stderr=subprocess.STDOUT,
            )
        except subprocess.CalledProcessError as e:
            raise GitException(e)

    def clone(self, dir: str, repo: str):
        try:
            return subprocess.check_output(
                ["git", "clone", repo],
                text=True,
                cwd=dir,
                env=self._ssh_key_override(),
                stderr=subprocess.STDOUT,
            )
        except subprocess.CalledProcessError as e:
            raise GitException(e.output + "\n" + str(e))

    def generate_key(self, force: bool = False):
        sprinkler_dir = get_sprinkler_directory()
        private_key_path = os.path.join(sprinkler_dir, "sprinkler_key")
        public_key_path = os.path.join(sprinkler_dir, "sprinkler_key.pub")
        if (
            os.path.exists(private_key_path) or os.path.exists(public_key_path)
        ) and not force:
            raise GitException("sprinkler_key already exists.")
        if os.path.exists(private_key_path):
            os.remove(private_key_path)
        if os.path.exists(public_key_path):
            os.remove(public_key_path)
        try:
            subprocess.check_output(
                [
                    "ssh-keygen",
                    "-q",
                    "-f",
                    "sprinkler_key",
                    "-t",
                    "ed25519",
                    "-N",
                    "",
                ],
                text=True,
                cwd=sprinkler_dir,
            )
            self.config.set_value(_CONFIG_SSH_KEY, private_key_path)
            return self.get_key()
        except subprocess.CalledProcessError as e:
            raise GitException(e)

    def get_key(self):
        sprinkler_dir = get_sprinkler_directory()
        public_key_path = os.path.join(sprinkler_dir, "sprinkler_key.pub")
        if not os.path.exists(public_key_path):
            raise GitException("Key does not exist.")
        with open(public_key_path, "r") as f:
            return f.read().strip()
