# Podcast Generator & Image Captioning Suite

A modern Streamlit app for generating podcast-style scripts (with Groq Llama 3) and creating funny, sarcastic, or story-based captions for images using the BLIP model—all with a beautiful, easy-to-use interface.

---

## Features
- **Podcast Script Generator:**
  - Enter text or upload a PDF to generate:
    - Podcast-style discussion (alternating hosts)
    - Summary
    - Detailed explanation
  - Uses Groq Llama 3 via the Groq API
  - Converts scripts to audio with gTTS (Google Text-to-Speech)
  - Downloadable MP3 output
- **Image Captioning:**
  - Upload an image and generate a caption or creative story
  - BLIP model runs locally (no Hugging Face API key required)
  - Option for funny/sarcastic or creative story output (uses Groq for style)
  - Captions/stories are displayed in a visually appealing box
- **Modern UI:**
  - Large, bold tab navigation for easy switching between features
  - Clean, attractive layout and color scheme

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
1. Use the large tabs at the top to switch between "YourPod" (script generator) and "Image Captioning".
2. For scripts: Enter text or upload a PDF, select output style, and generate/download audio.
3. For image captions: Upload an image, choose caption type, and generate a funny/sarcastic caption or creative story. The result appears in a styled box.

---

## Notes
- **BLIP Model Loading:** The first time you use image captioning, the BLIP model will be downloaded and loaded into memory. This may take up to a minute. Subsequent uses will be much faster.
- **No Hugging Face API key is required** for image captioning—everything runs locally.
- **Groq API key is required** for script and story generation.

---

## Deployment
- **Local:** Works out of the box as long as you have internet access (for Groq API and gTTS).
- **Streamlit Community Cloud:**
  - gTTS may not work reliably due to outbound network restrictions.
  - BLIP model download may be slow or restricted on some cloud platforms.
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
- [BLIP (Salesforce)](https://huggingface.co/Salesforce/blip-image-captioning-base)
- [transformers](https://huggingface.co/docs/transformers/index)

---

## License
MIT License 