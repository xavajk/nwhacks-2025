import reflex as rx
from .pages.capture import capture
from .components.navbar import navbar
from .backend.backend import AppState

def index() -> rx.Component:
    return capture()


app = rx.App(
    theme=rx.theme(
        appearance="light", has_background=True, radius="large", accent_color="iris"
    ),
)

app.add_page(
    index,
    title="MindFlow",
    description="Let your ideas flow...",
)
