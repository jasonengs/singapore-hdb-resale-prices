from dash import Dash

from dashboard.callbacks import register_callbacks
from dashboard.layout import create_layout
from dashboard.viz.theme import FONT_AWESOME_KIT


def create_app() -> Dash:
    app = Dash(
        __name__,
        external_scripts=[
            {
                "src": f"https://kit.fontawesome.com/{FONT_AWESOME_KIT}.js",
                "crossorigin": "anonymous",
            }
        ],
    )

    app.layout = create_layout()

    register_callbacks()

    return app
