import os
from google import genai
from google.genai import types
from flask import Flask, Response, Blueprint

model = Blueprint("model", __name__)

@model.route('/generate')
def generate():
    api_key = "AIzaSyAXIdf2HWpXwMPnJyhfvsj7CfbuYhcn" #Remember to use environment variables for api keys.
    client = genai.Client(api_key=api_key)

    files = [
        client.files.upload(file="hand_opt.jpg"),
        client.files.upload(file="uploads/doubt.jpg"),
    ]

    model_name = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",            parts=[
                types.Part.from_uri(
                    file_uri=files[0].uri,
                    mime_type=files[0].mime_type,
                ),
                types.Part.from_text(text="""give me the content of this image"""),
            ],
        ),
        types.Content(
            role="model",
            parts=[
                types.Part.from_text(
                    text="""Here's the content of the image:\n\n**Problem:**\n\nFind the range/null spaces and nullity of T & verify the rank-nullity theorem for T: V3(R) → V4(R), defined by:\n\n* T(e₁) = (0, 1, 0, 2)\n* T(e₂) = (0, 1, 1, 0)\n* T(e₃) = (0, 1, -1, 4)""",
                ),
            ],
        ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_uri(
                    file_uri=files[1].uri,
                    mime_type=files[1].mime_type,
                ),
                types.Part.from_text(text="""solve this mathematical problem"""),  # Changed the prompt to ask for solving
            ],
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_mime_type="text/plain",
    )

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=contents,
            config=generate_content_config,
        )
        # Post-processing: Delete the uploaded image "doubt.jpg"
        try:
            os.remove("uploads/doubt.jpg")
            print("doubt.jpg deleted successfully.")
        except FileNotFoundError:
            print("doubt.jpg not found.")
        except Exception as delete_error:
            print(f"Error deleting doubt.jpg: {delete_error}")

        return response.text
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return f"An error occurred: {e}"
