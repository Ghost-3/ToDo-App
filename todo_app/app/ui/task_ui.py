"""Module contains a class TaskUi that represents a user interface for managing tasks."""

from typing import override

from flet import (
    Checkbox,
    Column,
    Container,
    CrossAxisAlignment,
    DatePicker,
    ElevatedButton,
    Icon,
    IconButton,
    MainAxisAlignment,
    Offset,
    Row,
    Text,
    TextField,
    TextThemeStyle,
    TimePicker,
    UserControl,
    colors,
    icons,
    margin,
)


class TaskUi(UserControl):
    """A class representing a user interface for managing tasks."""

    def __init__(self) -> None:
        """Initialize the TaskUi object with necessary display and edit elements."""
        super().__init__()  # type: ignore[reportUnknownMemberType] (Bad library typing)
        # Display elements
        # Task name & complete checkbox
        self._display_task: Checkbox
        self._edit_task_btn: IconButton
        self._delete_task_btn: IconButton
        # Description indicator
        self._description_indicator: Row
        # Date indicator
        self._date_indicator_text: Text
        self._date_indicator: Row
        # Time indicator
        self._time_indicator_text: Text
        self._time_indicator: Row

        self._set_display_elements()

        # Edit elements
        self._edit_name_field: TextField
        self._save_btn: IconButton
        self._edit_description_field: TextField
        self._date_picker: DatePicker
        self._time_picker: TimePicker
        self._date_picker_btn: ElevatedButton
        self._time_picker_btn: ElevatedButton

        self._set_edit_elements()

        # Views
        self._display_view: Column
        self._set_display_view()

        self._edit_view: Column
        self._set_edit_view()

    def _set_display_elements(self) -> None:
        """Set up display elements for viewing tasks."""
        # Task name & complete checkbox
        self._display_task = Checkbox()

        # Description indicator
        description_indicator_icon = Icon(name=icons.DESCRIPTION_OUTLINED, size=15)
        description_indicator_text = Text(value="Description", theme_style=TextThemeStyle.BODY_SMALL)

        self._description_indicator = Row(
            spacing=3,
            controls=[
                description_indicator_icon,
                description_indicator_text,
            ],
        )

        # Date indicator
        date_indicator_icon = Icon(name=icons.CALENDAR_MONTH_OUTLINED, size=15)

        self._date_indicator_text = Text(
            style=TextThemeStyle.BODY_SMALL,
        )

        self._date_indicator = Row(
            spacing=3,
            controls=[
                date_indicator_icon,
                self._date_indicator_text,
            ],
        )

        # Time indicator
        time_indicator_icon = Icon(name=icons.ACCESS_TIME, size=15)

        self._time_indicator_text = Text(
            style=TextThemeStyle.BODY_SMALL,
        )

        self._time_indicator = Row(
            spacing=3,
            controls=[
                time_indicator_icon,
                self._time_indicator_text,
            ],
        )

    def _set_edit_elements(self) -> None:
        """Set up edit elements for modifying task details."""
        self._edit_name_field = TextField(label="Name", expand=1)
        self._edit_description_field = TextField(label="Description", multiline=True)
        self._date_picker = DatePicker()
        self._time_picker = TimePicker()

        self._date_picker_btn = ElevatedButton(
            text="Due date",
            icon=icons.CALENDAR_MONTH_OUTLINED,
        )

        self._time_picker_btn = ElevatedButton(
            text="Due time",
            icon=icons.ACCESS_TIME,
        )

    def _set_display_view(self) -> None:
        """Set the display view layout for showing task information."""
        self._edit_task_btn = IconButton(
            icon=icons.CREATE_OUTLINED,
            tooltip="Edit task",
        )

        self._delete_task_btn = IconButton(
            icons.DELETE_OUTLINE,
            tooltip="Delete task",
        )

        btn_row = Row(
            spacing=0,
            controls=[
                self._edit_task_btn,
                self._delete_task_btn,
            ],
        )

        task_row = Row(
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=CrossAxisAlignment.CENTER,
            controls=[
                self._display_task,
                btn_row,
            ],
        )

        indicator_row = Row(
            controls=[
                self._description_indicator,
                self._date_indicator,
                self._time_indicator,
            ],
        )

        indicator_container = Container(
            margin=margin.only(left=7),
            content=indicator_row,
        )

        self._display_view = Column(
            spacing=0,
            controls=[
                task_row,
                indicator_container,
            ],
        )

    def _set_edit_view(self) -> None:
        """Set the edit view layout for editing task details."""
        self._save_btn = IconButton(
            icon=icons.DONE_OUTLINE_OUTLINED,
            icon_color=colors.GREEN,
            tooltip="Update To-Do",
        )

        edit_name_row = Row(
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=CrossAxisAlignment.CENTER,
            controls=[
                self._edit_name_field,
                self._save_btn,
            ],
        )

        pick_buttons_row = Row(
            offset=Offset(0, -0.5),
            controls=[
                self._date_picker_btn,
                self._time_picker_btn,
            ],
        )

        self._edit_view = Column(
            visible=False,
            controls=[
                edit_name_row,
                self._edit_description_field,
                self._date_picker,
                self._time_picker,
                pick_buttons_row,
            ],
        )

    @override
    def build(self) -> Column:  # type: ignore[reportIncompatibleMethodOverride] (Bad library typing)
        return Column(
            controls=[
                self._display_view,
                self._edit_view,
            ],
        )
