from __future__ import annotations

from aiida.manage.configuration import load_profile
from solara import Route

from qb_widget.app import App

_ = load_profile()

routes = [
    Route("/", component=App),
]
