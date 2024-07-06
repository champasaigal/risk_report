import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from google.cloud import aiplatform
import pathlib
import textwrap

from vertexai.generative_models import GenerativeModel, Image

import PIL.Image
import re
import requests


def load_api_key():
  """Loads the Google API key from a .env file."""
  load_dotenv()
  return os.environ["GOOGLE_API_KEY"]


def main():
  """Main function for the Streamlit app."""
  st.title("FireGuard - Introducing FireGuard: Your Ultimate Fire Risk Detection Solution \n In an age where fire safety is paramount, FireGuard leverages advanced image processing technology to scan and detect fire risks from both house cameras and outdoor drones. Whether you’re monitoring your home or surveying vast outdoor spaces, FireGuard provides real-time alerts and insights, ensuring you can take preventative action before disaster strikes. With FireGuard, safeguarding your property from potential fire hazards has never been easier or more efficient.")

  # Load API key
  try:
    api_key = load_api_key()
    genai.configure(api_key=api_key)
  except KeyError:
    st.error("Error: Please set GOOGLE_API_KEY in your .env file")
    return

  # Model selection (potentially add a dropdown for future)
  model_name = "gemini-1.5-flash-001"

  # Image upload
  uploaded_file = st.file_uploader("Choose an Image", type=["jpg", "jpeg", "png"])
  if uploaded_file is not None:
    try:
      img = PIL.Image.open(uploaded_file)
      st.write("Input Image:")
      st.image(img)
    except Exception as e:
      st.error(f"Error: Failed to open image. {e}")
      return
    
    prompt = """
            Provide a description of the image.
            The description should also contain whether there is fire in the image. Is there a risk of fire?
            """

    
    contents = [img, prompt]

    # Text generation
    try:
      model = genai.GenerativeModel(model_name)
      response = model.generate_content(contents)
      st.write("Generated Text:")
      st.write(response.text)  # Directly display the text using Streamlit

      pattern = "There is a \w+ risk"

      match = re.search(pattern, response.text)
      print("fire risk search"+match)

      if (match):
          print("fire risk hellloooooo")
          url = "https://us-central1-inchefs-login-v1.cloudfunctions.net/sendEmailNotification"
          response = requests.get(url)
          # Check if the request was successful (status code 200)
          if response.status_code == 200:
              print(response.text)  # Print the content of the response
          else:
              print("Request failed with status code:", response.status_code)
            #call cloud function
            
    except Exception as e:
      st.error(f"Error: During generation. {e}")


if __name__ == "__main__":
  main()

