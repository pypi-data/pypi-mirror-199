class SprinklerException(Exception):
    """
    All Sprinkler exceptions inherit from this.
    """


class TargetsDirectoryUnsetException(SprinklerException):
    """
    raised when an action is taken that requires the TARGETS_DIRECTORY
    to be set, but it is not
    """


class GitException(SprinklerException):
    """
    Raised when there is an exception with a git command.
    """


class APIKeyAlreadyExistsException(SprinklerException):
    """
    raised when creating an API Key that already exists.
    """


class APIKeyDoesNotExistException(SprinklerException):
    """
    raised when an action is taken on an API key that does not exist.
    """


class InvalidConfigKey(SprinklerException):
    """
    raised when an operation is attempted on a non-existent config key.
    """


class TargetBuildException(SprinklerException):
    """
    raised when there is an exception while building a target.
    """


class BuildLogNotFoundException(SprinklerException):
    """
    raised when build logs are not found for a target.
    """


class TaskInstanceDoesNotExistException(SprinklerException):
    """
    Raised when a task instance does not exist in the db.
    """


class InvalidTaskInstanceQueryFilter(SprinklerException):
    """
    Raised when an invalid filter is provided
    """


class UserAlreadyExistsException(SprinklerException):
    """
    raised when creating a user that already exists.
    """


class UserDoesNotExistException(SprinklerException):
    """
    raised when an action is taken on a user that doesn't exist.
    """


class InvalidSprinklerConfigException(SprinklerException):
    """
    Exception raised when the sprinkler_config.yaml is invalid.
    """


class TaskCreationException(SprinklerException):
    """
    raised when a task is unable to be created.
    """


class InvalidSecretName(SprinklerException):
    """
    raised when a secret name is invalid.
    """
