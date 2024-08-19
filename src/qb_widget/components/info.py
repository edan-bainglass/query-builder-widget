from __future__ import annotations

from solara import Button, Row, VBox
from solara.core import component

from qb_widget.utils.info import notice


@component
def InfoPanel():
    """Info panel component."""
    visible = notice.has_content()

    def close_panel():
        notice.clear()

    with Row(classes=["container" if visible else "", "info-panel"]):
        if visible:
            VBox(notice.get_content())
            Button(
                icon_name="mdi-close",
                color="error",
                on_click=close_panel,
                classes=["close-info-button"],
            )
