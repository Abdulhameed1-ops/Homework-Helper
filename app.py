import streamlit as st
import requests
from PIL import Image

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Homework Helper AI",
    page_icon="📘",
    layout="centered"
)

# ================= API KEYS =================
import os

OCR_API_KEY = st.secrets["OCR_API_KEY"]
COHERE_API_KEY = st.secrets["COHERE_API_KEY"]
# ================= CUSTOM CSS =================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #eef3ff, #ffffff);
    font-family: "Segoe UI", sans-serif;
}

h1 {
    text-align: center;
    color: #1e40af;
}

h3 {
    text-align: center;
    color: #2563eb;
}

.card {
    background: white;
    padding: 1.6em;
    border-radius: 22px;
    box-shadow: 0 18px 35px rgba(0,0,0,0.08);
    margin-top: 1.2em;
}

.stButton button {
    width: 100%;
    background: #2563eb;
    color: white;
    border-radius: 14px;
    padding: 0.7em;
    font-size: 17px;
    border: none;
}

.stTextArea textarea {
    border-radius: 14px;
}

footer {
    text-align: center;
    color: gray;
    margin-top: 1em;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ================= FUNCTIONS =================

def extract_text_from_image(image_file):
    """Uses OCR.Space API to extract text from image"""
    url = "https://api.ocr.space/parse/image"
    payload = {
        "apikey": OCR_API_KEY,
        "language": "eng",
        "isOverlayRequired": False
    }
    files = {
        "file": image_file
    }

    response = requests.post(url, data=payload, files=files)
    result = response.json()

    try:
        return result["ParsedResults"][0]["ParsedText"]
    except:
        return ""

def explain_homework_with_ai(text):
    """Uses Cohere REST API to explain homework"""
    url = "https://api.cohere.ai/v1/generate"

    headers = {
        "Authorization": f"Bearer {COHERE_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are a friendly school tutor.
Explain the homework below step-by-step in very simple language.
Make it easy for a student to understand.

Homework:
{text}
"""

    data = {
        "model": "command-a-03-2025",
        "prompt": prompt,
        "max_tokens": 450,
        "temperature": 0.4
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    try:
        return result["generations"][0]["text"]
    except:
        return "Sorry, the AI could not generate an explanation."

# ================= UI =================

st.markdown("<h1>📘 Homework Helper AI</h1>", unsafe_allow_html=True)
st.markdown("<h3>Take a photo of your homework and get help instantly</h3>", unsafe_allow_html=True)

st.markdown("<div class='card'>", unsafe_allow_html=True)

uploaded_image = st.file_uploader(
    "📸 Upload or take a picture of your homework",
    type=["jpg", "jpeg", "png"]
)

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Homework Image", use_container_width=True)

    if st.button("🧠 Read & Explain Homework"):
        with st.spinner("📖 Reading homework..."):
            extracted_text = extract_text_from_image(uploaded_image)

        st.markdown("### ✏️ Extracted Text")
        st.text_area("", extracted_text, height=160)

        if extracted_text.strip():
            with st.spinner("🤖 AI is explaining..."):
                explanation = explain_homework_with_ai(extracted_text)

            st.markdown("### 📘 Explanation")
            st.success(explanation)
        else:
            st.error("❌ Could not read the text. Try a clearer image.")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<footer>
Made for students • Smart learning • Clean & safe
</footer>
""", unsafe_allow_html=True)
