import streamlit as st
import audio_utils
import agent

st.set_page_config(page_title="Voice Chat", layout="centered")

st.title("🎙️ Voice Chat with AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "turn" not in st.session_state:
    st.session_state.turn = 0

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["type"] == "text":
            st.write(msg["content"])
        elif msg["type"] == "audio":
            st.audio(msg["content"], format="audio/wav")


st.write("**Speak to send a message:**")
audio_input = st.button("🎤 Record")

if audio_input:
    st.toast("Recording... (simulate capturing audio)")
    audio_utils.record_to_file(f"audio-{st.session_state.turn}.wav")
    user_audio = f"audio-{st.session_state.turn}.wav"
    st.session_state.messages.append(
        {"role": "user", "type": "audio", "content": user_audio})
    st.rerun()

if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    agent.send_chat(st.session_state.turn)
    ai_audio = f"agent-{st.session_state.turn}.wav"
    st.session_state.messages.append(
        {"role": "assistant", "type": "audio", "content": ai_audio})
    st.session_state.__setitem__("turn", st.session_state.turn + 1)
    print("end:", st.session_state.get("turn"))
    st.rerun()
