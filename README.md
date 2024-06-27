# Google AI Chat - Streamlit App


## Overview

Google AI Chat is an AI-powered chat application built with Streamlit and Python. This application allows you to interact with Google AI language generation models, specifically based on the models **gemini-pro** and **gemini-pro-vision**. It is capable of answering questions, describing images, reading text and table files, generating graphs with Graphviz, and much more.

![Google AI Chat](https://seeklogo.com/images/G/google-ai-logo-996E85F6FD-seeklogo.com.png)

[Streamlit App](https://sergiolm-ai.streamlit.app/)
1. pip install `requirements.txt`.
     ``` bash
     pip install -r requirements.txt
     ``` 

2. add key to .env
     ```
     GOOGLE_API_KEY=###
     ```

3. Let's try deploying it locally. 
     ``` bash
     streamlit run app.py
     ```

4. Let's build the Docker image. We'll tag our image as `llm-app` using the `-t` parameter. The `.` at the end means we want all of the files in our current directory to be added to our image.
     
     ``` bash
     docker build -t llm-app .
     ```
You'll see a number of steps - each of those steps corresponds to an item outlined in our `Dockerfile` and the build process. 

If you'd like to learn more - check out this resource by Docker: [build](https://docs.docker.com/engine/reference/commandline/build/)

2. Run and test the Docker image locally using the `run` command. The `-p`parameter connects our **host port #** to the left of the `:` to our **container port #** on the right.
    
     ``` bash
     docker run -p 7860:7860 llm-app
     ```

3. Visit http://localhost:8501


2. Setup your huggingface space as shown below:
   
- Owner: Your username
- Space Name: `llm-app`
- License: `Openrail`
- Select the Space SDK: `Docker`
- Docker Template: `Blank`
- Space Hardware: `CPU basic - 2 vCPU - 16 GB - Free`
- Repo type: `Public`

<p align = "center" draggable=”false”>
<img src="https://github.com/AI-Maker-Space/LLMOps-Dev-101/assets/37101144/8f16afd1-6b46-4d9f-b642-8fefe355c5c9"> 
</p>

3. You should see something like this. We're now ready to send our files to our Huggingface Space. After cloning, move your files to this repo and push it along with your docker file. You DO NOT need to create a Dockerfile. Make sure NOT TO push your `.env` file. This should automatically be ignored.

4. After pushing all files, navigate to the settings in the top right to add your Google API key.


5. Scroll down to `Variables and secrets` and click on `New secret` on the top right.


6. Set the name to `GOOGLE_API_KEY` and add your  key under `Value`. Click save.

7. To ensure your key is being used, we recommend you `Restart this Space`.


