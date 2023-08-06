import json
import logging
import os
import shutil
from uuid import uuid4

import docker
import redis
import smart_open
from flask import Flask, jsonify, request, send_from_directory, session
from flask_cors import CORS

from sprinkler import __version__

from .constants import (
    _EXECUTE_TASK_INSTANCE_CHANNEL,
    _SPRINKLER_SECRET_KEY_ENVIRONMENT_VARIABLE,
    _TASK_INSTANCE_STATUS_RUNNING,
    _TASK_INSTANCE_STATUS_WAITING,
    _TASK_TYPE_CALL_AND_RESPONSE,
    _TRIGGER_TYPE_WEBHOOK,
    _WEBSERVER_LOGGER,
)
from .db import get_db
from .db_interfaces import (
    _CONFIG_GIT_BRANCH,
    _CONFIG_TARGETS_DIRECTORY,
    APIKeys,
    Config,
    Images,
    Secrets,
    TaskInstances,
    Users,
)
from .exceptions import (
    BuildLogNotFoundException,
    GitException,
    InvalidConfigKey,
    InvalidSecretName,
    InvalidSprinklerConfigException,
    TargetBuildException,
    TargetsDirectoryUnsetException,
    TaskInstanceDoesNotExistException,
)
from .git import Git
from .targets import load_target, load_targets
from .utils import get_sprinkler_directory

logger = logging.getLogger(_WEBSERVER_LOGGER)
app = Flask(__name__)
app.config["development"] = False
CORS(app)
app.secret_key = os.environ.get(_SPRINKLER_SECRET_KEY_ENVIRONMENT_VARIABLE, "sprinkler")


_WHITELISTED_PATHS = {"/login", "/access_check"}


@app.before_request
def before_requests():
    if app.config["development"]:
        return
    if request.path[-1:] == "/":
        return
    if request.path in _WHITELISTED_PATHS:
        return
    if request.path[:8] == "/assets/":
        return

    user = session.get("user")
    if user is not None:
        return

    api_key = request.headers.get("x-api-key")
    if api_key is None:
        return "Access Denied", 403

    db = get_db()
    api_keys = APIKeys(db)
    is_valid = api_keys.verify_api_key(api_key)
    db.close()
    if is_valid:
        return
    return "Access Denied", 403


@app.get("/access_check")
def access_check():
    if app.config["development"]:
        return jsonify({"is_authorized": True, "type": "user", "user_name": "JOHN_DOE"})
    user = session.get("user")
    if user is not None:
        return jsonify({"is_authorized": True, "type": "user", "user_name": user})
    api_key = request.headers.get("x-api-key")
    if api_key is not None:
        db = get_db()
        api_keys = APIKeys(db)
        is_valid_api_key = api_keys.verify_api_key(api_key)
        db.close()
        if is_valid_api_key:
            return jsonify({"is_authorized": True, "type": "api_key"})

    return jsonify({"is_authorized": False})


@app.post("/login")
def login():
    body = request.get_json(force=True)
    if "user_name" not in body or "password" not in body:
        return jsonify({"success": False})

    db = get_db()
    users = Users(db)
    valid_user = users.verify_user_password(body["user_name"], body["password"])
    db.close()

    if valid_user:
        session["user"] = body["user_name"]
        return jsonify({"success": True})
    return jsonify({"success": False})


@app.get("/assets/<path:path>")
def assets(path: str):
    build_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), ".build", "assets"
    )
    return send_from_directory(build_path, path)


@app.get("/")
@app.get("/<path:path>/")
def index(path: str = ""):
    build_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        ".build",
    )
    return send_from_directory(build_path, "index.html")


