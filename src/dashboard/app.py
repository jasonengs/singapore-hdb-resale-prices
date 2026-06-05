from dash import Dash

from dashboard.callbacks import register_callbacks
from dashboard.layout import create_layout


def create_app() -> Dash:
    app = Dash(
        __name__,
        external_stylesheets=[
            "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.1/css/all.min.css"
        ],
    )

    app.title = "Singapore HDB Resale Explorer"

    app.layout = create_layout()

    register_callbacks()

    return app


app = create_app()
server = app.server
