import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Model Scanner", page_icon="🔍")
st.title("🔍 DragoX: Model Discovery")

# API Key check
if "MY_GEMINI_KEY" not in st.secrets:
    st.error("Pehle Streamlit Secrets mein 'MY_GEMINI_KEY' daal bhai!")
    st.stop()

genai.configure(api_key=st.secrets["MY_GEMINI_KEY"])

st.info("Tere account ke liye available models dhoond raha hoon...")

try:
    # Google se list maang rahe hain
    available_models = genai.list_models()
    
    found = False
    for m in available_models:
        # Hum wahi models dikhayenge jo 'generateContent' support karte hain
        if 'generateContent' in m.supported_generation_methods:
            st.success(f"Mil gaya! Model Name: `{m.name}`")
            st.write(f"Description: {m.description}")
            st.divider()
            found = True
            
    if not found:
        st.warning("Koi bhi generative model nahi mila. API key check kar.")

except Exception as e:
    st.error(f"Error aa gaya bhai: {e}")
    st.write("Ho sakta hai API Key invalid ho ya permissions na hon.")