@app.post("/target/<string:target>/task/<string:task>/trigger")
def trigger_target_job(target: str, task: str):
    body = request.get_data(as_text=True)
    redis_client = redis.Redis()
    response_channel = f"sprinkler-response-channel:{uuid4().hex}"
    with redis_client.pubsub(ignore_subscribe_messages=True) as pub_sub:
        pub_sub.subscribe(response_channel)
        subscribers = redis_client.publish(
            _EXECUTE_TASK_INSTANCE_CHANNEL,
            json.dumps(
                {
                    "target": target,
                    "task": task,
                    "trigger_type": _TRIGGER_TYPE_WEBHOOK,
                    "response_channel": response_channel,
                    "body": json.dumps(body),
                }
            ),
        )
        if subscribers == 0:
            return (
                jsonify(
                    "Nothing was listening. Are you sure sprinkler task-manager was listening?"
                ),
                500,
            )
        for message in pub_sub.listen():
            message_data = json.loads(message["data"].decode())
            if message_data.get("type") == "receipt":
                if message_data.get("success") is not True:
                    return jsonify(message_data.get("message")), 404
                if message_data.get("job_type") == _TASK_TYPE_CALL_AND_RESPONSE:
                    continue
                return jsonify(f"Started {message_data.get('message')} successfully")

            if message_data.get("type") == "response":
                return message_data.get("message"), 200
            return jsonify("Did not get a valid response from the task manager."), 500
    return jsonify("Internal Service Error"), 500


@app.get("/config")
def get_config():
    db = get_db()
    c = Config(db)
    configuration = {key: value if value else "" for key, value in c.ls()}
    db.close()
    return jsonify(configuration)


@app.post("/config/<string:key>")
def set_config(key: str):
    value = request.get_data(as_text=True)
    db = get_db()
    c = Config(db)
    try:
        c.set_value(key, value)
    except InvalidConfigKey:
        db.close()
        return f"Invalid config key {key}", 428
    db.close()
    return get_config()


@app.delete("/config/<string:key>")
def delete_config(key: str):
    db = get_db()
    c = Config(db)
    try:
        c.delete_value(key)
    except InvalidConfigKey:
        db.close()
        return f"Invalid config key {key}", 428
    db.close()
    return get_config()


@app.get("/secrets")
def get_secrets():
    db = get_db()
    s = Secrets(db)
    secrets = s.get_secret_keys()
    db.close()
    return jsonify(secrets)


@app.post("/secrets/<string:key>")
def set_secret(key):
    value = request.get_data(as_text=True)
    db = get_db()
    s = Secrets(db)
    try:
        s.set_secret(key, value)
    except InvalidSecretName as e:
        return jsonify(f"The key was invalid: {str(key)}"), 428
    db.close()
    return get_secrets()


@app.delete("/secrets/<string:key>")
def delete_secret(key):
    db = get_db()
    s = Secrets(db)
    s.delete_secret(key)
    db.close()
    return get_secrets()


@app.get("/targets")
def get_targets():
    targets_dir = Config(get_db()).get_value(_CONFIG_TARGETS_DIRECTORY)
    if targets_dir is None:
        return jsonify([])
    targets = []
    for target, config in load_targets(targets_dir=targets_dir, include_errors=True):
        if isinstance(config, str):
            targets.append({"target": target, "error": config})
            continue
        targets.append({"target": target, "error": None})
    return jsonify(targets)


@app.get("/targets/<string:target>")
def get_target_detail(target: str):
    targets_dir = Config(get_db()).get_value(_CONFIG_TARGETS_DIRECTORY)
    if targets_dir is None:
        return jsonify(f"{_CONFIG_TARGETS_DIRECTORY} is unset."), 500
    try:
        config = load_target(targets_dir, target)
    except InvalidSprinklerConfigException as e:
        return jsonify({"error": str(e)})

    return jsonify(config.dict())


