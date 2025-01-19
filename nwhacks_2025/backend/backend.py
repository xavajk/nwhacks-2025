import reflex as rx
import asyncio
import typing
from google.cloud import storage


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client(project='nwhacks-2025-448222')
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    generation_match_precondition = 0
    blob.upload_from_filename(source_file_name, if_generation_match=generation_match_precondition)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

def check_if_blob_in_storage(bucket_name, file_to_check):
    """Checks if a given blob already exists in storage."""
    storage_client = storage.Client(project='nwhacks-2025-448222')
    bucket = storage_client.bucket(bucket_name)
    return storage.Blob(bucket=bucket, name=file_to_check).exists(storage_client)

class UploadState(rx.State):
    """The uploading state."""

    # The images to show.
    audio_files: list[str] = []
    upload_success: bool = False
    toast_message: str = ""

    def on_mount(self):
        """Reset state variables when the state is initialized or remounted."""
        self.upload_success = False
        self.audio_files = []
        self.toast_message = ""

    @rx.event
    async def wait_to_render(self, time: int | float):
        await asyncio.sleep(time)
        self.toast_message = ""

    @rx.event
    async def handle_upload(
        self, files: list[rx.UploadFile]
    ):
        """Handle the upload of file(s).

        Args:
            files: The uploaded files.
        """
        for file in files:
            # check if filename is already in use
            if check_if_blob_in_storage('nwhacks-2025-recordings', file.filename): 
                self.toast_message = "File already uploaded!"
                self.upload_success = False
                print('File already uploaded!')
                yield rx.toast(
                    self.toast_message,
                    style={
                        "background-color": "red",
                        "color": "white",
                        "border": "1px solid red",
                        "border-radius": "0.53em",
                    }
                )
            else:
                self.toast_message = "File uploaded successfully!"
                try:
                    # save the file locally
                    outfile = rx.get_upload_dir() / file.filename
                    with open(outfile, "wb") as f:
                        f.write(file.file.read())

                    # upload the file to GCP storage
                    print(self.upload_success)
                    upload_blob('nwhacks-2025-recordings', f'uploaded_files/{file.filename}', file.filename)
                    print(self.upload_success)

                    # Add the file to the list of uploaded files and show the toast notification.
                    self.audio_files.append(file.filename)
                    print(self.upload_success)
                    yield rx.toast(
                        self.toast_message,
                        style={
                            "background-color": "green",
                            "color": "white",
                            "border": "1px solid green",
                            "border-radius": "0.53em",
                        }
                    )

                except Exception as e:
                    self.toast_message = "Could not upload file." # set the error message
                    self.upload_success = False
                    print(f"Upload failed: {e}")
                    yield rx.toast(
                        self.toast_message,
                        style={
                            "background-color": "red",
                            "color": "white",
                            "border": "1px solid red",
                            "border-radius": "0.53em",
                        }
                    )

class IdeaObject(rx.Base):
    title: str
    body: str
    tags: list(str)