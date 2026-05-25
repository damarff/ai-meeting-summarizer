# 🎙️ AI Voice Meeting Summarizer

An intelligent **Multimodal Audio AI** web application built with Streamlit and Google Gemini. It automatically listens to meeting recordings (MP3, WAV, M4A) and generates professional meeting minutes, executive summaries, and structured action items.

## Business Value 💼
Executives, Project Managers, and Sales Teams waste countless hours manually transcribing meetings and writing follow-up emails. This application solves that by:
- **Zero Manual Typing:** Transcribes and understands context directly from raw audio.
- **Multimodal AI:** Uses `gemini-2.5-flash` natively to listen to audio without needing third-party Speech-to-Text (STT) intermediaries like Whisper.
- **Privacy First:** The audio is processed and immediately deleted from the AI server after transcription.

## Tech Stack 🚀
- **Frontend**: `Streamlit`
- **Audio Processing / LLM**: `Google GenAI SDK` (Gemini 1.5 Multimodal)
- **Language**: `Python 3`

## How to Run 🛠️

1. Clone the repository and navigate to the directory.
2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Set your Gemini API Key in `.env`:
```env
GEMINI_API_KEY=your_api_key_here
```

4. Launch the application:
```bash
streamlit run app.py
```
