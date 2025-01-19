import reflex as rx

def navbar_link(text: str, url: str) -> rx.Component:
    return rx.link(
        rx.text(text, size="4", weight="regular"), href=url
    )

def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.icon('brain-circuit'),
                rx.heading(
                    "MindFlow", size="7", weight="bold"
                ),
                align_items="center",
                justify="start",
                width='10em'
            ),
            rx.hstack(
                navbar_link("capture", "/capture"),
                navbar_link("explore", "/explore"),
                navbar_link("create", "/create"),
                justify="center",
                spacing="9",
            ),
            rx.hstack(
                rx.color_mode.button(size='3'),
                justify="end",
                width='10em'
            ),
            align_items="center",
            justify="between",
            padding_bottom="1.5em",
        ),
        rx.divider(),
        width="100%",
    )