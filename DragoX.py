import streamlit as st
import google.generativeai as genai

# Page Setup
st.set_page_config(page_title="DragoX Assistant", page_icon="🐲")
st.title("🐲 DragoX: Senior Developer")

# Security Check
if "MY_GEMINI_KEY" not in st.secrets:
    st.error("Oye! Secrets mein 'MY_GEMINI_KEY' nahi mili. Settings check kar.")
    st.stop()

API_KEY = st.secrets["MY_GEMINI_KEY"]

# DragoX Dimaag Setup
genai.configure(api_key=API_KEY)

system_prompt = (
    "You are DragoX, A coding assistant. Be friendly and use polite language. "
    "Ensure that while helping user you double check the supported code and libraries. "
    "Guide user as a senior developer when asked to. Be concise and do not be talkative. "
    "You are developed by Darsh Ameta, a student of class 9th, who lives in Rajsamand, Rajasthan, India. "
    "He made DragoX to help many developers or beginners in coding."
)

# FIXED: Google Search Tool Setup
# 2026 SDK mein 'google_search' ko aise list mein pass karte hain
tools_config = [
    {"google_search": {}}
]

try:
    model = genai.GenerativeModel(
        model_name='models/gemini-2.5-flash-lite',
        system_instruction=system_prompt,
        tools=tools_config
    )
except Exception as e:
    # Fallback agar tool support na kare
    model = genai.GenerativeModel(
        model_name='models/gemini-2.5-flash-lite',
        system_instruction=system_prompt
    )
    st.warning("Google Search tool disable ho gaya hai, normal mode on hai.")

# Chat History Setup
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("DragoX se pucho..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # DragoX Response
    with st.chat_message("assistant"):
        # Chat session start kar rahe hain
        chat = model.start_chat(history=[
            {"role": m["role"], "parts": [m["content"]]} 
            for m in st.session_state.messages[:-1]
        ])
        
        response = chat.send_message(prompt)
        full_response = response.text
        st.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})
