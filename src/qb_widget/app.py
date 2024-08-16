from __future__ import annotations

from pathlib import Path

from solara import Head, Style, Title, VBox
from solara.core import component
from solara.lab import Tab, Tabs

from qb_widget.components import HelpPanel, InfoPanel, QueryPanel


@component
def App():
    """Main page component."""
    with VBox(classes=["container"]):
        with Head():
            Title("AiiDA Query Builder App")
            Style(Path(__file__).parent / "app.css")
        InfoPanel()
        with Tabs():
            with Tab("Query"):
                QueryPanel()
            with Tab("Help"):
                HelpPanel()
