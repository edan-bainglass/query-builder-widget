from __future__ import annotations


from solara import VBox
from solara.core import component

from qb_widget.utils.info import manager


@component
def InfoPanel():
    """Info panel component."""
    return VBox(manager.get_content())
