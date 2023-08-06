import asyncio
import json
import logging
import os
import shutil
from typing import Optional
from uuid import uuid4

import click
import docker
import redis
import smart_open

from sprinkler import __version__

from .constants import (
    _EXECUTE_TASK_INSTANCE_CHANNEL,
    _TASK_INSTANCE_STATUS_COMPLETE,
    _TASK_INSTANCE_STATUS_ERROR,
    _TASK_INSTANCE_STATUS_RUNNING,
    _TASK_INSTANCE_STATUS_TIMEOUT,
    _TASK_INSTANCE_STATUS_WAITING,
    _TASK_TYPE_CALL_AND_RESPONSE,
    _TRIGGER_TYPE_WEBHOOK,
)
from .db import db_select, get_db, get_db_file, init_db
from .db_interfaces import (
    _CONFIG_GIT_BRANCH,
    _CONFIG_TARGETS_DIRECTORY,
    APIKeys,
    Config,
    Images,
    Secrets,
    Users,
)
from .exceptions import (
    APIKeyAlreadyExistsException,
    APIKeyDoesNotExistException,
    BuildLogNotFoundException,
    InvalidConfigKey,
    InvalidSprinklerConfigException,
    TargetBuildException,
    UserAlreadyExistsException,
    UserDoesNotExistException,
)
from .git import Git, GitException
from .scheduler import Scheduler
from .targets import load_target, load_targets
from .task_manager import TaskManager
from .utils import get_sprinkler_directory


def init_fn():
    os.makedirs(os.path.join(get_sprinkler_directory(), "logs"), exist_ok=True)
    init_db()
    click.echo(f"Initialized SprinklerDB at {get_db_file()}")


@click.group()
def cli():
    """
    Run sprinkler processes, trigger tasks, get/set config and secrets, and more.

    Built by Henry Jones
    """
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s %(asctime)s %(name)s | %(message)s"
    )
    if not os.path.exists(get_sprinkler_directory()):
        click.secho(
            "Sprinkler has not yet been initialized. Initializing now.", fg="red"
        )
        init_fn()


@cli.command(name="version")
def version():
    """
    Return the version.
    """
    click.echo(f"Sprinkler {__version__}")


@cli.command(name="webserver")
@click.option("--host", default="0.0.0.0")
@click.option("--port", default=8476)
@click.option("--workers", default=4)
@click.option("--dev", default=False, is_flag=True)
def webserver(host: str, port: int, workers: int, dev: bool):
    """
    Run the Sprinkler webserver.
    """
    if dev:
        from .webserver import app

        app.config["development"] = True
        app.run(debug=True, host=host, port=port)
        return
    from .webserver import StandaloneApplication

    kwargs = {"bind": f"{host}:{port}", "workers": workers}
    StandaloneApplication(kwargs).run()


@cli.command(name="init")
def init_fn_command():
    """Initialize the Sprinkler environment."""
    init_fn()


@cli.command()
def task_manager():
    """Starts the Sprinkler Task Manager"""
    click.echo("Starting Sprinkler Task Manager")
    tm = TaskManager()
    asyncio.run(tm.execute())


@cli.command()
def scheduler():
    """Starts the Sprinkler Scheduler"""
    click.echo("Starting Sprinkler Scheduler")
    sc = Scheduler()
    asyncio.run(sc.execute())


@cli.group()
def git():
    """
    Targets git related actions.
    """


@git.command("pull")
def git_pull():
    """
    Pulls from remote.
    """
    git = Git(get_db())
    try:
        click.echo(git.pull())
    except GitException as e:
        raise click.ClickException(str(e))


@git.command("checkout")
@click.argument("branch")
def git_checkout(branch: str):
    """
    Checks out the given branch and updates the config.
    """
    db = get_db()
    git = Git(db)
    config = Config(db)
    try:
        config.set_value(_CONFIG_GIT_BRANCH, branch)
        click.echo(git.pull())
    except GitException as e:
        raise click.ClickException(str(e))


