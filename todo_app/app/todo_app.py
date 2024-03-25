"""Module representing a Todo App user control with task management functionality."""

from typing import override

from flet import (
    Column,
    ControlEvent,
    FloatingActionButton,
    Row,
    Tab,
    Tabs,
    TextField,
    UserControl,
    icons,
)

from todo_app.todo_logic.task import Task
from todo_app.todo_logic.task_manager import TaskManager

from .filter_status import FilterStatus
from .task_control import TaskControl
from .task_event import TaskEvent
from .ui.todo_app_ui import TodoAppUi


class TodoAppControl(TodoAppUi):
    """A class representing a Todo App user control."""

    def __init__(self) -> None:
        """Initialize a new instance of TodoApp."""
        super().__init__()
        self.add_task_button.on_click = self.add_clicked
        self.filter.on_change = self.tabs_changed

        self.task_manager = TaskManager()
        self.load_tasks()

    def load_tasks(self) -> None:
        """Load tasks from a file during initialization.

        This method loads tasks using the TaskManager and creates TaskUi objects for each task to update the UI.
        """
        self.task_manager.load_tasks()
        for task in self.task_manager.tasks:
            task_ui = TaskControl(task, self.on_task_event)
            self.task_list.controls.append(task_ui)

    @override
    def update(self) -> None:
        """Update the screen with changes based on selected filter status.

        Method checks the filter status and updates the visibility of tasks accordingly.
        """
        if not (tabs := self.filter.tabs):
            return
        filter_index = self.filter.selected_index if self.filter.selected_index else 0

        if isinstance(status := tabs[filter_index].text, str) and status in {"all", "active", "completed"}:  # type: ignore[reportUnknownMemberType] (Bad library typing)
            status = FilterStatus.from_str(status)  # type: ignore[reportArgumentType] (The string has been verified)
        else:
            return

        for task_ui in self.task_list.controls:
            if not isinstance(task_ui, TaskControl):
                continue
            task_ui.visible = (
                status == FilterStatus.ALL
                or (status == FilterStatus.ACTIVE and task_ui.task.is_complete is False)
                or (status == FilterStatus.COMPLETED and task_ui.task.is_complete)
            )

        super().update()

    def add_clicked(self, _: ControlEvent) -> None:
        """Handle the click event when the add button is clicked.

        :param _: The control event object.
        """
        if not self.new_task_field.value:
            return
        task_ui = TaskControl(
            Task(self.new_task_field.value),
            self.on_task_event,
        )
        if self.task_manager.add_task(task_ui.task):
            self.task_list.controls.append(task_ui)
            self.new_task_field.value = ""
            self.update()

    def on_task_event(self, task_event: TaskEvent, task_ui: TaskControl) -> None:
        """Handle a task event by modifying tasks in the TaskManager and updating the UI.

        :param task_event: The TaskEvent that occurred for the task.
        :param task_ui: The TaskUi object associated with the task.
        """
        task = task_ui.task
        match task_event:
            case TaskEvent.MODIFY:
                result = self.task_manager.modify_task(
                    task_id=task.task_id,
                    name=task.name,
                    description=task.description,
                    due_date=task.due_date,
                    due_time=task.due_time,
                )
            case TaskEvent.SWITCH_COMPLETE:
                result = self.task_manager.modify_task(task.task_id, is_complete=task.is_complete)
            case TaskEvent.DELETE:
                result = self.task_manager.delete_task(task.task_id)
                if result:
                    self.task_list.controls.remove(task_ui)
        if result:
            self.update()

    def tabs_changed(self, _: ControlEvent) -> None:
        """Handle the event when filter tab are changed.

        :param _: The control event object.
        """
        self.update()