@app.post("/targets/<string:target>/build")
def build_target(target: str):
    db = get_db()
    targets_dir = Config(db).get_value(_CONFIG_TARGETS_DIRECTORY)
    if targets_dir is None:
        return jsonify(f"{_CONFIG_TARGETS_DIRECTORY} is unset."), 500

    try:
        config = load_target(targets_dir, target)
    except InvalidSprinklerConfigException as e:
        return jsonify(f"{target} is invalid: {e}"), 500
    images = Images(db, docker.from_env())
    try:
        images.build_target_image(
            targets_dir=targets_dir,
            target=target,
            runtime=config.runtime,
            version=config.version,
            os_tag=config.os,
        )
    except TargetBuildException as e:
        return jsonify({"success": False, "logs": str(e)})
    finally:
        db.close()
    return jsonify({"success": True})


@app.get("/targets/<string:target>/build-logs")
def build_logs_target(target: str):
    db = get_db()
    images = Images(db, None)
    try:
        success, build_logs = images.get_target_build_logs(target)
    except BuildLogNotFoundException:
        return jsonify({"logs": None})

    return jsonify({"build_success": success, "logs": build_logs})


@app.get("/task_instance")
def get_task_instances():
    db = get_db()
    task_instances = TaskInstances(db)
    results = task_instances.get_task_instances(
        limit=request.args.get("limit", 100, type=int),
        offset=request.args.get("offset", 0, type=int),
        sort_by=request.args.get("sort_by", "created_at_time"),
        sort_ascending="sort_ascending" in request.args,
        target=request.args.getlist("target"),
        task=request.args.getlist("task"),
        status=request.args.getlist("status"),  # type: ignore
        trigger_type=request.args.getlist("trigger_type"),  # type: ignore
        runtime=request.args.getlist("runtime"),  # type: ignore
        version=request.args.getlist("version"),
        git_hash=request.args.getlist("git_hash"),
        created_at_time_start=request.args.get("created_at_time_start", type=float),
        created_at_time_end=request.args.get("created_at_time_end", type=float),
        start_time_start=request.args.get("start_time_start", type=float),
        start_time_end=request.args.get("start_time_end", type=float),
        end_time_start=request.args.get("end_time_start", type=float),
        end_time_end=request.args.get("end_time_end", type=float),
    )
    db.close()
    return jsonify([result.dict() for result in results])


@app.get("/task_instance/<string:task_instance_id>")
def get_task_instance(task_instance_id: str):
    db = get_db()
    task_instances = TaskInstances(db)
    try:
        task_instance = task_instances.get_task_instance(task_instance_id)
    except TaskInstanceDoesNotExistException:
        return jsonify(f"task instance {task_instance_id} not found"), 404
    return jsonify(task_instance.dict())


@app.get("/task_instance/<string:task_instance_id>/logs")
def get_task_instance_logs(task_instance_id: str):
    db = get_db()
    task_instances = TaskInstances(db)
    try:
        task_instance = task_instances.get_task_instance(task_instance_id)
    except TaskInstanceDoesNotExistException:
        return jsonify(f"task instance {task_instance_id} not found"), 404

    db.close()
    if task_instance.status == _TASK_INSTANCE_STATUS_WAITING:
        return jsonify("")
    if (
        task_instance.status == _TASK_INSTANCE_STATUS_RUNNING
        and task_instance.container_id is not None
    ):
        docker_client = docker.from_env()
        try:
            container = docker_client.containers.get(task_instance.container_id)
            return jsonify(container.logs().decode())
        except docker.errors.NotFound:
            return jsonify(f"Container {task_instance.container_id} not found."), 404
    elif task_instance.log_location is not None:
        with smart_open.open(task_instance.log_location, "r") as f:
            return jsonify(f.read())
    return jsonify("No Logs Found."), 500


@app.get("/version")
def version():
    return jsonify(__version__)


@app.get("/git/hash")
def get_git_hash():
    db = get_db()
    git = Git(db)
    try:
        git_hash = git.get_git_hash()
    except GitException as e:
        return jsonify(f"GIT exception: {e}"), 500
    except TargetsDirectoryUnsetException:
        return jsonify(f"{_CONFIG_TARGETS_DIRECTORY} is unset."), 500
    db.close()
    return jsonify(git_hash)