@git.command("init")
@click.argument("directory")
@click.argument("git-remote")
@click.option("--branch", default=None)
@click.option("--force", default=False, is_flag=True)
def git_init(directory: str, git_remote: str, branch: Optional[str], force: bool):
    """
    Initializes the target directory with a remote git repo.
    """
    if not os.path.exists(directory):
        raise click.ClickException(f"{directory} does not exist.")
    if not os.path.isdir(directory):
        raise click.ClickException(f"{directory} is not a directory.")
    d = git_remote.split("/")[-1].replace(".git", "")
    targets_dir = os.path.join(directory, d)

    db = get_db()
    git = Git(db)
    config = Config(db)
    try:
        if os.path.exists(targets_dir):
            if force:
                click.secho(f"Deleting {targets_dir}", fg="red")
                shutil.rmtree(targets_dir)
            else:
                raise click.ClickException(
                    click.style(
                        f"{targets_dir} already exists. Use --force to remove it.",
                        fg="yellow",
                    )
                )
        click.echo(f"Setting TARGETS_DIRECTORY to {targets_dir}.")
        config.set_value(_CONFIG_TARGETS_DIRECTORY, targets_dir)
        if branch is not None:
            click.echo(f"Setting GIT_BRANCH to {branch}.")
            config.set_value(_CONFIG_GIT_BRANCH, branch)
        click.echo(git.clone(directory, git_remote))
        click.echo(git.pull())
    except GitException as e:
        raise click.ClickException(str(e))


@git.command("generate-key")
@click.option("-f", "--force", default=False, is_flag=True)
def git_generate_key(force: bool):
    """
    Generate a ssh-key to be used by sprinkler.
    """
    db = get_db()
    git = Git(db)
    try:
        click.echo(git.generate_key(force=force))
        db.close()
    except GitException as e:
        raise click.ClickException(str(e))


@git.command("get-key")
def git_get_key():
    """
    Get the sprinkler public key.
    """
    db = get_db()
    git = Git(db)

    try:
        click.echo(git.get_key())
        db.close()
    except GitException as e:
        raise click.ClickException(str(e))


@cli.group()
def users():
    """
    Create, delete, or update users.
    """


@users.command(name="create")
@click.argument("username")
@click.argument("password")
@click.option("-a", "--admin", default=False, is_flag=True)
def create_user(username: str, password: str, admin: bool):
    """
    Create a new user.
    """
    users = Users(get_db())
    try:
        users.create_user(username, password, admin)
    except UserAlreadyExistsException:
        raise click.ClickException(
            f"A user with the username {username} already exists."
        )
    click.echo(f"Created user {username}.")


@users.command(name="delete")
@click.argument("username")
def delete_user(username: str):
    """
    Deletes a user.
    """
    users = Users(get_db())
    try:
        users.delete_user(username)
    except UserDoesNotExistException:
        raise click.ClickException(
            f"A user with the username {username} does not exist."
        )
    click.echo(f"Deleted user {username}.")


@users.command("update-password")
@click.argument("username")
@click.argument("password")
def update_user_password(username: str, password: str):
    """
    Updates a user's password.
    """
    users = Users(get_db())
    try:
        users.update_user(username, password=password)
    except UserDoesNotExistException:
        raise click.ClickException(
            f"A user with the username {username} does not exist."
        )
    click.echo(f"Updated user {username} password.")


@users.command("promote")
@click.argument("username")
def promote_user_password(username: str):
    """
    Makes a user an admin.
    """
    users = Users(get_db())
    try:
        users.update_user(username, admin=True)
    except UserDoesNotExistException:
        raise click.ClickException(
            f"A user with the username {username} does not exist."
        )
    click.echo(f"Promoted user {username}.")


@users.command("demote")
@click.argument("username")
def demote_user_password(username: str):
    """
    Revoke a user's admin status.
    """
    users = Users(get_db())
    try:
        users.update_user(username, admin=False)
    except UserDoesNotExistException:
        raise click.ClickException(
            f"A user with the username {username} does not exist."
        )
    click.echo(f"Demoted user {username}.")


@users.command("ls")
def ls_users():
    """
    Lists users and their admin status.
    """
    users = Users(get_db())
    results = users.get_users()
    for user in results:
        click.echo(
            f"{user.user_name} {click.style('admin', fg='green') if user.admin else click.style('not-admin', fg='red')}"
        )


@cli.group("api-keys")
def api_keys():
    """
    Create, list, or delete API Keys.
    """
    pass


@api_keys.command("create")
@click.argument("api-key-id")
def create_api_key(api_key_id: str):
    """
    Create an API Key. Returns the API key.

    Save it in a safe place as it cannot be retrieved again.
    """
    api_keys = APIKeys(get_db())
    try:
        api_key = api_keys.create_api_key(api_key_id)
    except APIKeyAlreadyExistsException:
        raise click.ClickException(
            f"An API Key already exists with the id {api_key_id}"
        )
    click.echo(api_key)


@api_keys.command("delete")
@click.argument("api-key-id")
def delete_api_key(api_key_id: str):
    """
    Deletes an API Key.
    """
    api_keys = APIKeys(get_db())
    try:
        api_keys.delete_api_key(api_key_id)
    except APIKeyDoesNotExistException:
        raise click.ClickException(
            f"An API Key does not exists with the id {api_key_id}"
        )
    click.echo(f"Deleted API Key {api_key_id}.")


