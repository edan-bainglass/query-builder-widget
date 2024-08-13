from solara import VBox
from solara.core import component

from qb_widget.components.node import NodePanel


@component
def QueryPanel():
    """Query panel component."""

    with VBox(classes=["container"]):
        NodePanel()
