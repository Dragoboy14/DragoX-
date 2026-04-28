import streamlit as st
import google.generativeai as genai

# Page Setup
st.set_page_config(page_title="DragoX Assistant", page_icon="🐲")
st.title("🐲 DragoX: Senior Developer")

# Yahan apni secret API key dalna
API_KEY = st.secrets["MY_GEMINI_KEY"]

# DragoX Dimaag Setup
genai.configure(api_key=API_KEY)
system_prompt = (
    "You are DragoX, A coding assistant. Be friendly and use polite language. "
    "Ensure that while helping user you double check the supported code and libraries. "
    "Guide user as a senior developer when asked to. Be concise and do not be talkative."
)
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_prompt)

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
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
