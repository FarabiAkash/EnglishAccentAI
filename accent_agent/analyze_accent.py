import openai
import os
import logging
from datetime import datetime

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)
# Configure logging
log_filename = f"logs/analyze_accent_{datetime.now().strftime('%Y%m%d')}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    filename=log_filename,
    filemode="a"
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=OPENAI_API_KEY)

logging.info("[INFO] OpenAI client initialized.")

def analyze_accent(input_data: str) -> dict:
    """
    Analyze and classify accent using GPT-4 based on text or audio input.

    Args:
        input_data (str): Either a transcription text or path to audio file.
        is_audio (bool): If True, input_data is treated as an audio file path.

    Returns:
        dict: Accent classification result with confidence and explanation.
    """

    logging.info("[STEP] Starting accent analysis process.")
    logging.debug(f"[DEBUG] OpenAI API Key: {OPENAI_API_KEY}")
    transcription = input_data

    # Craft a prompt for GPT-4 to analyze accent
    prompt = (
        "You are a linguistic expert specialized in English accents.\n"
        "Based on the following transcription of speech, analyze the speaker's English accent.\n"
        "Classify the accent (e.g., American, British, Australian, Indian, Irish, Scottish, Canadian, etc.), "
        "estimate confidence, and provide a short explanation for your classification.\n\n"
        f"Transcription:\n{transcription}\n\n"
        "Respond in JSON format with keys: accent, confidence (0 to 1), explanation."
    )

    try:
        logging.info("[STEP] Sending prompt to OpenAI GPT for accent analysis.")
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You analyze English accents."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=300,
        )
        logging.info("[SUCCESS] GPT response received.")
        logging.debug(f"[DEBUG] Raw GPT response: {response}")
        # Parse response JSON safely
        import json
        import re
        raw_content = response.choices[0].message.content

        # Strip Markdown-style code blocks
        cleaned_json = re.sub(r"^```json\s*|\s*```$", "", raw_content.strip(), flags=re.IGNORECASE)

        try:
            analysis = json.loads(cleaned_json)
            logging.info("[SUCCESS] Accent analysis JSON parsed successfully.")
        except Exception as e:
            logging.error(f"[ERROR] Failed to parse GPT response as JSON: {e}")
            analysis = {"raw_response": raw_content}

        return analysis
    except Exception as e:
        logging.error(f"[ERROR] Exception during accent analysis: {e}")
        raise