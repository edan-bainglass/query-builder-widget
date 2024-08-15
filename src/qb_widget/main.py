from __future__ import annotations

from solara import Route

from qb_widget.app import App

routes = [
    Route("/", component=App),
]
