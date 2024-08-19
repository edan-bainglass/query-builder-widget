from __future__ import annotations

import typing as t
from enum import Enum

from solara import reactive
from solara.components import alert


class Types(Enum):
    """Types of messages that can be posted to the `InfoPanel` component."""

    ERROR = "error"
    WARNING = "warning"
    SUCCESS = "success"
    INFO = "info"


class Notice:
    """Utility class used for posting messages to the `InfoPanel` component."""

    TYPES = Types

    def __init__(self):
        """`InfoManager` constructor."""
        self._content = reactive(t.cast(list, []))

    def get_content(self):
        """Get the current value of the reactive `content` variable."""
        return self._content.value

    def has_content(self) -> bool:
        """Check if the info panel has content."""
        return bool(self._content.value)

    def post(
        self,
        message: str,
        post_type: Types,
    ):
        """Post a message to the info panel.

        Parameters
        ----------
        `message` : `str`
            The new value for the reactive `content` variable.
        `post_type` : `Types`
            The enumerated type of the message (error, warning, success, info)
        """
        if not message:
            self.clear()
            return

        try:
            notifier = getattr(alert, post_type.value.capitalize())
            self._content.value = [notifier(message)]
        except AttributeError as err:
            error = f"Internal error: {err} - Please contact the development team"
            self._content.value = [alert.Error(error)]

    def clear(self):
        """Clear the content of the info panel."""
        self._content.value = []


notice = Notice()
