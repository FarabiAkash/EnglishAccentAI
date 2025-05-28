from flask import Flask, request, jsonify
from accent_agent import download_video, extract_audio, transcribe_audio, analyze_accent

app = Flask(__name__)

@app.route('/accent-analysis', methods=['POST'])
def accent_analysis():
    data = request.get_json()
    if not data or 'video_link' not in data:
        return jsonify({
            "status": "error",
            "message": "Missing 'video_link' in request body."
        }), 400

    try:
        # Step 1: Download video
        video_link = data['video_link']
        video_path = download_video(video_link)

        # Step 2: Extract audio
        audio_path = extract_audio(video_path)

        # Step 3: Transcribe audio
        transcribed_text = transcribe_audio(audio_path)

        # Step 4: Analyze accent
        result = analyze_accent(transcribed_text, is_audio=False)

        # Get accent info
        accent = result.get("accent", "Unknown")
        confidence = result.get("confidence", 0.0)
        explanation = result.get("explanation", "No explanation provided.")

        # Return structured response
        return jsonify({
            "status": "success",
            "accent_analysis": {
                "accent": accent,
                "confidence": round(confidence, 2),
                "explanation": explanation
            }
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True)
