"""Module containing TaskDict type definition."""

from datetime import datetime
from typing import TypedDict


class TaskDict(TypedDict):
    """Type definition for a dictionary representing a task."""

    name: str
    """The name of the task."""

    description: str | None
    """The description of the task, or None if not provided."""

    due_date: datetime | None
    """The due date of the task, or None if not specified."""

    task_id: str
    """The unique identifier of the task."""

    is_complete: bool
    """The completion status of the task."""
