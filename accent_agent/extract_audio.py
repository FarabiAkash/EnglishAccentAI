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