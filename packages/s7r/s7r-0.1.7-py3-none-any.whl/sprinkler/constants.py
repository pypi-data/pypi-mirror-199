from typing import Literal

_CONFIG_YAML_FILENAME = "sprinkler_config.yaml"

_TASK_MANAGER_LOGGER = "sprinkler.task_manager"
_TASK_INSTANCE_LOGGER = "sprinkler.task_instance"
_SCHEDULER_LOGGER = "sprinkler.scheduler"
_WEBSERVER_LOGGER = "sprinkler.webserver"
_IMAGES_LOGGER = "sprinkler.images"
_SECRETS_LOGGER = "sprinkler.secrets"
_GIT_LOGGER = "sprinkler.git"

_SPRINKLER_BODY_ENV_VAR = "SPRINKLER_TASK_INSTANCE_BODY"

_TASK_TYPE_FIRE_AND_FORGET = "fire-and-forget"
_TASK_TYPE_CALL_AND_RESPONSE = "call-and-response"
TASK_TYPE = Literal["fire-and-forget", "call-and-response"]

_TRIGGER_TYPE_SCHEDULED = "scheduled"
_TRIGGER_TYPE_WEBHOOK = "webhook"

_TASK_INSTANCE_STATUS_WAITING = "waiting"
_TASK_INSTANCE_STATUS_RUNNING = "running"
_TASK_INSTANCE_STATUS_ERROR = "error"
_TASK_INSTANCE_STATUS_COMPLETE = "complete"
_TASK_INSTANCE_STATUS_TIMEOUT = "timeout"

_TASK_EXECUTE_LOOP_DELAY_SLOW = 0.5
_TASK_EXECUTE_LOOP_DELAY_FAST = 0.05

TRIGGER_TYPE = Literal["scheduled", "webhook"]
TASK_INSTANCE_STATUS_TYPE = Literal[
    "waiting", "running", "error", "complete", "timeout"
]
_EXECUTE_TASK_INSTANCE_CHANNEL = "sprinkler_execute_task_instance"

_SECRET_ENVIRONMENT_VARIABLE_PREFIX = "SPRINKLER_SECRET_"

_SPRINKLER_SECRET_KEY_ENVIRONMENT_VARIABLE = "SPRINKLER_SECRET"

RUNTIME_TYPE = Literal["python", "node-npm", "node-yarn"]
