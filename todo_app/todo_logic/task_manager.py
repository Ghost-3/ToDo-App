"""Module for managing tasks."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

from .task import Task

if TYPE_CHECKING:
    from datetime import datetime
    from os import PathLike

    from .task_dict import TaskDict


class TaskManager:
    """A class to manage tasks."""

    def __init__(self, path: PathLike[str] | None = None) -> None:
        """Initialize the TaskManager with the given file path.

        :param path: The path to the file where tasks will be stored.
        """
        self._path = Path(path) if path else Path("task_data.json")
        self._tasks: dict[str, Task] = {}
        self.load_tasks()

    @property
    def tasks(self) -> tuple[Task, ...]:
        """Get a tuple of all tasks stored in the TaskManager.

        :return: A tuple of Task objects representing all tasks.
        """
        return tuple(self._tasks.values())

    def save_tasks(self) -> None:
        """Save the tasks to the file specified by _path attribute."""
        save_list = tuple(value.to_dict() for value in self._tasks.values())
        with self._path.open("w") as f:
            json.dump(save_list, f)

    def load_tasks(self) -> None:
        """Load tasks from the file specified by _path attribute.

        If the file does not exist, do nothing.
        """
        if not (self._path.exists() and self._path.is_file()):
            return

        with self._path.open("r") as f:
            try:
                tasks: list[TaskDict] = json.load(f)
                self._tasks = {task["task_id"]: Task.from_dict(task) for task in tasks}
            except json.JSONDecodeError:
                self.save_tasks()

    def add_task(self, task: Task) -> bool:
        """Add a new task to the task manager.

        :param task: The task object to be added.

        :return: True if the task is successfully added, False otherwise.
        """
        if self._tasks.get(task.task_id):
            return False
        self._tasks[task.task_id] = task
        self.save_tasks()
        return True

    def modify_task(  # noqa: PLR0913 (There are actually 5 args)
        self,
        task_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        due_date: datetime | None = None,
        is_complete: bool | None = None,
    ) -> bool:
        """Modify the attributes of a task.

        :param task_id: The ID of the task to be modified.
        :param name:  The new name for the task. If None, the name remains unchanged.
        :param description: The new description for the task. If None, the description remains unchanged.
        :param due_date: The new due date for the task. If None, the due date remains unchanged.
        :param is_complete: The new completion status for the task. If None, the status remains unchanged.

        :return: True if the task is successfully modified, False otherwise.
        """
        if task := self._tasks.get(task_id):
            if name is not None:
                task.name = name
            if description is not None:
                task.description = description
            if due_date is not None:
                task.due_date = due_date
            if is_complete is not None:
                task.is_complete = is_complete
            self._tasks[task_id] = task
            self.save_tasks()
            return True
        return False

    def delete_task(self, task_id: str) -> bool:
        """Delete a task from the task manager.

        :param task_id: The ID of the task to be deleted.
        :return: True if the task is successfully deleted, False otherwise.
        """
        result = bool(self._tasks.pop(task_id))
        if result:
            self.save_tasks()
        return result
