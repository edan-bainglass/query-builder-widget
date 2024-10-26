from __future__ import annotations

import typing as t

from reacton import use_state
from solara import Head, Style, Title, VBox
from solara.core import component
from solara.lab import Tab, Tabs

from qb_widget.assets.styles import css
from qb_widget.components import HelpPanel, InfoPanel, QueryPanel, ResultsPanel
from qb_widget.models import ResultModel


@component
def App():
    """Main page component."""
    selected_tab, set_selected_tab = use_state(0)
    results, set_results = use_state(t.cast(list[ResultModel], []))
    is_loading, set_loading = use_state(False)

    def switch_tab(value: int):
        set_selected_tab(value)

    def update_results(new_results: list[ResultModel]):
        set_loading(True)
        set_results(new_results)
        set_selected_tab(1)
        set_loading(False)

    Style(css / "app.css")

    with VBox(classes=["container"]):
        with Head():
            Title("AiiDA Query Builder App")
        InfoPanel()
        with Tabs(value=selected_tab, on_value=switch_tab):
            with Tab("Query"):
                QueryPanel(handle_submit=update_results)
            with Tab("Results"):
                ResultsPanel(results, is_loading)
            with Tab("Help"):
                HelpPanel()
