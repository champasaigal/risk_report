import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from google.cloud import aiplatform
from google.cloud import storage
import pathlib
import textwrap
import io

from vertexai.generative_models import GenerativeModel, Image

import PIL.Image
import re
import requests
import json
import google.oauth2.id_token
import google.auth.transport.requests


def load_api_key():
    """Loads the Google API key from a .env file."""
    load_dotenv()
    return os.environ["GOOGLE_API_KEY"]


def get_image_from_gcs(bucket_name, image_name):
    """Fetches an image from Google Cloud Storage."""
    # Specify the path to your service account key file
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"
    
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(image_name)
    img_data = blob.download_as_bytes()
    img = PIL.Image.open(io.BytesIO(img_data))
    return img


def main():
    """Main function for the Streamlit app."""
    st.title("FireGuard - Your Ultimate Fire Risk Detection Solution")

    # Load API key
    try:
        api_key = load_api_key()
        genai.configure(api_key=api_key)
    except KeyError:
        st.error("Error: Please set GOOGLE_API_KEY in your .env file")
        return

    # Model selection (potentially add a dropdown for future)
    model_name = "gemini-1.5-flash-001"

    # Image upload options
    image_source = st.selectbox("Choose image source", ["Upload", "Google Cloud Storage"])

    img = None
    if image_source == "Upload":
        uploaded_file = st.file_uploader("Choose an Image", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            try:
                img = PIL.Image.open(uploaded_file)
                st.write("Input Image:")
                st.image(img)
            except Exception as e:
                st.error(f"Error: Failed to open image. {e}")
                return
    else:
        bucket_name = st.text_input("Enter GCS bucket name")
        image_name = st.text_input("Enter GCS image name")
        if bucket_name and image_name:
            try:
                img = get_image_from_gcs(bucket_name, image_name)
                st.write("Input Image from GCS:")
                st.image(img)
            except Exception as e:
                st.error(f"Error: Failed to load image from GCS. {e}")
                return

    if img:
        prompt = """
        Provide a description of the image.
        The description should also contain whether there is fire in the image. If there is a risk of fire, please say, yes, there is a risk of fire, otherwise say it is safe, don't worry
        """

        contents = [img, prompt]

        # Text generation
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(contents)
            print("Generated Text:" + str(response))
            st.write(response.parts[0].text)  # Directly display the text using Streamlit
            pattern = " is a [a-zA-Z]* risk"
            match1 = re.search(pattern, response.parts[0].text)
            print("match" + str(match1))
            pattern = " is a risk"
            match2 = re.search(pattern, response.parts[0].text)
            print("match" + str(match2))
            if match1 or match2:
                print("fire risk hellloooooo")
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './my_service_account.json'
                request = google.auth.transport.requests.Request()

                audience = 'https://us-central1-inchefs-login-v1.cloudfunctions.net/sendEmailNotification2'
                r = requests.post(
                    audience,
                    headers={},
                )
                print("posted request")
                if r.status_code == 200:
                    st.write(r.text)  # Print the content of the response
                else:
                    print("Request failed with status code:", r.status_code, r.reason)
                    print("Request failed with reason:", r.reason)

        except Exception as e:
            st.error(f"Error: During generation. {e}")


if __name__ == "__main__":
    main()
