import io
from typing import Set
import streamlit as st
import google.generativeai as genai
import google.ai.generativelanguage as glm
import PIL.Image
import urllib.request
from PIL import Image

import os
from dotenv import load_dotenv
import pathlib
import textwrap
# from IPython.display import display
# from IPython.display import Markdown
import pandas as pd
import matplotlib.pyplot as plt

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
print("ushakiz 111111")

load_dotenv()
genai.configure( api_key = os.environ["GOOGLE_API_KEY"] )
model = genai.GenerativeModel('gemini-pro-vision')

async def get_response(prompt, model="gemini-pro-vision"):
    
    print("messages", prompt);
    res = await model.generate_content(messages, stream=False,
                                safety_settings={'HARASSMENT':'block_none'})
    # res.resolve()
    return res

def risk_calc(risk_type):
    score=0
    return score

if "messages" not in st.session_state:
    st.session_state["messages"] = []
messages = st.session_state["messages"]
if messages :
    for item in messages:
        role, parts = item.values()
        if role == "user":
            st.chat_message("user").markdown(parts[0])
        elif role == "model":
            st.chat_message("assistant").markdown(parts[0])
print("ushakiz ====")
st.title("Welcome to Green Risks")
st.text("Please fill out the form")
chat_message = st.chat_input("Click the button or type enter here. Calculate my carbon footprint. Calculate my green score and give me recommendations to reduce my carbon footprint")

#TEST TEST
prompt = f"Given the following picture:\n" \
        f" Please assess the risks. "
urllib.request.urlretrieve(
    'https://media.istockphoto.com/id/470984370/photo/forest-fire.jpg?s=612x612&w=0&k=20&c=ZEQKDtmNTfUrS5ldiygfvdJDJ2yD_l7ksu-hJCtPvKg=',
   )
image = PIL.Image.open('fire1.jpeg')
model = genai.GenerativeModel("gemini-pro-vision")
# def to_markdown(text):
#     text = text.replace("•", "  *")
#     return Markdown(textwrap.indent(text, "> ", predicate=lambda _: True))
response = model.generate_content(image)
print(response.text)


# import vertexai

# from vertexai.generative_models import GenerativeModel, Part

# TODO(developer): Update and un-comment below line
# project_id = "PROJECT_ID"

# vertexai.init(project=project_id, location="us-central1")

# model = GenerativeModel(model_name="gemini-1.5-flash-001")

# image_file = Part.from_uri(
#     "gs://cloud-samples-data/generative-ai/image/scones.jpg", "image/jpeg"
# )

# Query the model
# response = model.generate_content([image_file, "what is this image?"])
# print(response.text)
#TEST TEST
risk_type="fire"
risk_score = risk_calc(risk_type)
risk_score_message = "Your risk score is "+str(risk_score)+"."
if (risk_score > 50):
    risk_score = "Please check the risk report attached."
if st.button("GET MY RISKSCORE")  or st.chat_message:
    st.chat_message("user").markdown(chat_message)
    res_area = st.chat_message("assistant").empty()
    messages.append(
        {"role": "user", "parts":  ["Show me my risk score"]},
    )
    # res = model.generate_content(prompt, stream=True,
    #                             safety_settings={'HARASSMENT':'block_none'})
    # res.resolve()


    res = get_response(prompt)
    res_text='Your risk is '+str(risk_score)+". "+risk_score_message+". "
    # for chunk in res:
    #     if chunk:
    #       res_text += chunk.parts[0].text
    # res_text += res
    # res_area.markdown(res_text)
    # messages.append({"role": "model", "parts": [res_text]})
