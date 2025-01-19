import reflex as rx
# from .components.stats_cards import stats_cards_group
from .components.upload import upload_audio
from .views.navbar import navbar
# from .views.table import main_table

def index() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.flex(
            upload_audio('voice-memo'),
            rx.button(
                "Record"
            ),
            spacing="3",
        ),
        width="100%",
        spacing="6",
        padding_x=["1.5em", "1.5em", "3em"],
    )


app = rx.App(
    theme=rx.theme(
        appearance="light", has_background=True, radius="large", accent_color="iris"
    ),
)

app.add_page(
    index,
    title="FreeFlow",
    description="Let your ideas flow...",
)
