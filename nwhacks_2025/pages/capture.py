import reflex as rx
from ..components.upload import upload_audio
from ..components.navbar import navbar

def capture_view():
    return rx.box(
        rx.vstack(
            rx.box(
                rx.heading("Let your mind flow...", weight="bold", size="9")
            ),
            upload_audio('voice-memo'),
            align="center",
            justify="center",
            height="100%"
        ),
        width="100%",
        height="100%",
        background_color="#C8D9E6",
        border_radius="14px",
        align="center"
    )

@rx.page(route='/capture')
def capture():
    return rx.vstack(
            navbar(),
            capture_view(),
            width="100vw",
            height="100vh",
            spacing="6",
            padding="1.5em",
            justify="center",
            align="stretch"
        )