@api_keys.command("ls")
def ls_api_keys():
    """
    Lists API Keys.
    """
    api_keys = APIKeys(get_db())
    results = api_keys.get_api_keys()
    for api_key_id in results:
        click.echo(api_key_id)


@cli.group()
def config():
    """
    Get, set, or list config values.
    """
    pass


@config.command(name="ls")
def config_ls():
    """
    List config options.
    """
    c = Config(get_db())
    for key, value in c.ls():
        click.echo(f"{key}  {value}")


@config.command(name="set")
@click.argument("key")
@click.argument("value")
def config_set(key: str, value: str):
    """
    Set a config option.
    """
    c = Config(get_db())
    try:
        c.set_value(key, value)
        click.echo(f"SET {key} {value}")
    except InvalidConfigKey as e:
        raise click.ClickException(f"Invalid config key `{e}`")


@config.command(name="get")
@click.argument("key")
def config_get(key: str):
    """
    Get a config value.
    """
    c = Config(get_db())
    try:
        v = c.get_value(key)
        click.echo(v)
    except InvalidConfigKey as e:
        raise click.ClickException(f"Invalid config key `{e}`")


@config.command(name="delete")
@click.argument("key")
def config_delete(key: str):
    c = Config(get_db())
    try:
        c.delete_value(key)
        click.echo(f"Deleted {key}")
    except InvalidConfigKey as e:
        raise click.ClickException(f"Invalid config key `{e}`")


@cli.group()
def secrets():
    """
    Get, set, delete, and list secrets.
    """
    pass


@secrets.command(name="set")
@click.argument("key")
@click.argument("value")
def secrets_set(key: str, value: str):
    """
    Set a secret value.
    """
    s = Secrets(get_db())
    s.set_secret(key, value)
    click.echo(f"SET {key}")


@secrets.command(name="get")
@click.argument("key")
def secrets_get(key: str):
    """
    Get a secret value.
    """
    s = Secrets(get_db())
    secret_value = s.get_secret(key)
    if secret_value is None:
        raise click.ClickException(f"No secret found with the key `{key}`.")
    click.echo(secret_value)


@secrets.command("delete")
@click.argument("key")
def secrets_delete(key: str):
    s = Secrets(get_db())
    s.delete_secret(key)
    click.echo(f"Deleted {key}.")


@secrets.command(name="ls")
def secrets_ls():
    """
    List set secrets.
    """
    s = Secrets(get_db())
    keys = s.get_secret_keys()
    for key in keys:
        click.echo(key)


@cli.group()
def targets():
    """
    Build, list, and describe targets.
    """
    pass


@targets.command(name="build-logs")
@click.argument("target")
def target_build_logs(target: str):
    """
    Retrieve the latest build logs for a target.
    """
    images = Images(get_db(), None)
    try:
        success, build_logs = images.get_target_build_logs(target)
    except BuildLogNotFoundException:
        raise click.ClickException(f"No build logs found for the target {target}.")
    click.echo(
        f"Build status for {click.style(target, bold=True)}: {click.style('SUCCESS', fg='green') if success else click.style('FAILED', fg='red')}"
    )
    click.echo("=========Build Logs==========")
    click.echo(build_logs)


@targets.command(name="build")
@click.argument("target")
@click.option("-l", "--logs", default=False, is_flag=True)
def target_build(target: str, logs: bool):
    """
    Build the image for a target.
    """
    db = get_db()
    targets_dir = Config(db).get_value(_CONFIG_TARGETS_DIRECTORY)
    if targets_dir is None:
        raise click.ClickException(f"{_CONFIG_TARGETS_DIRECTORY} is unset.")
    try:
        config = load_target(targets_dir, target)
    except InvalidSprinklerConfigException as e:
        raise click.ClickException(str(e))
    images = Images(db, docker.from_env())
    try:
        images.build_target_image(
            targets_dir,
            target,
            config.runtime,
            config.version,
            config.os,
        )
    except TargetBuildException as e:
        raise click.ClickException(f"Build Failed:\n{e}")
    if not logs:
        return
    try:
        _, build_logs = images.get_target_build_logs(target)
    except BuildLogNotFoundException:
        raise click.ClickException(f"No build logs found for the target {target}.")
    click.echo("=========Build Logs==========")
    click.echo(build_logs)


