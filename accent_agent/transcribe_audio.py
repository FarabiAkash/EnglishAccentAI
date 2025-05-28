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