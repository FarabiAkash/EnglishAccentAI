from flask import Flask, request, jsonify
from accent_agent import download_video, extract_audio, transcribe_audio, analyze_accent
from flask_cors import CORS
import logging
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

log_filename = f"logs/app_{datetime.now().strftime('%Y%m%d')}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    filename=log_filename,
    filemode="a"
)

@app.route('/accent-analysis', methods=['POST'])
def accent_analysis():
    logging.info("[STEP] Received request for accent analysis.")
    data = request.get_json()
    if not data or 'video_link' not in data:
        logging.error("[ERROR] Missing 'video_link' in request body.")
        return jsonify({
            "status": "error",
            "message": "Missing 'video_link' in request body."
        }), 400

    try:
        # Step 1: Download video
        video_link = data['video_link']
        logging.info("[STEP] Downloading video.")
        video_path = download_video.download_video(video_link)
        logging.info(f"[SUCCESS] Video downloaded: {video_path}")

        # Step 2: Extract audio
        logging.info("[STEP] Extracting audio from video.")
        audio_path = extract_audio.extract_audio(video_path)
        if not audio_path:
            logging.error("[ERROR] Audio extraction failed.")
            return jsonify({
                "status": "error",
                "message": "Audio extraction failed."
            }), 500
        logging.info(f"[SUCCESS] Audio extracted: {audio_path}")

        # Step 3: Transcribe audio
        logging.info("[STEP] Transcribing audio.")
        transcribed_text = transcribe_audio.transcribe_audio(audio_path)
        logging.info(f"[SUCCESS] Audio transcribed.")

        # Step 4: Analyze accent
        logging.info("[STEP] Analyzing accent.")
        result = analyze_accent.analyze_accent(transcribed_text)
        logging.info(f"[SUCCESS] Accent analysis complete.")

        # Get accent info
        accent = result.get("accent", "Unknown")
        confidence = result.get("confidence", 0.0)
        explanation = result.get("explanation", "No explanation provided.")

        # Return structured response
        logging.info("[STEP] Returning accent analysis result.")
        return jsonify({
            "status": "success",
            "accent_analysis": {
                "accent": accent,
                "confidence": f'{round(confidence, 2) * 100}%',
                "explanation": explanation
            }
        }), 200

    except Exception as e:
        logging.error(f"[ERROR] Exception in accent analysis endpoint: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=False)
