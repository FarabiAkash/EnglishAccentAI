import os
import ffmpeg
import logging
from datetime import datetime

os.makedirs("logs", exist_ok=True)
log_filename = f"logs/extract_audio_{datetime.now().strftime('%Y%m%d')}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    filename=log_filename,
    filemode="a"
)

def extract_audio(video_path, output_dir="audio"):
    """
    Extracts audio from a video file and saves it as a .wav file.
    Returns the path to the audio file.
    """
    logging.info("[STEP] Starting audio extraction process.")
    os.makedirs(output_dir, exist_ok=True)
    
    filename = os.path.splitext(os.path.basename(video_path))[0]
    audio_path = os.path.join(output_dir, f"{filename}.wav")
    logging.info(f"[STEP] Extracting audio from {video_path} to {audio_path}")
    try:
        (
            ffmpeg
            .input(video_path)
            .output(audio_path, acodec='libmp3lame')
            .run(overwrite_output=True)
        )
        logging.info(f"[SUCCESS] Extracted audio to {audio_path}")
        return audio_path
    except ffmpeg.Error as e:
        logging.error(f"[ERROR] ffmpeg failed: {e}")
        return None
    except Exception as e:
        logging.error(f"[ERROR] Unexpected error during audio extraction: {e}")
        return None