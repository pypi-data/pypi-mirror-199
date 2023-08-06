import sqlite3
from typing import List, Optional

from pydantic import BaseModel

from ..constants import RUNTIME_TYPE, TASK_INSTANCE_STATUS_TYPE, TASK_TYPE, TRIGGER_TYPE
from ..db import db_execute, db_select
from ..exceptions import (
    InvalidTaskInstanceQueryFilter,
    TaskInstanceDoesNotExistException,
)
from ..targets.task import Task
from ..utils import now


class TaskInstanceModel(BaseModel):
    id: str
    target: str
    task: str
    timeout: Optional[int]
    entrypoint_file: str
    task_type: TASK_TYPE
    status: TASK_INSTANCE_STATUS_TYPE
    trigger_type: TRIGGER_TYPE
    created_at_time: float
    runtime: RUNTIME_TYPE
    version: str
    git_hash: str
    start_time: Optional[float]
    end_time: Optional[float]
    log_location: Optional[str]
    container_id: Optional[str]
    response_channel: str
    is_failure_task: bool


class TaskInstances:
    db: sqlite3.Connection

    def __init__(self, db: sqlite3.Connection):
        self.db = db

    def insert_task_instance(
        self,
        id: str,
        task: Task,
        status: TASK_INSTANCE_STATUS_TYPE,
        trigger_type: TRIGGER_TYPE,
        git_hash: str,
        response_channel: str,
        is_error_task: bool,
    ):
        current_timestamp = now()
        db_execute(
            self.db,
            """
INSERT INTO task_instances (
    id,
    target,
    task,
    timeout,
    entrypoint_file,
    task_type,
    status,
    trigger_type,
    created_at_time,
    runtime,
    version,
    git_hash,
    response_channel,
    is_failure_task
)
VALUES
(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """.strip(),
            (
                id,
                task.target,
                task.task,
                task.timeout,
                task.entrypoint_file,
                task.task_type,
                status,
                trigger_type,
                current_timestamp,
                task.runtime,
                task.version,
                git_hash,
                response_channel,
                is_error_task,
            ),
        )

    def update_task_instance(
        self,
        id: str,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None,
        log_location: Optional[str] = None,
        container_id: Optional[str] = None,
        status: Optional[TASK_INSTANCE_STATUS_TYPE] = None,
    ):
        set_statements = []
        args = []
        if start_time is not None:
            set_statements.append("start_time = ?")
            args.append(start_time)

        if end_time is not None:
            set_statements.append("end_time = ?")
            args.append(end_time)

        if log_location is not None:
            set_statements.append("log_location = ?")
            args.append(log_location)

        if container_id is not None:
            set_statements.append("container_id = ?")
            args.append(container_id)

        if status is not None:
            set_statements.append("status = ?")
            args.append(status)

        if len(set_statements) == 0:
            return
        args.append(id)
        db_execute(
            self.db,
            f"update task_instances SET {' , '.join(set_statements)} where id = ?;",
            tuple(args),
        )

    def get_task_instance(self, id: str):
        results = self.get_task_instances(id=id)
        if len(results) != 1:
            raise TaskInstanceDoesNotExistException(id)
        return results[0]

    def get_task_instances(
        self,
        id: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
        sort_by: str = "created_at_time",
        sort_ascending: bool = False,
        target: List[str] = [],
        task: List[str] = [],
        task_type: List[str] = [],
        status: List[TASK_INSTANCE_STATUS_TYPE] = [],
        trigger_type: List[TRIGGER_TYPE] = [],
        runtime: List[RUNTIME_TYPE] = [],
        version: List[str] = [],
        git_hash: List[str] = [],
        created_at_time_start: Optional[float] = None,
        created_at_time_end: Optional[float] = None,
        start_time_start: Optional[float] = None,
        start_time_end: Optional[float] = None,
        end_time_start: Optional[float] = None,
        end_time_end: Optional[float] = None,
    ):
        filter_statements = []
        args = []

        if sort_by not in {"created_at_time", "start_time", "end_time"}:
            raise InvalidTaskInstanceQueryFilter(f"sort_by: {sort_by}")

        sort_direction = "asc" if sort_ascending else "desc"

        if len(target) > 0:
            filter_statements.append(_make_in_filter_statement("target", target))
            args += target

        if len(task) > 0:
            filter_statements.append(_make_in_filter_statement("task", task))
            args += task

        if len(task_type) > 0:
            filter_statements.append(_make_in_filter_statement("task_type", task_type))
            args += task_type

        if len(status) > 0:
            filter_statements.append(_make_in_filter_statement("status", status))
            args += status

        if len(trigger_type) > 0:
            filter_statements.append(
                _make_in_filter_statement("trigger_type", trigger_type)
            )
            args += trigger_type

        if len(runtime) > 0:
            filter_statements.append(_make_in_filter_statement("runtime", runtime))
            args += runtime

        if len(version) > 0:
            filter_statements.append(_make_in_filter_statement("version", version))
            args += version

        if len(git_hash) > 0:
            filter_statements.append(_make_in_filter_statement("git_hash", git_hash))
            args += git_hash

        if created_at_time_start is not None:
            filter_statements.append(f"created_at_time >= ?")
            args.append(created_at_time_start)

        if created_at_time_end is not None:
            filter_statements.append(f"created_at_time < ?")
            args.append(created_at_time_end)

        if start_time_start is not None:
            filter_statements.append(f"start_time >= ?")
            args.append(start_time_start)

        if start_time_end is not None:
            filter_statements.append(f"start_time < ?")
            args.append(start_time_end)

        if end_time_start is not None:
            filter_statements.append(f"end_time >= ?")
            args.append(end_time_start)

        if end_time_end is not None:
            filter_statements.append(f"end_time < ?")
            args.append(end_time_end)

        if id is not None:
            filter_statements.append(f"id = ?")
            args.append(id)

        args.append(limit)
        args.append(offset)

        where_clause = (
            ""
            if len(filter_statements) == 0
            else "WHERE " + " AND ".join(filter_statements)
        )
        query = f"""
select id,
    target,
    task,
    timeout,
    entrypoint_file,
    task_type,
    status,
    trigger_type,
    created_at_time,
    runtime,
    version,
    git_hash,
    start_time,
    end_time,
    log_location,
    container_id,
    response_channel,
    is_failure_task
from task_instances
{where_clause}
order by {sort_by} {sort_direction}
limit ? offset ?;
        """.strip()
        results = db_select(
            self.db,
            query,
            tuple(args),
        )

        return [
            TaskInstanceModel(
                id=row[0],
                target=row[1],
                task=row[2],
                timeout=row[3],
                entrypoint_file=row[4],
                task_type=row[5],
                status=row[6],
                trigger_type=row[7],
                created_at_time=row[8],
                runtime=row[9],
                version=row[10],
                git_hash=row[11],
                start_time=row[12],
                end_time=row[13],
                log_location=row[14],
                container_id=row[15],
                response_channel=row[16],
                is_failure_task=row[17],
            )
            for row in results
        ]


def _make_in_filter_statement(column: str, filter_value: list):
    return f"""{column} in ({",".join(["?" for _ in filter_value])})"""
