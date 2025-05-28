# accent_agent.py
import os
import re
import requests
import yt_dlp
import logging
from datetime import datetime

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)
# Log file with date stamp
log_filename = f"logs/download_video_{datetime.now().strftime('%Y%m%d')}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    filename=log_filename,
    filemode="a"
)

def sanitize_filename(name):
    """Sanitize filename by removing special characters."""
    return re.sub(r'[^\w\-_.]', '_', name)

def download_video(url, output_dir="video"):
    """
    Downloads a video from a public URL.
    Supports direct MP4 URLs and platforms like Loom, etc.
    Returns the path to the downloaded video file.
    """
    logging.info("[STEP] Starting video download process.")
    os.makedirs(output_dir, exist_ok=True)

    # Check if it's a direct video link (ends with .mp4 or similar)
    if url.endswith(('.mp4', '.mov', '.webm')):
        filename = sanitize_filename(url.split("/")[-1])
        filepath = os.path.join(output_dir, filename)
        logging.info(f"[STEP] Downloading direct video: {url}")

        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(1024 * 1024):
                        f.write(chunk)
                logging.info(f"[SUCCESS] Video downloaded to {filepath}")
                return filepath
            else:
                logging.error(f"[ERROR] Failed to download file: {url} (Status Code: {response.status_code})")
                raise Exception(f"Failed to download file: {url} (Status Code: {response.status_code})")
        except Exception as e:
            logging.error(f"[ERROR] Exception during direct video download: {e}")
            raise

    # Use yt_dlp for Loom, etc.
    else:
        logging.info(f"[STEP] Attempting to download using yt_dlp for: {url}")
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'quiet': True
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                downloaded_file = ydl.prepare_filename(info)
                logging.info(f"[SUCCESS] Video downloaded to {downloaded_file}")
                return downloaded_file
        except Exception as e:
            logging.error(f"[ERROR] yt_dlp failed to download video: {e}")
            raise