import reflex as rx
from ..components.upload import upload_audio
from ..components.navbar import navbar

def explore_view():
    return rx.box(
        rx.vstack(
            rx.grid(
                rx.foreach(
                    rx.Var.range(12),
                    lambda i: rx.card(f"Card {i + 1}", height="10vh"),
                ),
                gap="1rem",
                grid_template_columns=[
                    "1fr",
                    "repeat(2, 1fr)",
                    "repeat(2, 1fr)",
                    "repeat(3, 1fr)",
                    "repeat(4, 1fr)",
                ],
                width="100%",
            ),
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

@rx.page(route='/explore')
def explore():
    return rx.vstack(
            navbar(),
            explore_view(),
            width="100vw",
            height="100vh",
            spacing="6",
            padding="1.5em",
            justify="center",
            align="stretch"
        )