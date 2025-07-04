import streamlit as st
import fitz  # PyMuPDF
import requests
import tempfile
import os
from gtts import gTTS
from pydub import AudioSegment
import re
from config_secret import GROQ_API_KEY

# ========== CONFIGURATION ========== #
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama3-70b-8192"

# ========== HELPER FUNCTIONS ========== #
def extract_text_from_pdf(pdf_file):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            tmp.write(pdf_file.read())
            tmp_path = tmp.name
        doc = fitz.open(tmp_path)
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
        os.remove(tmp_path)
        if not text.strip():
            return None, "No extractable text found in PDF."
        return text, None
    except Exception as e:
        return None, f"PDF extraction error: {e}"

def build_prompt(input_text, output_style):
    if output_style == "Podcast-Style Discussion":
        return (
            "You are two podcast hosts (Host 1: Male, Host 2: Female). "
            "Create a 150-200 word informative, friendly discussion about the following content. "
            "End with a call to action.\n"
            f"Content: {input_text}\n"
            "Format:\nHost 1 (Male): ...\nHost 2 (Female): ...\nHost 1: ...\n"
        )
    elif output_style == "Summary":
        return (
            "Summarize the following content in 50-100 words, focusing on the key points:\n"
            f"Content: {input_text}\n"
        )
    elif output_style == "Detailed Explanation":
        return (
            "Provide a detailed explanation (200-300 words) of the following content, giving in-depth context:\n"
            f"Content: {input_text}\n"
        )
    else:
        return input_text

