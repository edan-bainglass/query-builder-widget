from __future__ import annotations

from uuid import uuid4

from reacton import use_state
from solara import Button, VBox
from solara.core import component

from qb_widget.components.node import NodePanel
from qb_widget.models.node import NodeModel


@component
def QueryPanel():
    """Query panel component."""
    nodes, set_nodes = use_state([NodeModel(uuid4(), is_root=True)])

    def add_node():
        new_nodes = [*nodes, NodeModel(uuid4())]
        set_nodes(new_nodes)

    with VBox(classes=["container"]) as query_panel:
        for index, node in enumerate(nodes):

            def update_node(updated_node: NodeModel, i=index):
                copy = nodes.copy()
                copy[i] = updated_node
                set_nodes(copy)

            def remove_node(i: int = index):
                copy = nodes.copy()
                copy.pop(i)
                set_nodes(copy)

            NodePanel(
                node=node,
                handle_change=update_node,
                handle_close=remove_node,
            )

        Button(
            icon_name="mdi-plus",
            color="primary",
            on_click=add_node,
            classes=["mx-auto"],
        )

    return query_panel
