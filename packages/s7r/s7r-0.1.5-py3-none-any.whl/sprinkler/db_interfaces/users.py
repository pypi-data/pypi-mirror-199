import sqlite3
from hashlib import sha256
from typing import Optional

from pydantic import BaseModel

from ..db import db_execute, db_select
from ..exceptions import UserAlreadyExistsException, UserDoesNotExistException


class UserModel(BaseModel):
    user_name: str
    admin: bool
    password_hash: Optional[str] = None


class Users:
    db: sqlite3.Connection

    def __init__(self, db: sqlite3.Connection):
        self.db = db

    def create_user(self, username: str, password: str, admin: bool):
        existing_user = db_select(
            self.db, "select 1 from users where user_name = ?;", (username,)
        )
        if len(existing_user) != 0:
            raise UserAlreadyExistsException(username)

        password_hash = sha256(password.encode()).hexdigest()
        db_execute(
            self.db,
            "insert into users (user_name, password_hash, admin) VALUES (?, ?, ?)",
            (username, password_hash, admin),
        )

    def update_user(
        self,
        username: str,
        password: Optional[str] = None,
        admin: Optional[bool] = None,
    ):
        existing_user = db_select(
            self.db, "select 1 from users where user_name = ?;", (username,)
        )
        if len(existing_user) != 1:
            raise UserDoesNotExistException(username)

        if password is not None:
            hashed_password = sha256(password.encode()).hexdigest()
            db_execute(
                self.db,
                "update users set password_hash = ? where user_name = ?;",
                (hashed_password, username),
            )
        if admin is not None:
            db_execute(
                self.db,
                "update users set admin = ? where user_name = ?;",
                (admin, username),
            )

    def delete_user(self, username: str):
        existing_user = db_select(
            self.db, "select 1 from users where user_name = ?;", (username,)
        )
        if len(existing_user) != 1:
            raise UserDoesNotExistException(username)
        db_execute(self.db, "delete from users where user_name = ?;", (username,))

    def get_users(self):
        results = db_select(self.db, "select user_name, admin from users;", None)
        return [UserModel(user_name=result[0], admin=result[1]) for result in results]

    def verify_user_password(self, username: str, password: str):
        password_hash = sha256(password.encode()).hexdigest()
        result = db_select(
            self.db,
            "select 1 from users where user_name = ? and password_hash = ?;",
            (username, password_hash),
        )

        return len(result) == 1
