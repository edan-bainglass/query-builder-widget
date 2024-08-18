from __future__ import annotations

import typing as t

from reacton import use_state
from solara import Head, Style, Title, VBox
from solara.core import component
from solara.lab import Tab, Tabs

from qb_widget.assets.styles import css
from qb_widget.components import HelpPanel, InfoPanel, QueryPanel
from qb_widget.components.results import ResultsPanel
from qb_widget.models.result import ResultModel


@component
def App():
    """Main page component."""
    selected_tab, set_selected_tab = use_state(0)
    results, set_results = use_state(t.cast(list[ResultModel], []))

    def switch_tab(value):
        set_selected_tab(value)

    def update_results(new_results):
        set_results(new_results)
        set_selected_tab(1)

    Style(css / "app.css")

    with VBox(classes=["container"]):
        with Head():
            Title("AiiDA Query Builder App")
        InfoPanel()
        with Tabs(value=selected_tab, on_value=switch_tab):
            with Tab("Query"):
                QueryPanel(handle_submit=update_results)
            with Tab("Results"):
                ResultsPanel(results)
            with Tab("Help"):
                HelpPanel()
