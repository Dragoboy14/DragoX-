import streamlit as st
import google.generativeai as genai

# Page Setup
st.set_page_config(page_title="DragoX Assistant", page_icon="🐲")
st.title("🐲 DragoX: Senior Developer")

# Security Check
if "MY_GEMINI_KEY" not in st.secrets:
    st.error("Oye! Secrets mein 'MY_GEMINI_KEY' nahi mili.")
    st.stop()

genai.configure(api_key=st.secrets["MY_GEMINI_KEY"])

# --- DRAGOX KA NAYA BRAINWASHING PROMPT ---
system_prompt = (
    "You are DragoX, a senior coding assistant developed by Darsh Ameta who is a 9th class student living in Rajsamand city of Rajasthan."
    "CRITICAL: If the user asks for real-time information like current time, date, weather, or news, "
    "YOU MUST USE THE GOOGLE SEARCH TOOL. Do not say you are an AI with no live access. "
    "Always provide the current IST time if asked."
)

# --- GOOGLE SEARCH TOOL ENABLE ---
tools_config = [{"google_search": {}}]

try:
    model = genai.GenerativeModel(
        model_name='models/gemini-2.5-flash-lite',
        system_instruction=system_prompt,
        tools=tools_config
    )
except:
    model = genai.GenerativeModel(
        model_name='models/gemini-2.5-flash-lite',
        system_instruction=system_prompt
    )

# Session state check
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
if prompt := st.chat_input("Puch bhai..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # DragoX ab search marega kyunki prompt mein force kiya hai
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
