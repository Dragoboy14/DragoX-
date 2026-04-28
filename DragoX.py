import streamlit as st
import google.generativeai as genai

# --- 1. Page Setup ---
st.set_page_config(page_title="DragoX Assistant", page_icon="🐲")
st.title("🐲 DragoX: Senior Developer")

# --- 2. Security Check ---
if "MY_GEMINI_KEY" not in st.secrets:
    st.error("Oye! Secrets mein 'MY_GEMINI_KEY' nahi mili. Settings check kar.")
    st.stop()

API_KEY = st.secrets["MY_GEMINI_KEY"]
genai.configure(api_key=API_KEY)

# --- 3. System Prompt ---
system_prompt = (
    "You are DragoX, A coding assistant. Be friendly and use polite language. "
    "Guide user as a senior developer. Be concise. "
    "Developed by Darsh Ameta, a class 9th student from Rajsamand, Rajasthan."
)

# --- 4. Google Search Tool Setup (The Fixed Part) ---
# 2026 mein tools ko simple list of strings ya specific dict mein dena hota hai
tools_config = [{'google_search': {}}]

try:
    model = genai.GenerativeModel(
        model_name='models/gemini-2.5-flash-lite',
        system_instruction=system_prompt,
        tools=tools_config
    )
except Exception:
    # Agar search tool support nahi kar raha, toh bina tool ke load karo
    model = genai.GenerativeModel(
        model_name='models/gemini-2.5-flash-lite',
        system_instruction=system_prompt
    )

# --- 5. Chat Session Setup ---
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 6. Display Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 7. User Input & Response ---
if prompt := st.chat_input("DragoX se pucho..."):
    # User message display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant"):
        try:
            response = st.session_state.chat_session.send_message(prompt)
            full_response = response.text
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Bhai error aa gaya: {e}")
