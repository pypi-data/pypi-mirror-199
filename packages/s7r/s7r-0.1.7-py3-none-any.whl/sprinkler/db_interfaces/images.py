import logging
import os
import shutil
import sqlite3
from typing import List, Optional, Tuple
from uuid import uuid4

import docker
import docker.errors

from ..constants import _IMAGES_LOGGER, RUNTIME_TYPE
from ..db import db_execute, db_select
from ..exceptions import BuildLogNotFoundException, TargetBuildException
from ..targets.sprinkler_config import load_targets
from ..utils import make_target_image_name

logger = logging.getLogger(_IMAGES_LOGGER)


class Images:
    db: sqlite3.Connection
    docker_client: docker.DockerClient

    def __init__(self, db: sqlite3.Connection, docker_client: docker.DockerClient):
        self.db = db
        self.docker_client = docker_client

    def build_target_images(
        self,
        targets_dir: str,
    ):
        targets = load_targets(targets_dir, include_errors=False)
        for target, config in targets:
            self.build_target_image(
                targets_dir,
                target,
                config.runtime,
                config.version,
                config.os,
            )

    def build_target_image(
        self,
        targets_dir: str,
        target: str,
        runtime: RUNTIME_TYPE,
        version: str,
        os_tag: Optional[str] = None,
    ):
        tmp_dir = os.path.join("/tmp", uuid4().hex)
        logger.info(
            f"Building docker image for target {target} ({os.path.join(targets_dir, target)}) in temp dir ({tmp_dir})."
        )
        os.makedirs(tmp_dir, exist_ok=True)
        if not os.path.exists(os.path.join(targets_dir, target)):
            raise TargetBuildException(f"target {target} does not exist.")
        shutil.copytree(os.path.join(targets_dir, target), tmp_dir, dirs_exist_ok=True)
        with open(os.path.join(tmp_dir, "Dockerfile"), "w") as dockerfile:
            dockerfile.write(
                self._get_dockerfile(runtime=runtime, version=version, os_tag=os_tag)
            )
        try:
            _, logs_iter = self.docker_client.images.build(
                path=tmp_dir,
                tag=make_target_image_name(target),
            )
            logs = [l["stream"] for l in logs_iter if "stream" in l]
            self.set_target_build_logs(target, "".join(logs), True)
        except docker.errors.BuildError as e:
            logs = [l["stream"] for l in e.build_log if "stream" in l] + [str(e)]
            self.set_target_build_logs(target, "".join(logs), False)
            raise TargetBuildException("".join(logs))
        finally:
            shutil.rmtree(tmp_dir)

        logger.info(f"Completed building image for target {target}.")

    def get_target_build_logs(self, target: str) -> Tuple[bool, str]:
        results = db_select(
            self.db,
            "SELECT success, build_logs from target_build_logs where target = ?;",
            (target,),
        )
        if len(results) != 1:
            raise BuildLogNotFoundException()
        success, build_logs = results[0]
        return success, build_logs

    def set_target_build_logs(self, target: str, logs: str, success: bool):
        db_execute(
            self.db,
            "INSERT OR REPLACE INTO target_build_logs (target, build_logs, success) VALUES (?, ?, ?)",
            (target, logs, success),
        )

    def _get_dockerfile(
        self, runtime: RUNTIME_TYPE, version: str, os_tag: Optional[str] = None
    ):
        image = runtime if runtime not in ("node-npm", "node-yarn") else "node"
        tag = f"{version}{'' if os_tag is None else f'-{os_tag}'}"
        install = _RUNTIME_SPECIFIC_INSTALL[runtime]
        entrypoint = _RUNTIME_SPECIFIC_ENTRYPOINTS[runtime]
        return f"""
FROM {image}:{tag}

RUN groupadd -r sprinkler-user && useradd -m -r -g sprinkler-user sprinkler-user


WORKDIR /home/sprinkler-user/target
{install}

COPY . /home/sprinkler-user/target

USER sprinkler-user
ENTRYPOINT {entrypoint}
        """


_RUNTIME_SPECIFIC_ENTRYPOINTS = {
    "python": '[ "python3", "-u" ]',
    "node-npm": '[ "node" ]',
    "node-yarn": '[ "node" ]',
}

_RUNTIME_SPECIFIC_INSTALL = {
    "python": """
RUN pip install --no-cache-dir sprinkler_util==0.1.3
COPY requirements.txt /home/sprinkler-user/target/requirements.txt
RUN pip install --no-cache-dir -r /home/sprinkler-user/target/requirements.txt
    """.strip(),
    "node-yarn": """
COPY yarn.lock /home/sprinkler-user/target/yarn.lock
COPY package.json /home/sprinkler-user/target/package.json
RUN yarn install sprinkler_util@0.1.3
RUN yarn install
    """.strip(),
    "node-npm": """
COPY package-lock.json /home/sprinkler-user/target/package-lock.json
COPY package.json /home/sprinkler-user/target/package.json
RUN npm install sprinkler_util@0.1.3
RUN npm install
    """.strip(),
}
