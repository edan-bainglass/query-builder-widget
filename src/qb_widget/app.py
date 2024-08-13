from pathlib import Path

from solara import Head, Style, Title, VBox
from solara.core import component
from solara.lab import Tab, Tabs

from qb_widget.components import HelpPanel, QueryPanel


@component
def App():
    """Main page component."""

    with VBox() as app:
        with Head():
            Title("AiiDA Query Builder App")
            Style(Path(__file__).parent / "app.css")
        with Tabs():
            with Tab("Query"):
                QueryPanel()
            with Tab("Help"):
                HelpPanel()

    return app
