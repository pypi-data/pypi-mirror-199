import sqlite3
from hashlib import sha256
from uuid import uuid4

from ..db import db_execute, db_select
from ..exceptions import APIKeyAlreadyExistsException, APIKeyDoesNotExistException


class APIKeys:
    db: sqlite3.Connection

    def __init__(self, db: sqlite3.Connection):
        self.db = db

    def create_api_key(self, api_key_id: str) -> str:
        api_key = uuid4().hex
        hashed_api_key = sha256(api_key.encode()).hexdigest()
        results = db_select(
            self.db, "select 1 from api_keys where api_key_id = ?;", (api_key_id,)
        )
        if len(results) != 0:
            raise APIKeyAlreadyExistsException(api_key_id)

        db_execute(
            self.db,
            "insert into api_keys (api_key_id, api_key_hash) values (?, ?);",
            (api_key_id, hashed_api_key),
        )
        return api_key

    def delete_api_key(self, api_key_id: str):
        results = db_select(
            self.db, "select 1 from api_keys where api_key_id = ?;", (api_key_id,)
        )
        if len(results) == 0:
            raise APIKeyDoesNotExistException(api_key_id)
        db_execute(self.db, "delete from api_keys where api_key_id = ?;", (api_key_id,))

    def get_api_keys(self):
        results = db_select(self.db, "select api_key_id from api_keys;", None)
        return [result[0] for result in results]

    def verify_api_key(self, api_key: str):
        hashed_api_key = sha256(api_key.encode()).hexdigest()
        results = db_select(
            self.db, "select 1 from api_keys where api_key_hash = ?;", (hashed_api_key,)
        )
        return len(results) == 1
