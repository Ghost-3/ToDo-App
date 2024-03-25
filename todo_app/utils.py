"""Module provides utility functions."""

from __future__ import annotations

from datetime import UTC, datetime, tzinfo

from .ui.filter_status import FilterStatus


class Utils:
    """A utility class for handling time zones."""

    @staticmethod
    def get_current_tzinfo() -> tzinfo | None:
        """Get the current time zone information.

        :return: The current time zone information.
        """
        return datetime.now(UTC).astimezone().tzinfo

    @staticmethod
    def get_filter_status(status: object | None) -> FilterStatus | None:
        """Get the filter status based on the provided input.

        :param status: The status to be checked.
        :return: The filter status if valid, otherwise None.
        """
        if isinstance(status, str) and status in {"all", "active", "completed"}:
            return FilterStatus.from_str(status)  # type: ignore[reportArgumentType] (The string has been verified)
        return None
