import openai
import os
import logging
from datetime import datetime
from dotenv import load_dotenv  # <-- Add this

# Load environment variables from .env file
load_dotenv()  # <-- Add this

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)
# Configure logging
log_filename = f"logs/transcribe_audio_{datetime.now().strftime('%Y%m%d')}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    filename=log_filename,
    filemode="a"
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def transcribe_audio(audio_path: str, model="whisper-1") -> str:
    """
    Transcribes the given audio file using OpenAI Whisper API (v1.x client).
    """
    logging.info("[STEP] Starting audio transcription process.")
    try:
        with open(audio_path, "rb") as audio_file:
            logging.info(f"[STEP] Sending audio file '{audio_path}' to OpenAI Whisper API.")
            transcript = client.audio.transcriptions.create(
                file=audio_file,
                model=model,
            )
        logging.info("[SUCCESS] Audio transcription completed successfully.")
        return transcript.text
    except Exception as e:
        logging.error(f"[ERROR] Failed to transcribe audio: {e}")
        raise