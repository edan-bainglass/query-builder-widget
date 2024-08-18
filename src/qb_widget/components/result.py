from __future__ import annotations

from solara import Card, display
from solara.core import component

from qb_widget.models.result import ResultModel


@component
def ResultCard(result: ResultModel):
    """Result card component."""
    with Card(
        title=f"Result {result.id}",
        margin=0,
        classes=["result-card mb-2"],
    ):
        display(result.content)
