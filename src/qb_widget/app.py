from __future__ import annotations

import typing as t

from qb_widget.models.node import NodeModel
from qb_widget.services.aiida import AiiDAService
from reacton import use_state
from solara import Head, Result, ResultState, Style, Title, VBox, use_thread
from solara.core import component
from solara.lab import Tab, Tabs

from qb_widget.assets.styles import css
from qb_widget.components import HelpPanel, InfoPanel, QueryPanel, ResultsPanel
from qb_widget.models import ResultModel


@component
def App():
    """Main page component."""
    selected_tab, set_selected_tab = use_state(0)
    query, set_query = use_state(t.cast(list[NodeModel], []))

    def switch_tab(value: int):
        set_selected_tab(value)

    def fetch_results() -> list[ResultModel] | None:
        if query:
            response = [
                ResultModel(
                    id=i,
                    content=result,
                )
                for i, result in enumerate(AiiDAService.get_results(query), 1)
            ]
            return response

    def submit_query(query: list[NodeModel]):
        set_query(query)
        set_selected_tab(1)

    fetching: Result[list[ResultModel]] = use_thread(fetch_results, [query])

    if fetching.state == ResultState.FINISHED:
        if fetching.value:
            results, is_loading = fetching.value, False
        else:
            results, is_loading = [], False
    elif fetching.state == ResultState.ERROR:
        print(fetching.error)
    else:
        results, is_loading = [], True

    Style(css / "app.css")

    with VBox(classes=["container"]):
        with Head():
            Title("AiiDA Query Builder App")
        InfoPanel()
        with Tabs(value=selected_tab, on_value=switch_tab):
            with Tab("Query"):
                QueryPanel(handle_submit=submit_query)
            with Tab("Results"):
                ResultsPanel(results, is_loading)
            with Tab("Help"):
                HelpPanel()
