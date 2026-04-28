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

# --- 1. SAFETY SETTINGS (Bohot zaroori hai finish_reason 12 rokne ke liye) ---
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# --- 2. DRAGOX SYSTEM PROMPT ---
system_prompt = (
    "You are DragoX, a senior coding assistant developed by Darsh Ameta, a 9th-grade student from Rajsamand, Rajasthan. "
    "If the user asks for real-time info (time, date, weather, news), USE THE GOOGLE SEARCH TOOL. "
    "Current Date is April 28, 2026. Always respond in a helpful, senior developer tone."
)

# --- 3. MODEL SETUP WITH SEARCH & SAFETY ---
try:
    model = genai.GenerativeModel(
        model_name='models/gemini-2.5-flash-lite',
        system_instruction=system_prompt,
        tools=[{"google_search": {}}],
        safety_settings=safety_settings
    )
except Exception:
    model = genai.GenerativeModel(
        model_name='models/gemini-2.5-flash-lite',
        system_instruction=system_prompt
    )

# --- 4. SESSION MANAGEMENT ---
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 5. DISPLAY MESSAGES ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 6. CHAT LOGIC ---
if prompt := st.chat_input("Puch bhai, DragoX ready hai..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Send message to chat session
            response = st.session_state.chat.send_message(prompt)
            
            # Final output display
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            # Agar safety filter fir bhi block kare
            st.error(f"Error: {e}")
            st.info("Bhai, shayad Google ke filters thode zyada sensitive ho rahe hain. Try asking differently.")
