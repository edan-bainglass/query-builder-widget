from __future__ import annotations

import typing as t

from reacton import use_state
from solara import Button, Row, Style, Text, VBox
from solara.core import component

from qb_widget.assets.styles import css
from qb_widget.components import ResultCard

if t.TYPE_CHECKING:
    from qb_widget.models import ResultModel


@component
def ResultsPanel(results: list[ResultModel]):
    """Results panel component."""
    page, set_page = use_state(1)

    last_page = len(results) // 10 + (1 if len(results) % 10 != 0 else 0)
    start_page = max(1, page - 4) if last_page > 10 else 1
    end_page = min(start_page + 9, last_page)
    if last_page <= 10:
        end_page = last_page
    else:
        start_page = max(1, end_page - 9)

    def select_page(p: int):
        if 1 <= p <= last_page:
            set_page(p)

    Style(css / "results.css")

    def Ellipsis(condition: bool):
        return Text(
            "...",
            classes=[
                "more-pages",
                "show" if condition else "hide",
            ],
        )

    def Pagination():
        with Row(classes=["pagination-controls"]):
            with Row(classes=["page-back-buttons"]):
                Button(
                    icon_name="mdi-chevron-double-left",
                    on_click=lambda: select_page(1),
                )
                Button(
                    icon_name="mdi-chevron-left",
                    on_click=lambda: select_page(page - 1),
                )
            with Row(classes=["page-buttons"]):
                if last_page > 10:
                    Ellipsis(start_page > 1)
                for i in range(start_page, end_page + 1):
                    Button(
                        label=str(i),
                        on_click=lambda index=i: select_page(index),
                        classes=["active" if page == i else ""],
                    )
                if last_page > 10:
                    Ellipsis(end_page < last_page)
            with Row(classes=["page-forward-buttons"]):
                Button(
                    icon_name="mdi-chevron-right",
                    on_click=lambda: select_page(page + 1),
                )
                Button(
                    icon_name="mdi-chevron-double-right",
                    on_click=lambda: select_page(last_page),
                )

    def ResultList():
        for result in results[(page - 1) * 10 : page * 10]:
            ResultCard(result)

    with VBox(classes=["container results-panel"]):
        if results:
            Pagination()
        ResultList()
