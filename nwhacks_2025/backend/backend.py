import reflex as rx
import asyncio
import json
from typing import List, Literal
from google.cloud import storage
from google import genai
from google.genai import types
from pydantic import BaseModel, Field


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

class TranscriptToIdeaSchema(BaseModel):
    title: str = Field(description="A short title that describes the content of the transcript.")
    body: str = Field(description="A markdown string that expands on / organizes a raw idea transcript.")
    tags: List[str] = Field(description="1-3 descriptive tags that relate to the content of the idea.")

def generate_transcript(audio_file):
    client = genai.Client(
        vertexai=True,
        project="nwhacks-2025-448222",
        location="us-central1"
    )

    audio = types.Part.from_uri(file_uri=f'gs://nwhacks-2025-recordings/{audio_file}', mime_type="audio/mp3")

    model = "gemini-1.5-pro"
    contents = [
        types.Content(
        role="user",
        parts=[
            audio,
            types.Part.from_text("""Give me a transcript of the accompanying audio file.""")
        ]
        )
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature = 0,
        top_p = 0.95,
        max_output_tokens = 8192,
        response_modalities = ["TEXT"],
        safety_settings = [types.SafetySetting(
        category="HARM_CATEGORY_HATE_SPEECH",
        threshold="OFF"
        ),types.SafetySetting(
        category="HARM_CATEGORY_DANGEROUS_CONTENT",
        threshold="OFF"
        ),types.SafetySetting(
        category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
        threshold="OFF"
        ),types.SafetySetting(
        category="HARM_CATEGORY_HARASSMENT",
        threshold="OFF"
        )],
    )

    res = client.models.generate_content(
        model = model,
        contents = contents,
        config = generate_content_config,
    )

    return res

def convert_generation_to_text(res):
    out = ''
    for r in res:
        for cs in r.candidates:
            for ps in cs.content.parts:
                out += ps.text
    return out

def get_idea_fields(res):
    client = genai.Client(
        vertexai=True,
        project="nwhacks-2025-448222",
        location="us-central1"
    )

    model = "gemini-1.5-pro"
    contents = [
        types.Content(
        role="user",
        parts=[types.Part.from_text(f"""Given the following transcript of an audio file (an brainstorming idea that is meant to be expanded on), output a suggested short title, a markdown page that incorporates and expands on the idea, as well as any categorical tags that may be associated with the proposed idea.\n\nIdea Transcript:\n\n{res}""")]
        )
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature = 0,
        top_p = 0.95,
        max_output_tokens = 8192,
        response_modalities = ["TEXT"],
        safety_settings = [types.SafetySetting(
        category="HARM_CATEGORY_HATE_SPEECH",
        threshold="OFF"
        ),types.SafetySetting(
        category="HARM_CATEGORY_DANGEROUS_CONTENT",
        threshold="OFF"
        ),types.SafetySetting(
        category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
        threshold="OFF"
        ),types.SafetySetting(
        category="HARM_CATEGORY_HARASSMENT",
        threshold="OFF"
        )],
        response_mime_type='application/json',
        response_schema=TranscriptToIdeaSchema.model_json_schema()
    )

    res = client.models.generate_content(
        model = model,
        contents = contents,
        config = generate_content_config,
    )
    return res

class IdeaObject(rx.Base):
    title: str
    body: str
    tags: List[str]

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

class AppState(rx.State):
    ideas: List[IdeaObject] = []

    @rx.event
    async def add_ideas(self, files: List[str]):
        # create audio transcript and add to app state
        for file in files:
            res = generate_transcript(file)
            res = convert_generation_to_text(res)
            fields = get_idea_fields(res).parsed

            print(fields)

            idea = IdeaObject(title=fields['title'], body=fields['body'], tags=fields['tags'])
            self.ideas.append(idea)