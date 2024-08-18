from __future__ import annotations

from solara import Style, VBox
from solara.core import component

from qb_widget.assets.styles import css
from qb_widget.components.result import ResultCard
from qb_widget.models.result import ResultModel


@component
def ResultsPanel(results: list[ResultModel]):
    """Results panel component."""
    Style(css / "results.css")

    with VBox(classes=["container results-panel"]):
        for result in results:
            ResultCard(result)
