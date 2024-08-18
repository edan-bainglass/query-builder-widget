from __future__ import annotations

import typing as t
from dataclasses import replace

from reacton import use_effect, use_state
from solara import Button, Card, Column, InputText, Row, Select
from solara.core import component

from qb_widget.models import NodeModel
from qb_widget.services import AiiDAService
from qb_widget.services.aiida import NodeType
from qb_widget.utils import info


@component
def NodeCard(
    node: NodeModel,
    handle_change: t.Callable[[NodeModel], None],
    handle_close: t.Callable[[], None],
):
    """Node card component."""
    types, set_types = use_state(t.cast(dict[str, NodeType], {}))
    relationship_types, set_relationship_types = use_state(t.cast(list[str], []))

    def select_type(value: str):
        try:
            node_type = types[value]
        except KeyError:
            info.manager.post(f"Type {value} not found", "error")
            node_type = NodeType()
        info.manager.clear()
        handle_change(replace(node, type=node_type))

    def select_relationship(value: str):
        handle_change(replace(node, relationship=value))

    def reset_panel():
        handle_change(NodeModel(id=node.id, is_root=node.is_root))

    def fetch_types():
        types = AiiDAService.get_node_types()
        set_types(types)

    def fetch_relationship_types():
        if node.is_root:
            return
        relationships = AiiDAService.get_relationship_types(node.type)
        set_relationship_types(relationships)

    use_effect(fetch_types, [])

    use_effect(fetch_relationship_types, [node.type])

    def Controls():
        with Row(classes=["node-controls"]):
            Button(
                icon_name="mdi-filter",
                classes=["filter-node-button"],
            )
            Button(
                icon_name="mdi-format-list-bulleted",
                classes=["project-node-button"],
            )
            Button(
                icon_name="mdi-refresh",
                color="warning",
                on_click=reset_panel,
                classes=["reset-node-button"],
            )
            if not node.is_root:
                Button(
                    icon_name="mdi-close",
                    color="error",
                    on_click=handle_close,
                    classes=["close-node-button"],
                )

    def TypeSelector():
        with Row(classes=["selector-row"]):
            with Column(classes=["flex-grow-1"]):
                Select(
                    label="Select node type",
                    values=[type.name for type in types.values()],
                    value=node.type.name,
                    on_value=select_type,
                )
            with Column():
                InputText("Our tag", classes=["me-3"])

    def RelationshipSelector():
        with Row(classes=["selector-row"]):
            with Column(classes=["flex-grow-1"]):
                Select(
                    label="Select relationship",
                    values=relationship_types,
                    value=node.relationship,
                    on_value=select_relationship,
                )  # type: ignore
            with Column():
                InputText("Their tag", classes=["me-3"])

    with Card(
        margin=0,
        classes=[
            "container node-card",
            "root" if node.is_root else "",
        ],
    ):
        Controls()
        TypeSelector()

        if not node.is_root:
            RelationshipSelector()
