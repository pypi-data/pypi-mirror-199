import os
from datetime import datetime


def now():
    return datetime.utcnow().timestamp()


def get_sprinkler_directory():
    return os.path.join(os.path.expanduser("~"), ".sprinkler")


def make_target_image_name(target: str):
    return f"sprinkler-target-image:{target}"
