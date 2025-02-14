import google.generativeai as genai
import os
from kokoro import KPipeline
import soundfile as sf
import streamlit as st

genai.configure(api_key=st.secrets['GEMINI_API_KEY'])


model = genai.GenerativeModel('gemini-1.5-flash')
pipeline = KPipeline(lang_code='a')
chat = model.start_chat()

prompt = """
You are a helpful agent for your user. You listen to the audio file of your user speaking. You listen to it carefully and generate reponses to help them.
Sometimes they may simply have a conversation with you, sometime they may tell you tasks to do. Your task it to interpret what they said, and generate the responses to meet their needs.
GENERATE THE RESPONSE ONLY!
"""


def send_chat(turn):
    print("Generating.....")
    audio_file = genai.upload_file(
        path=f"audio-{turn}.wav"
    )
    response = chat.send_message([prompt, audio_file])
    for chunk in response:
        print("Speaking.....")
        print(chunk.text, end='')
        generator = pipeline(
            chunk.text,
            voice='af_heart',
            speed=1,
            split_pattern=r'\n+'
        )
        for i, (gs, ps, audio) in enumerate(generator):
            sf.write(f'agent-{turn}.wav', audio, 24000)
