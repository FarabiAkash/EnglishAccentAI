
# accent_agent.py
import os
import re
import requests
import yt_dlp

def sanitize_filename(name):
    """Sanitize filename by removing special characters."""
    return re.sub(r'[^\w\-_.]', '_', name)

def download_video(url, output_dir="video"):
    """
    Downloads a video from a public URL.
    Supports direct MP4 URLs and platforms like Loom, etc.
    Returns the path to the downloaded video file.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Check if it's a direct video link (ends with .mp4 or similar)
    if url.endswith(('.mp4', '.mov', '.webm')):
        filename = sanitize_filename(url.split("/")[-1])
        filepath = os.path.join(output_dir, filename)
        print(f"[INFO] Downloading direct video: {url}")

        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(1024 * 1024):
                    f.write(chunk)
            print(f"[SUCCESS] Video downloaded to {filepath}")
            return filepath
        else:
            raise Exception(f"Failed to download file: {url} (Status Code: {response.status_code})")

    # Use yt_dlp for Loom, etc.
    else:
        print(f"[INFO] Attempting to download using yt_dlp for: {url}")
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            downloaded_file = ydl.prepare_filename(info)
            print(f"[SUCCESS] Video downloaded to {downloaded_file}")
            return downloaded_file



import os
import ffmpeg

def extract_audio(video_path, output_dir="audio"):
    """
    Extracts audio from a video file and saves it as a .wav file.
    Returns the path to the audio file.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    filename = os.path.splitext(os.path.basename(video_path))[0]
    audio_path = os.path.join(output_dir, f"{filename}.wav")
    print(f"[INFO] Extracting audio from {video_path} to {audio_path}")
    try:
        (
            ffmpeg
            .input(video_path)
            .output(audio_path, acodec='libmp3lame')
            .run(overwrite_output=True)
        )
        print(f"[SUCCESS] Extracted audio to {audio_path}")
        return audio_path
    except ffmpeg.Error as e:
        print(f"[ERROR] ffmpeg failed: {e}")
        return None


import openai

# Create an OpenAI client instance (you can also set OPENAI_API_KEY as env variable)
client = openai.OpenAI()

def transcribe_audio(audio_path: str, model="whisper-1") -> str:
    """
    Transcribes the given audio file using OpenAI Whisper API (v1.x client).
    """
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            file=audio_file,
            model=model,
        )
    return transcript.text


def analyze_accent(input_data: str, is_audio: bool = False) -> dict:
    """
    Analyze and classify accent using GPT-4 based on text or audio input.

    Args:
        input_data (str): Either a transcription text or path to audio file.
        is_audio (bool): If True, input_data is treated as an audio file path.

    Returns:
        dict: Accent classification result with confidence and explanation.
    """
    # If input is audio, transcribe first
    if is_audio:
        print(f"[INFO] Transcribing audio file: {input_data}")
        transcription = transcribe_audio(input_data)
        print(f"[INFO] Transcription: {transcription}")
    else:
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

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # or "gpt-4" if you have access
        messages=[
            {"role": "system", "content": "You analyze English accents."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=300,
    )
    print("[INFO] GPT response received.")
    print("[DEBUG] Raw GPT response:", response)
    # Parse response JSON safely
    import json
    import re
    raw_content = response.choices[0].message.content

    # Strip Markdown-style code blocks
    cleaned_json = re.sub(r"^```json\s*|\s*```$", "", raw_content.strip(), flags=re.IGNORECASE)

    try:
        analysis = json.loads(cleaned_json)
    except Exception as e:
        print("[ERROR] Failed to parse GPT response as JSON:", e)
        analysis = {"raw_response": raw_content}


    return analysis