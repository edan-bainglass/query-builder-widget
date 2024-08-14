import typing as t
from dataclasses import replace

from solara import Button, InputText, Row, Select, VBox
from solara.core import component

from qb_widget.models.node import NodeModel


@component
def NodePanel(
    node: NodeModel,
    handle_change: t.Callable[[NodeModel], None],
    handle_close: t.Callable[[], None],
):
    """Node panel component."""

    def select_type(value: str):
        handle_change(replace(node, type=value))

    def select_relationship(value: str):
        handle_change(replace(node, relationship=value))

    def reset_panel():
        handle_change(NodeModel(id=node.id, is_root=node.is_root))

    def ResetButton():
        return Button(
            icon_name="mdi-refresh",
            color="warning",
            on_click=reset_panel,
        )

    def CloseButton():
        return Button(
            icon_name="mdi-close",
            color="error",
            on_click=handle_close,
        )

    with VBox(classes=["container border px-5 mb-3"]) as node_panel:
        with Row(classes=["align-items-center"]):
            Select(
                label="Type",
                values=[
                    "Data",
                    "Process",
                    "Group",
                ],
                value=node.type,
                on_value=select_type,
                classes=["me-3 w-100"],
            )
            InputText("Tag", classes=["me-3"])
            ResetButton() if node.is_root else CloseButton()
        if not node.is_root:
            with Row(classes=["align-items-center"]):
                Select(
                    label="With",
                    values=[
                        "Incoming",
                        "Outgoing",
                        "Group",
                    ],
                    value=node.relationship,
                    on_value=select_relationship,
                    classes=["me-3 w-100"],
                )
                InputText("Tag", classes=["me-3"])
                ResetButton()

    return node_panel
