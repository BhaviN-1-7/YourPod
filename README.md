# YourPod: Streamlit Script Generator with gTTS & Groq Llama 3

YourPod is a free, locally-runnable Streamlit web app that generates scripts from text or PDF input using Groq Llama 3 (via the Groq API) and converts them to audio using Google Text-to-Speech (gTTS). It supports podcast-style, summary, and detailed explanation output, and can generate podcast audio with two distinct voices.

---

## Features
- **Input:**
  - Text area for manual entry
  - PDF upload and automatic text extraction
- **Output Styles:**
  - Podcast-style discussion (two hosts, two accents)
  - Summary
  - Detailed explanation
- **Script Generation:**
  - Uses Groq Llama 3 via the Groq API
- **Audio Generation:**
  - Uses gTTS (Google Text-to-Speech)
  - Podcast mode alternates two female host names ("Alice" and "Sophie") and two English accents (US/UK)
  - Humanizes script for more natural speech
- **Downloadable Audio:**
  - Download generated MP3 files
- **Secure API Key Handling:**
  - API key is stored in `config_secret.py` (not tracked by git)

---

## Setup

1. **Clone the repo:**
   ```sh
   git clone https://github.com/BhaviN-1-7/YourPod.git
   cd YourPod
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Add your Groq API key:**
   - Create a file called `config_secret.py` in the project root:
     ```python
     GROQ_API_KEY = "your-groq-api-key-here"
     ```
   - **Do not commit this file to git!**

5. **Run the app:**
   ```sh
   streamlit run script_generator_app.py
   ```

---

## Usage
1. Enter text or upload a PDF.
2. Select the output style (Podcast, Summary, Detailed Explanation).
3. Click "Generate Script".
4. Review the generated script.
5. Click the audio button to generate and play/download the MP3.

---

## Deployment
- **Local:** Works out of the box as long as you have internet access (for gTTS and Groq API).
- **Streamlit Community Cloud:**
  - gTTS may not work reliably due to outbound network restrictions.
  - For public deployment, consider using a cloud TTS API (e.g., ElevenLabs, PlayHT, Azure).
- **Cloud VM:** Works if the server has internet access.

---

## Security
- **Never commit your API keys to git.**
- `config_secret.py` is in `.gitignore` and should be created manually on each deployment.

---

## Credits
- [Streamlit](https://streamlit.io/)
- [gTTS](https://pypi.org/project/gTTS/)
- [Groq Llama 3](https://groq.com/)
- [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/)
- [pydub](https://github.com/jiaaro/pydub)

---

## License
MIT License 