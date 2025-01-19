import reflex as rx
from ..backend.backend import UploadState, AppState

def upload_audio(id: str) -> rx.Component:
    color = "rgb(107,99,246)"
    return rx.vstack(
        rx.upload(
            rx.vstack(
                rx.button(
                    "Select File",
                    color=color,
                    bg="white",
                    border=f"1px solid {color}",
                ),
                rx.text(
                    "Drag and drop files here or click to select files"
                ),
            ),
            id=id,
            border=f"1px dotted {color}",
            padding="2em",
            accept={'audio/mpeg': 'mp3'},
            max_files=3,
        ),
        rx.hstack(
            rx.foreach(
                rx.selected_files(id), rx.text
            )
        ),
        rx.flex(
            rx.button(
                "Upload",
                on_click=[
                    UploadState.handle_upload(rx.upload_files(upload_id=id)),
                    rx.clear_selected_files(id),
                    AppState.add_ideas(UploadState.audio_files)
                ]
            ),
            rx.button(
                "Clear",
                on_click=rx.clear_selected_files(id),
            ),
            spacing='2',
            direction="row",
            align="stretch",
            justify="between"
        ),
        padding="2em",
    )