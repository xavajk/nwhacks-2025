# from pydantic_ai import Agent
# from pydantic_ai.models.vertexai import VertexAIModel

# model = VertexAIModel(
#     model_name='gemini-1.5-pro',
#     service_account_file='/Users/xava/Documents/nwhacks-2025/nwhacks-2025-448222-2e7b9e5e693f.json',
#     project_id='nwhacks-2025-448222',
#     region='us-west1',
#     model_publisher='google'
# )

# agent = Agent(model)
# result = agent.run_sync()
# print(result.data)

from google import genai
from google.genai import types
import base64

from google.cloud import storage


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client(project='nwhacks-2025-448222')
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Optional: set a generation-match precondition to avoid potential race conditions
    # and data corruptions. The request to upload is aborted if the object's
    # generation number does not match your precondition. For a destination
    # object that does not yet exist, set the if_generation_match precondition to 0.
    # If the destination object already exists in your bucket, set instead a
    # generation-match precondition using its generation number.
    generation_match_precondition = 0

    blob.upload_from_filename(source_file_name, if_generation_match=generation_match_precondition)

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )

# upload_blob('nwhacks-2025-recordings', '/Users/xava/Documents/nwhacks-2025/recordings/test.mp3', 'test-blob.mp3')

def generate():
    client = genai.Client(
        vertexai=True,
        project="nwhacks-2025-448222",
        location="us-central1"
    )

    audio1 = types.Part.from_uri(file_uri='gs://nwhacks-2025-recordings/test-blob.mp3', mime_type="audio/mp3")

    model = "gemini-2.0-flash-exp"
    contents = [
        types.Content(
        role="user",
        parts=[
            audio1,
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

    res = []
    for chunk in client.models.generate_content_stream(
        model = model,
        contents = contents,
        config = generate_content_config,
        ):
        res.append(chunk)

    return res

res = generate()
print(res)

out = ''
for r in res:
    for cs in r.candidates:
        for ps in cs.content.parts:
            out += ps.text
print(out)