@app.post("/git/pull")
def git_pull():
    db = get_db()
    git = Git(db)
    try:
        git.pull()
        git_hash = git.get_current_branch()
    except GitException as e:
        return jsonify(f"GIT exception: {e}"), 500
    except TargetsDirectoryUnsetException:
        return jsonify(f"{_CONFIG_TARGETS_DIRECTORY} is unset."), 500
    db.close()
    return jsonify(git_hash)


@app.post("/git/checkout")
def git_checkout():
    branch = request.get_data(as_text=True)
    db = get_db()
    git = Git(db)
    config = Config(db)
    config.set_value(_CONFIG_GIT_BRANCH, branch)
    try:
        git.pull()
        git_hash = git.get_current_branch()
    except GitException as e:
        return jsonify(f"GIT exception: {e}"), 500
    except TargetsDirectoryUnsetException:
        return jsonify(f"{_CONFIG_TARGETS_DIRECTORY} is unset."), 500
    db.close()
    return jsonify(git_hash)


@app.post("/git/generate_key")
def git_generate_key():
    force = "force" in request.args
    db = get_db()
    git = Git(db)
    try:
        public_key = git.generate_key(force=force)
    except GitException as e:
        return jsonify(f"GIT exception: {e}"), 500
    return jsonify(public_key)


@app.get("/git/get_key")
def git_get_key():
    db = get_db()
    git = Git(db)
    try:
        public_key = git.get_key()
    except GitException as e:
        return jsonify(f"GIT exception: {e}"), 500
    return jsonify(public_key)


@app.post("/git/init")
def git_init():
    data = request.get_json(force=True)
    directory = data.get("directory", get_sprinkler_directory())
    git_remote = data.get("git_remote")
    if git_remote is None:
        return jsonify("Must specify git_remote."), 500
    branch = data.get("branch")
    force = data.get("force")

    if not os.path.exists(directory):
        return jsonify(f"{directory} does not exist."), 404
    if not os.path.isdir(directory):
        return jsonify(f"{directory} is not a directory."), 404
    d = git_remote.split("/")[-1].replace(".git", "")
    targets_dir = os.path.join(directory, d)

    db = get_db()
    git = Git(db)
    config = Config(db)
    logs = ""
    try:
        if os.path.exists(targets_dir):
            if force:
                logger.warning(f"Deleting {targets_dir}")
                shutil.rmtree(targets_dir)
            else:
                return jsonify(
                    f"{targets_dir} already exists. Specify force=True to remove it.",
                )

        if branch is not None:
            config.set_value(_CONFIG_GIT_BRANCH, branch)
        logs += git.clone(directory, git_remote) + "\n"
        config.set_value(_CONFIG_TARGETS_DIRECTORY, targets_dir)
        logs += git.pull()
    except GitException as e:
        return jsonify(logs + "\n" + str(e)), 500
    return jsonify(logs)


@app.get("/api_keys")
def get_api_keys():
    db = get_db()
    api_keys = APIKeys(db)
    keys = api_keys.get_api_keys()
    db.close()
    return jsonify(keys)


@app.post("/api_keys/<string:key>")
def create_api_keys(key: str):
    db = get_db()
    api_keys = APIKeys(db)
    api_key = api_keys.create_api_key(key)
    db.close()
    return jsonify(api_key)


@app.delete("/api_keys/<string:key>")
def delete_api_key(key: str):
    db = get_db()
    api_keys = APIKeys(db)
    api_key = api_keys.delete_api_key(key)
    db.close()
    return jsonify(api_key)


### LAUNCHING GUNICORN SERER STUFF ##############
from gunicorn.app.base import BaseApplication


class StandaloneApplication(BaseApplication):
    def __init__(self, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def init(self, parser, opts, args):
        pass

    def load_config(self):
        for key, value in self.options.items():
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key.lower(), value)

    def load(self):
        return self.application
