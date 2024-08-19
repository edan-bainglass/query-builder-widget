from __future__ import annotations

import typing as t

from solara import Card, display
from solara.core import component

if t.TYPE_CHECKING:
    from qb_widget.models import ResultModel


@component
def ResultCard(result: ResultModel):
    """Result card component."""
    with Card(
        title=f"Result {result.id}",
        margin=0,
        classes=["result-card mb-2"],
    ):
        display(result.content)
