"""Module contains the Task class and related attributes for creating and managing tasks."""

from collections.abc import Callable
from typing import override

from flet import (
    Checkbox,
    Column,
    ControlEvent,
    CrossAxisAlignment,
    IconButton,
    MainAxisAlignment,
    Row,
    TextField,
    UserControl,
    colors,
    icons,
)

from todo_app.todo_logic import Task

from .task_event import TaskEvent


class TaskUi(UserControl):
    """Represents a task for managing to-do items."""

    def __init__(
        self,
        task: Task,
        on_task_event: Callable[[TaskEvent, "TaskUi"], None],
    ) -> None:
        """Initialize a Task object with the given parameters.

        :param task_name: The name of the task.
        :param task_status_change: A callback function for handling status changes of the task.
        :param task_delete: A callback function for deleting the task.
        """
        super().__init__()  # type: ignore (Bad library typing)
        self._task = task

        self.on_task_event = on_task_event

        self.display_task = Checkbox(value=self.task.is_complete, label=self._task.name, on_change=self.status_changed)
        self.edit_name_field = TextField(expand=1)

        self.display_view = Row(
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=CrossAxisAlignment.CENTER,
            controls=[
                self.display_task,
                Row(
                    spacing=0,
                    controls=[
                        IconButton(
                            icon=icons.CREATE_OUTLINED,
                            tooltip="Edit To-Do",
                            on_click=self.edit_clicked,
                        ),
                        IconButton(
                            icons.DELETE_OUTLINE,
                            tooltip="Delete To-Do",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = Row(
            visible=False,
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=CrossAxisAlignment.CENTER,
            controls=[
                self.edit_name_field,
                IconButton(
                    icon=icons.DONE_OUTLINE_OUTLINED,
                    icon_color=colors.GREEN,
                    tooltip="Update To-Do",
                    on_click=self.save_clicked,
                ),
            ],
        )

    @property
    def task(self) -> Task:
        """Returns the Task instance responsible for managing the task logic.

        :return: The Task instance handling the task logic.
        """
        return self._task

    @override
    def build(self) -> Column:  # type: ignore (Bad library typing)
        return Column(controls=[self.display_view, self.edit_view])

    def edit_clicked(self, _: ControlEvent) -> None:
        """Handle edit button click event.

        :param _: The control event object.
        """
        self.edit_name_field.value = str(self.display_task.label)  # type: ignore (Bad library typing)
        self.edit_name_field.focus()
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, _: ControlEvent) -> None:
        """Handle save button click event.

        :param _: The control event object.
        """
        if not (isinstance(string := self.edit_name_field.value, str) and string.strip()):
            return
        string = string.strip()
        self.display_task.label = string
        self.display_view.visible = True
        self.edit_view.visible = False
        self.task.name = string
        self.on_task_event(TaskEvent.RENAME, self)
        self.update()

    def status_changed(self, _: ControlEvent) -> None:
        """Handle status change event.

        :param _: The control event object.
        """
        if (is_complete := self.display_task.value) is None:
            return
        self._task.is_complete = is_complete
        self.on_task_event(TaskEvent.SWITCH_COMPLETE, self)

    def delete_clicked(self, _: ControlEvent) -> None:
        """Handle delete button click event.

        :param _: The control event object.
        """
        self.on_task_event(TaskEvent.DELETE, self)
