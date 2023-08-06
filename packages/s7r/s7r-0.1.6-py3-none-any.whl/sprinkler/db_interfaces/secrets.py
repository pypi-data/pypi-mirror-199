import logging
import os
import re
import sqlite3
from typing import Optional

from itsdangerous import BadSignature, URLSafeSerializer

from ..constants import (
    _SECRET_ENVIRONMENT_VARIABLE_PREFIX,
    _SECRETS_LOGGER,
    _SPRINKLER_SECRET_KEY_ENVIRONMENT_VARIABLE,
)
from ..db import db_execute, db_select
from ..exceptions import InvalidSecretName

logger = logging.getLogger(_SECRETS_LOGGER)


class Secrets:
    db: sqlite3.Connection
    serializer: Optional[URLSafeSerializer]
    secret_key: Optional[str]

    def __init__(self, db: sqlite3.Connection):
        self.db = db
        self.secret_key = None
        self.serializer = None

    def _create_serializer(self):
        if self.secret_key is not None:
            self.serializer = URLSafeSerializer(self.secret_key)
            return
        self.serializer = None

    def _get_sprinkler_secret(self):
        secret = os.environ.get(_SPRINKLER_SECRET_KEY_ENVIRONMENT_VARIABLE)
        if not secret:
            logger.warning(
                f"{_SPRINKLER_SECRET_KEY_ENVIRONMENT_VARIABLE} is not set. Secrets will not be encrypted. This is very unsafe."
            )
            return None
        return secret

    def _check_for_new_key(self):
        check_secret_key = self._get_sprinkler_secret()
        if check_secret_key != self.secret_key:
            self.secret_key = check_secret_key
            self._create_serializer()

    def encrypt(self, value: str):
        self._check_for_new_key()
        if self.serializer is None:
            return value
        return self.serializer.dumps(value)

    def decrypt(self, value: str):
        self._check_for_new_key()
        if self.serializer is None:
            return value
        try:
            return self.serializer.loads(value)
        except BadSignature:
            logger.error(
                "Tried to decrypt a secret but the signature didn't match. s"
                "This means that the SPRINKLER_SECRET has changed."
            )
            return value

    def set_secret(self, key: str, value: str):
        key = key.upper()
        if re.match(r"^[a-zA-Z0-9_]+$", key) is None:
            raise InvalidSecretName(key)
        encrypted_value = self.encrypt(value)
        db_execute(
            self.db,
            "INSERT OR REPLACE into secrets (key, value) VALUES (?, ?);",
            (key, encrypted_value),
        )

    def delete_secret(self, key: str):
        key = key.upper()
        db_execute(self.db, "DELETE FROM secrets where key = ?;", (key,))

    def get_secrets_for_execution(self):
        secrets = db_select(self.db, "select key, value from secrets;", None)

        return {
            f"{_SECRET_ENVIRONMENT_VARIABLE_PREFIX}{key}": self.decrypt(value)
            for key, value in secrets
        }

    def get_secret(self, key: str):
        secrets = db_select(
            self.db, "select value from secrets where key = ? limit 1;", (key,)
        )
        if len(secrets) == 0:
            return None
        return self.decrypt(str(secrets[0][0]))

    def get_secret_keys(self):
        results = db_select(self.db, "select key from secrets;", None)
        return [row[0] for row in results]
