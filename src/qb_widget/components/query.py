from __future__ import annotations

import typing as t
from uuid import uuid4

from reacton import use_effect, use_state
from solara import Button, Row, Style, VBox
from solara.core import component

from qb_widget.assets.styles import css
from qb_widget.components import NodeCard
from qb_widget.models import NodeModel, ResultModel


@component
def QueryPanel(handle_submit: t.Callable[[list[ResultModel]], None]):
    """Query panel component."""
    nodes, set_nodes = use_state([NodeModel(uuid4(), is_root=True)])
    is_valid, set_is_valid = use_state(False)

    def add_node():
        new_nodes = [*nodes, NodeModel(uuid4())]
        set_nodes(new_nodes)

    def clear_query():
        set_nodes([NodeModel(uuid4(), is_root=True)])

    def show_query_code():
        pass

    def validate():
        valid = all(node.is_valid() for node in nodes)
        set_is_valid(valid)

    use_effect(validate, [nodes])

    def NodeList():
        with VBox(classes=["node-list"]):
            for index, node in enumerate(nodes):

                def update_node(updated_node: NodeModel, i=index):
                    set_nodes(nodes[:i] + [updated_node] + nodes[i + 1 :])

                def remove_node(i: int = index):
                    set_nodes(nodes[:i] + nodes[i + 1 :])

                NodeCard(
                    node=node,
                    handle_change=update_node,
                    handle_close=remove_node,
                )

            Button(
                icon_name="mdi-plus",
                color="primary",
                on_click=add_node,
                classes=["add-node-button"],
            )

    def Controls():
        with Row(classes=["query-controls"]):
            Button(
                icon_name="mdi-code-tags",
                classes=["code-toggle"],
            )
            with Row(classes=["main-controls"]):
                Button(
                    icon_name="mdi-refresh",
                    color="warning",
                    on_click=clear_query,
                )
                Button(
                    "Submit",
                    color="success",
                    on_click=lambda: handle_submit(nodes),
                    disabled=not is_valid,
                )

    Style(css / "query.css")

    with VBox(classes=["container query-panel"]):
        NodeList()
        Controls()