@targets.command(name="describe")
@click.argument("target")
def target_describe(target: str):
    """
    Describe a target.
    """
    targets_dir = Config(get_db()).get_value(_CONFIG_TARGETS_DIRECTORY)
    if targets_dir is None:
        raise click.ClickException(f"{_CONFIG_TARGETS_DIRECTORY} is unset.")

    try:
        config = load_target(targets_dir, target)
    except InvalidSprinklerConfigException as e:
        raise click.ClickException(str(e))

    click.echo(
        f"{click.style(target, bold=True)} {click.style(config.runtime, fg='yellow')} {click.style(config.version, fg='green')} {'' if config.os is None else click.style(config.os, fg='cyan')}"
    )

    for task in config.tasks:
        click.echo("=" * 40)
        click.secho(task.task, bold=True)
        click.echo(f"{task.entrypoint} {task.type}")
        if task.schedule:
            click.echo(f"Schedule: {task.schedule}")
        if task.timeout:
            click.echo(f"Timeout: {task.timeout} seconds.")


@targets.command(name="ls")
def targets_ls():
    """
    List targets and their validity.
    """
    targets_dir = Config(get_db()).get_value(_CONFIG_TARGETS_DIRECTORY)
    if targets_dir is None:
        raise click.ClickException(f"{_CONFIG_TARGETS_DIRECTORY} is unset.")
    for target, config in load_targets(targets_dir=targets_dir, include_errors=True):
        if isinstance(config, str):
            click.echo(f'{target} {click.style("invalid", fg="red")} {config}')
            continue
        click.echo(f'{target} {click.style("valid", fg="green")}')


@cli.group()
def tasks():
    """
    Trigger tasks.
    """
    pass


@tasks.command(name="trigger")
@click.argument("target")
@click.argument("task")
@click.option("--body")
def tasks_trigger(target: str, task: str, body: str = ""):
    """
    Trigger a task.
    """
    redis_client = redis.Redis()
    response_channel = f"sprinkler-response-channel:{uuid4().hex}"
    with redis_client.pubsub(ignore_subscribe_messages=True) as pub_sub:
        pub_sub.subscribe(response_channel)
        num_subscribers = redis_client.publish(
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
        if num_subscribers == 0:
            raise click.ClickException(
                f"Nobody was listening. Are you sure that the Sprinkler Task Manager is running?"
            )
        for message in pub_sub.listen():
            message_data = json.loads(message["data"].decode())
            if message_data.get("type") == "receipt":
                if message_data.get("success") is not True:
                    raise click.ClickException(message_data.get("message"))
                click.echo(message_data.get("message"))
                if message_data.get("task_type") == _TASK_TYPE_CALL_AND_RESPONSE:
                    continue
                return

            if message_data.get("type") == "response":
                click.echo(message_data.get("message"))
                return
            raise click.ClickException(
                "Did not get a valid response from the task manager."
            )
    raise click.ClickException("Internal Service Error")


@cli.command(name="logs")
@click.argument("task-instance-id")
@click.option("-f", "--follow", default=False, is_flag=True)
def task_instance_logs(task_instance_id: str, follow: bool = False):
    """
    Get logs for a task instance.
    """
    db = get_db()
    results = db_select(
        db,
        "select status, log_location, container_id from task_instances where id = ?;",
        (task_instance_id,),
    )
    if len(results) != 1:
        raise click.ClickException(f"No task found with id {task_instance_id}")
    status, log_location, container_id = results[0]
    if status == _TASK_INSTANCE_STATUS_WAITING:
        click.echo(f"The task {task_instance_id} is waiting to start.")
        return
    if status == _TASK_INSTANCE_STATUS_WAITING:
        status_txt = click.style(status, fg="grey")
    elif status == _TASK_INSTANCE_STATUS_RUNNING:
        status_txt = click.style(status, fg="yellow")
    elif status == _TASK_INSTANCE_STATUS_COMPLETE:
        status_txt = click.style(status, fg="green")
    elif status in (_TASK_INSTANCE_STATUS_ERROR, _TASK_INSTANCE_STATUS_TIMEOUT):
        status_txt = click.style(status, fg="red")
    else:
        status_txt = status
    click.echo(f"{task_instance_id} | {status_txt}")
    click.echo("=" * 20)
    if status == _TASK_INSTANCE_STATUS_RUNNING and container_id is not None:
        docker_client = docker.from_env()
        try:
            container = docker_client.containers.get(container_id)
            if follow:
                for line in container.logs(stream=True):
                    click.echo(line.strip())
            else:
                click.echo(container.logs())
        except docker.errors.NotFound:
            raise click.ClickException(f"Container {container_id} not found.")
    elif log_location is not None:
        with smart_open.open(log_location, "r") as f:
            click.echo(f.read())


if __name__ == "__main__":
    cli()
