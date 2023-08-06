import os
import sqlite3
from typing import Optional, Tuple

from .utils import get_sprinkler_directory


def get_db_file():
    return os.path.join(get_sprinkler_directory(), "sprinkler.db")


def get_db():
    return sqlite3.connect(get_db_file())


def db_select(conn: sqlite3.Connection, query: str, args: Optional[Tuple]) -> list:
    cursor = conn.cursor()
    if args is None:
        cursor.execute(query)
    else:
        cursor.execute(query, args)
    results = cursor.fetchall()
    cursor.close()
    return results


def db_execute(conn: sqlite3.Connection, query: str, args: Optional[Tuple]) -> None:
    cursor = conn.cursor()
    if args is None:
        cursor.execute(query)
    else:
        cursor.execute(query, args)
    cursor.close()
    conn.commit()


DDL = [
    """
CREATE TABLE IF NOT EXISTS task_instances (
    id TEXT,
    target TEXT,
    task TEXT,
    timeout INTEGER,
    entrypoint_file TEXT,
    task_type TEXT,
    status TEXT,
    trigger_type TEXT,
    created_at_time REAL,
    runtime TEXT,
    version TEXT,
    git_hash TEXT,

    start_time REAL,
    end_time REAL,
    log_location TEXT,
    container_id TEXT,
    response_channel TEXT,
    is_failure_task BOOL,


    primary key (id)
);
    """.strip(),
    """
CREATE TABLE IF NOT EXISTS secrets (
    key TEXT,
    value TEXT,
    primary key (key)
);
    """.strip(),
    """
CREATE TABLE IF NOT EXISTS config (
    key TEXT,
    value TEXT,
    primary key (key)
);
    """.strip(),
    """
CREATE TABLE IF NOT EXISTS target_build_logs (
    target TEXT,
    build_logs TEXT,
    success BOOLEAN,
    primary key (target)
);
    """.strip(),
    """
CREATE TABLE IF NOT EXISTS users (
    user_name TEXT,
    password_hash TEXT,
    admin BOOLEAN,
    primary key (user_name)
);
    """.strip(),
    """
CREATE TABLE IF NOT EXISTS api_keys (
    api_key_id TEXT,
    api_key_hash TEXT,
    primary key (api_key_id)
);
    """.strip(),
]


def init_db():
    conn = get_db()
    cursor = conn.cursor()
    for table in DDL:
        cursor.execute(table)
        conn.commit()
    cursor.close()
    conn.close()
