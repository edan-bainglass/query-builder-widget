from solara import Button, HBox, InputText, VBox
from solara import ui_dropdown as Dropdown
from solara.core import component


@component
def NodePanel():
    """Node panel component."""

    with VBox(classes=["border px-3"]):
        with HBox(classes=["align-items-center"]):
            Dropdown(
                "Select node type",
                options=[
                    "Int",
                    "StructureData",
                    "Group",
                ],
                class_="me-3",
            )
            InputText("Tag", classes=["me-3"])
            Button(
                icon_name="mdi-cached",
                color="primary",
            )
