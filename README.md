# Lost and Found Script Generator (DDD College)

A Streamlit-based web app for generating podcast-style scripts, summaries, and detailed explanations from text, PDFs, or news topics. Converts scripts to audio using MeloTTS and Llama 3.1 (Ollama). Designed for DDD College lost-and-found and announcement use cases.

## Features
- **Input Types:**
  - Text input
  - PDF upload (extracts text)
  - News topic (fetches news content)
- **Output Styles:**
  - Male & Female podcast-style discussion
  - Summary
  - Detailed explanation
- **Audio Generation:**
  - Uses MeloTTS for TTS (male/female voices)
  - Downloadable MP3
- **LLM:**
  - Uses Llama 3.1 8B via Ollama (local, free)
- **UI:**
  - Streamlit, with tabs for input types and output style selection

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your_github_repo_url>
cd your-repo-directory
```

### 2. Install Dependencies
```bash
pip install streamlit pymupdf langchain langchain-community ollama melotts requests beautifulsoup4
```

### 3. Install and Run Ollama
- [Download Ollama](https://ollama.com/download)
- Pull the Llama 3.1 8B model:
```bash
ollama pull llama3.1:8b
ollama serve  # Start the Ollama server
```

### 4. (Optional) Set Up NewsAPI
- Get a free API key from [NewsAPI](https://newsapi.org/)
- Add your key in `script_generator_app.py` (`NEWSAPI_KEY` variable)

### 5. Run the App
```bash
streamlit run script_generator_app.py
```

## Usage
1. Select an input type (Text, PDF, or News Topic).
2. Enter or upload your content.
3. Choose an output style (Podcast, Summary, Detailed Explanation).
4. Click "Generate Script".
5. Listen to or download the generated audio.

## Sample Inputs & Outputs

### Input (Text):
```
Lost: A blue laptop in DDD library on July 2, 2025.
```

### Podcast-Style Output:
```
Host 1 (Male): Welcome back, DDD students! We've got an urgent lost item alert. Someone's missing a blue laptop in the library!
Host 2 (Female): Yeah, it was last seen on July 2nd, probably left near the study desks. If it's yours, don't wait!
Host 1: Head to the DDD lost-and-found office or email student@domain.com to claim it. Let's get that laptop back!
```

### Summary Output:
```
A blue laptop was lost in the DDD library on July 2, 2025. Contact the lost-and-found office.
```

### Detailed Explanation Output:
```
On July 2, 2025, a blue laptop was reported lost in the DDD college library, likely near the study area. The owner is urged to contact the lost-and-found office at student@domain.com to verify and claim it. This incident highlights the importance of securing personal belongings in shared spaces.
```

## Project Submission (DDD College)
- **Format:** Single Python file (`script_generator_app.py`) and this README.
- **Integration:** Can be added as a new page/tab to the main Lost and Found Web App.
- **Testing:**
  - Test with sample PDFs, text, and news topics.
  - Ensure Ollama and MeloTTS are running locally.
- **GitHub Link:** [Your repository URL here]

## Notes
- All tools used are free and open-source.
- For non-text PDFs, OCR (e.g., pytesseract) can be added as a future enhancement.
- For image captioning, see the BLIP integration in the main app.

---
*For questions, contact the DDD College project team.* 