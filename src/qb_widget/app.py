from __future__ import annotations

from solara import Head, Style, Title, VBox
from solara.core import component
from solara.lab import Tab, Tabs

from qb_widget.assets.styles import css
from qb_widget.components import HelpPanel, InfoPanel, QueryPanel


@component
def App():
    """Main page component."""
    with VBox(classes=["container"]):
        Style(css / "app.css")
        with Head():
            Title("AiiDA Query Builder App")
        InfoPanel()
        with Tabs():
            with Tab("Query"):
                QueryPanel()
            with Tab("Help"):
                HelpPanel()
