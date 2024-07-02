import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import pathlib
import textwrap

from vertexai.generative_models import GenerativeModel, Image

import PIL.Image


def load_api_key():
  """Loads the Google API key from a .env file."""
  load_dotenv()
  return os.environ["GOOGLE_API_KEY"]


def main():
  """Main function for the Streamlit app."""
  st.title("Image Text Generation App")

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
            The description should also contain whether there is fire in the image, if yes is it safe or unsafe fire.
            """

    
    contents = [img, prompt]

    # Text generation
    try:
      model = genai.GenerativeModel(model_name)
      response = model.generate_content(contents)
      st.write("Generated Text:")
      st.write(response.text)  # Directly display the text using Streamlit
    except Exception as e:
      st.error(f"Error: During generation. {e}")


if __name__ == "__main__":
  main()

