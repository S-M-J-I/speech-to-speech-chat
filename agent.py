import google.generativeai as genai
import os
import audio_utils
from kokoro import KPipeline
import soundfile as sf

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))


model = genai.GenerativeModel('gemini-1.5-flash')
pipeline = KPipeline(lang_code='a')

prompt = """
You are a helpful agent for your user. You listen to the audio file of your user speaking. You listen to it carefully and generate reponses to help them.
Sometimes they may simply have a conversation with you, sometime they may tell you tasks to do. Your task it to interpret what they said, and generate the responses to meet their needs.
GENERATE THE RESPONSE ONLY!
"""


chat = model.start_chat()
while True:
    print("Listening.....")
    audio_utils.record_to_file("audio.wav")
    audio_file = genai.upload_file(
        path="audio.wav"
    )
    print("Generating.....")
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
            sf.write(f'agent-{i}.wav', audio, 24000)
            audio_utils.play_audio(f'agent-{i}.wav')
