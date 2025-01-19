import reflex as rx
import asyncio
from ..backend.backend import UploadState

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
            max_files=1,
        ),
        rx.hstack(
            rx.foreach(
                rx.selected_files(id), rx.text
            )
        ),
        rx.hstack(
            rx.button(
                "Upload",
                on_click=[
                    UploadState.handle_upload(rx.upload_files(upload_id=id)),
                    rx.clear_selected_files(id),
                ]
            ),
            rx.button(
                "Clear",
                on_click=rx.clear_selected_files(id),
            ),
        ),
        # rx.cond(
        #     UploadState.toast_message,  # Check if there's a message to show
        #     rx.toast(
        #         UploadState.toast_message,
        #         position="bottom-right",
        #         style={
        #             "background-color": rx.cond(
        #                 UploadState.upload_success, "green", "red"
        #             ),
        #             "color": "white",
        #             "border": "1px solid",
        #             "border-radius": "0.53em",
        #         },
        #     ),
        #     rx.text(""),
        padding="5em",
    )



# rx.cond(
#     UploadState.upload_success,
#     rx.toast(
#         UploadState.toast_message,
#         position="bottom-right",
#         style={
#                 "background-color": "green",
#                 "color": "white",
#                 "border": "1px solid green",
#                 "border-radius": "0.53m",
#         }
#     ),
#     rx.toast(
#         UploadState.toast_message,
#         position="bottom-right",
#         style={
#             "background-color": "red",
#             "color": "white",
#             "border": "1px solid red",
#             "border-radius": "0.53m",
#         },
#     ),
# )