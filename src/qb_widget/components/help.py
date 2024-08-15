from __future__ import annotations

from solara import Text, VBox
from solara.core import component


@component
def HelpPanel():
    """Help panel component."""

    with VBox(classes=["container"]):
        Text("Tutorial goes here")
