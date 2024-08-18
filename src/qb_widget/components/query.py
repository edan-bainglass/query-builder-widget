from __future__ import annotations

import typing as t
from uuid import uuid4

from reacton import use_state
from solara import Button, Row, Style, VBox
from solara.core import component

from qb_widget.assets.styles import css
from qb_widget.components import NodeCard
from qb_widget.models import NodeModel
from qb_widget.models.result import ResultModel
from qb_widget.services.aiida import AiiDAService


@component
def QueryPanel(handle_submit: t.Callable[[ResultModel], None]):
    """Query panel component."""
    nodes, set_nodes = use_state([NodeModel(uuid4(), is_root=True)])

    def add_node():
        new_nodes = [*nodes, NodeModel(uuid4())]
        set_nodes(new_nodes)

    def submit_query():
        results = [
            ResultModel(id=i, content=result)
            for i, result in enumerate(AiiDAService.get_results(nodes), 1)
        ]
        handle_submit(results)

    def clear_query():
        set_nodes([NodeModel(uuid4(), is_root=True)])

    def show_query_code():
        pass

    def NodeList():
        with VBox(classes=["node-list"]):
            for index, node in enumerate(nodes):

                def update_node(updated_node: NodeModel, i=index):
                    copy = nodes.copy()
                    copy[i] = updated_node
                    set_nodes(copy)

                def remove_node(i: int = index):
                    copy = nodes.copy()
                    copy.pop(i)
                    set_nodes(copy)

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
                classes=["code-toggle"]
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
                    on_click=submit_query,
                )

    Style(css / "query.css")

    with VBox(classes=["container query-panel"]):
        NodeList()
        Controls()
