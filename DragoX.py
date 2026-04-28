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
    "Guide user as a senior developer when asked to. Be concise and do not be talkative. You are developed by Darsh Ameta. A student of class 9th. Who lives in a cuty named RAJSAMAND in Rajsathan of India. He made DragoX to help many devlopers or beginners in coding."
)

# FIXED MODEL NAME HERE
# DragoX ko Internet ki shakti dene ke liye tools add karo
model = genai.GenerativeModel(
    model_name='models/gemini-2.5-flash-lite',
    system_instruction=system_prompt,
    tools=[{'google_search_queries': {}}]  # Yeh hai asli jaadu!
)

# Chat History Setup
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("DragoX, code likho..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error aa gaya bhai: {e}")