def generate_script_with_groq(prompt):
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": GROQ_MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 600,
            "temperature": 0.7
        }
        response = requests.post(GROQ_API_URL, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip(), None
    except Exception as e:
        return None, f"Groq API error: {e}"

def split_podcast_script(script):
    lines = script.split('\n')
    result = []
    for line in lines:
        if line.strip().startswith("Host 1"):
            result.append(('male', line.split(":", 1)[-1].strip()))
        elif line.strip().startswith("Host 2"):
            result.append(('female', line.split(":", 1)[-1].strip()))
        elif line.strip():
            result.append(('male', line.strip()))
    return result

def clean_script(script, output_style):
    # Remove introductory phrases like 'Here is a ... about ...:'
    # Remove lines that match 'Here is a ... about ...:' or similar
    lines = script.split('\n')
    cleaned = []
    for line in lines:
        if re.match(r"^Here is (a|an) .* about .*:", line.strip(), re.IGNORECASE):
            continue
        cleaned.append(line)
    return '\n'.join(cleaned).strip()

def humanize_script(text):
    # Add a pause after "Host 1:" and "Host 2:"
    text = re.sub(r'(Host [12]:)', r'\1 ', text)
    # Add commas before conjunctions for better pacing
    text = re.sub(r'([a-z]) (and|but|so|because) ', r'\1, \2 ', text, flags=re.IGNORECASE)
    # Replace some formal phrases with contractions
    text = text.replace("do not", "don't").replace("cannot", "can't").replace("I am", "I'm")
    text = text.replace("I will", "I'll").replace("you are", "you're").replace("we are", "we're")
    text = text.replace("it is", "it's").replace("that is", "that's")
    # Add more periods for shorter sentences
    text = re.sub(r'([a-zA-Z]), ([A-Z])', r'\1. \2', text)
    # Remove double spaces
    text = re.sub(r' +', ' ', text)
    return text

def gtts_tts_to_mp3(text, lang='en', tld='com', speed=1.15):
    temp_mp3 = tempfile.mktemp(suffix='.mp3')
    tts = gTTS(text=text, lang=lang, tld=tld)
    tts.save(temp_mp3)
    if speed != 1.0:
        audio = AudioSegment.from_mp3(temp_mp3)
        new_audio = audio._spawn(audio.raw_data, overrides={"frame_rate": int(audio.frame_rate * speed)})
        new_audio = new_audio.set_frame_rate(audio.frame_rate)
        new_audio.export(temp_mp3, format="mp3")
    return temp_mp3

def generate_podcast_audio_gtts(script):
    segments = []
    temp_files = []
    for i, (gender, text) in enumerate(split_podcast_script(script)):
        tld = 'com' if gender == 'male' else 'co.uk'
        # Use humanized text for each segment
        humanized = humanize_script(text)
        temp_mp3 = gtts_tts_to_mp3(humanized, tld=tld, speed=1.15)
        segments.append(temp_mp3)
        temp_files.append(temp_mp3)
    podcast = AudioSegment.empty()
    for mp3 in segments:
        podcast += AudioSegment.from_mp3(mp3)
    out_mp3 = tempfile.mktemp(suffix="_podcast.mp3")
    podcast.export(out_mp3, format="mp3")
    for f in temp_files:
        os.remove(f)
    return out_mp3

def replace_host_names(text, name1="Alice", name2="Sophie"):
    # Replace 'Host 1' and 'Host 2' with the given names
    text = text.replace("Host 1", name1)
    text = text.replace("Host 2", name2)
    return text

# ========== STREAMLIT UI ========== #
st.set_page_config(page_title="Script Generator", layout="centered")
st.markdown("""
    <style>
    .main {background-color: #f5f7fa;}
    .stTabs [data-baseweb="tab"] {font-size: 18px; font-weight: 600;}
    .stRadio label {font-size: 16px;}
    .stButton button {background-color: #0056b3; color: white; font-weight: bold;}
    </style>
    """, unsafe_allow_html=True)

st.title("Script Generator (Groq Llama 3 + gTTS)")
st.markdown("""
Generate podcast-style scripts, summaries, or detailed explanations from text or PDFs using Groq Llama 3. Generate audio files with gTTS (Google Text-to-Speech).
""")

tabs = st.tabs(["Text Input", "PDF Upload"])
output_style = st.radio(
    "Select Output Style:",
    ("Podcast-Style Discussion", "Summary", "Detailed Explanation"),
    horizontal=True
)

if "script" not in st.session_state:
    st.session_state.script = ""
if "err" not in st.session_state:
    st.session_state.err = ""

input_text = None
input_error = None

with tabs[0]:
    st.subheader("Enter Text")
    user_text = st.text_area("Enter your topic or content:", height=120)
    if st.button("Generate Script", key="text_btn"):
        if not user_text.strip():
            st.session_state.err = "Please enter some text."
            st.session_state.script = ""
        else:
            with st.spinner("Generating script with Groq Llama 3..."):
                prompt = build_prompt(user_text.strip(), output_style)
                script, err = generate_script_with_groq(prompt)
                st.session_state.script = script
                st.session_state.err = err

with tabs[1]:
    st.subheader("Upload PDF")
    pdf_file = st.file_uploader("Upload a PDF file:", type=["pdf"])
    if st.button("Generate Script", key="pdf_btn"):
        if not pdf_file:
            st.session_state.err = "Please upload a PDF file."
            st.session_state.script = ""
        else:
            text, err = extract_text_from_pdf(pdf_file)
            if err:
                st.session_state.err = err
                st.session_state.script = ""
            else:
                with st.spinner("Generating script with Groq Llama 3..."):
                    prompt = build_prompt(text, output_style)
                    script, err = generate_script_with_groq(prompt)
                    st.session_state.script = script
                    st.session_state.err = err

if st.session_state.script:
    cleaned_script = clean_script(st.session_state.script, output_style)
    named_script = replace_host_names(cleaned_script, "Alice", "Sophie")
    humanized_script = humanize_script(named_script)
    st.subheader("Generated Script:")
    st.text_area("Script Output", humanized_script, height=200)
    st.markdown(
        "> **Note:** Using gTTS (Google Text-to-Speech) for audio generation. Requires internet connection."
    )
    st.markdown("**Generate Audio (Powered by gTTS):**")
    if output_style == "Podcast-Style Discussion":
        if st.button("Generate Podcast Audio (Single Voice)"):
            with st.spinner("Generating podcast audio with gTTS..."):
                audio_file = generate_podcast_audio_gtts(humanized_script)
            if audio_file:
                st.success("Audio generated!")
                st.audio(audio_file, format="audio/mp3")
                with open(audio_file, "rb") as f:
                    st.download_button("Download Podcast Audio (MP3)", f, file_name="podcast.mp3", mime="audio/mp3")
            else:
                st.error("gTTS failed to generate audio.")
    else:
        if st.button(f"Generate Audio"):
            with st.spinner("Generating audio with gTTS..."):
                audio_file = gtts_tts_to_mp3(humanized_script)
            if audio_file:
                st.success("Audio generated!")
                st.audio(audio_file, format="audio/mp3")
                with open(audio_file, "rb") as f:
                    st.download_button(f"Download Audio", f, file_name=f"script.mp3", mime="audio/mp3")
            else:
                st.error("gTTS failed to generate audio.")
elif st.session_state.err:
    st.error(st.session_state.err)

st.markdown("""
---
*This tool is part of the DDD College Lost and Found Web App. For image captioning, visit the [Image Captioning page](#).*
""") 