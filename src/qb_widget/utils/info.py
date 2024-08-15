from __future__ import annotations

import typing as t

from solara import reactive
from solara.components import alert


class InfoManager:
    """Manager class used for posting messages to an `InfoPanel` component."""

    def __init__(self):
        """`InfoManager` constructor."""
        self._content = reactive(t.cast(list, []))

    def get_content(self):
        """Get the current value of the reactive `content` variable."""
        return self._content.value

    def post(
        self,
        message: str,
        post_type: t.Literal["error", "warning", "success", "info"] = "info",
    ):
        """Post a message to the info panel.

        Parameters
        ----------
        `message` : `str`
            The new value for the reactive `content` variable.
        `post_type` : `str`
            The type of the message (error, warning, success, info)
        """
        if not message:
            self._content.value = []
            return

        if post_type == "error":
            new = alert.Error(message)
        elif post_type == "warning":
            new = alert.Warning(message)
        elif post_type == "success":
            new = alert.Success(message)
        else:
            new = alert.Info(message)
        self._content.value = [new]


manager = InfoManager()
