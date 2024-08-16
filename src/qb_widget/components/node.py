from __future__ import annotations

import typing as t
from dataclasses import replace

from reacton import use_effect, use_state
from solara import Button, InputText, Row, Select, Style, VBox
from solara.core import component

from qb_widget.assets.styles import css
from qb_widget.models import NodeModel
from qb_widget.services import AiiDAService
from qb_widget.services.aiida import NodeType
from qb_widget.utils import info


@component
def NodePanel(
    node: NodeModel,
    handle_change: t.Callable[[NodeModel], None],
    handle_close: t.Callable[[], None],
):
    """Node panel component."""
    types, set_types = use_state(t.cast(dict[str, NodeType], {}))
    relationships, set_relationships = use_state([""])

    def select_type(value: str):
        try:
            node_type = types[value]
        except KeyError:
            info.manager.post(f"Type {value} not found", "error")
            node_type = NodeType()
        handle_change(replace(node, type=node_type))

    def select_relationship(value: str):
        handle_change(replace(node, relationship=value))

    def reset_panel():
        handle_change(NodeModel(id=node.id, is_root=node.is_root))

    def fetch_types():
        types = AiiDAService.get_node_types()
        set_types(types)

    def update_relationships():
        if not node.type.name:
            return
        relationships = AiiDAService.get_relationships(node.type)
        set_relationships(relationships)

    use_effect(fetch_types, [])

    use_effect(update_relationships, [node.type])

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

    with VBox(classes=["container node-panel"]):
        Style(css / "node.css")

        with Row(classes=["align-items-center"]):
            Select(
                label="Type",
                values=[type.name for type in types.values()],
                value=node.type.name,
                on_value=select_type,
                classes=["me-3 w-100"],
            )
            InputText("Tag", classes=["me-3"])
            ResetButton() if node.is_root else CloseButton()
        if not node.is_root:
            with Row(classes=["align-items-center"]):
                Select(
                    label="With",
                    values=relationships,
                    value=node.relationship,
                    on_value=select_relationship,
                    classes=["me-3 w-100"],
                )
                InputText("Tag", classes=["me-3"])
                ResetButton()
