# 🗣️ Accent Analysis API using OpenAI & Whisper

This Flask-based API accepts a video URL, extracts audio, transcribes speech using OpenAI Whisper, and analyzes the speaker’s English accent using GPT.

---

## 🚀 Features

- ✅ Accepts public video links (`.mp4`)
- 🎧 Extracts audio automatically
- 📝 Transcribes speech using OpenAI Whisper
- 🌍 Classifies the speaker's accent using GPT
- 📊 Provides a confidence score and a detailed explanation
- 📁 Logs all activities with timestamps

---

## 📦 Expected Request Format

Send a `POST` request to `/accent-analysis`:

```json
{
  "video_link": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/WeAreGoingOnBullrun.mp4"
}
```

## 📤 Example Response

```json
{
  "accent_analysis": {
    "accent": "American",
    "confidence": 0.9,
    "explanation": "The transcription reflects a casual, conversational style typical of American English. Phrases like 'oh, yeah' and the reference to specific American car models (Ford SVT Raptor, Shelby GT500) suggest a cultural context rooted in the United States. Additionally, the use of 'we're going to' and the overall sentence structure align with American speech patterns. The speaker's enthusiasm and informal tone further support this classification."
  },
  "status": "success"
}
```

## 🛠️ Setup & Installation

1. Clone the repo

```bash
git clone https://github.com/yourusername/accent-analysis-api.git
cd accent-analysis-api
```

2. Create virtual environment & install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Run the Flask app:

```bash
python app.py
```

## 📁 Project Structure

```bash
EnglishAccentAI
├── app.py
├── accent_agent/
│ ├── __init__.py
│ ├── download_video.py
│ ├── extract_audio.py
│ ├── transcribe_audio.py
│ └── analyze_accent.py
├── logs/
│ └── app_YYYYMMDD.log
│ └── download_video_YYYYMMDD.log
├── audio/
│ └── {all extracted audios}
├── video/
│ └── {all downloaded videos}
├── requirements.txt
└── README.md
```

## 📁 Project Structure

1. Client sends a video link via POST /accent-analysis.
2. download_video fetches and saves the video locally.
3. extract_audio converts the video to a .wav audio file.
4. transcribe_audio uses OpenAI Whisper (via API or local model) to convert speech to text.
5. analyze_accent sends the transcription to GPT to classify the accent.
6. API responds with accent type, confidence score, and explanation.

## 📁 Project Structure

```bash
curl -X POST http://127.0.0.1:5000/accent-analysis \
     -H "Content-Type: application/json" \
     -d '{"video_link": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/WeAreGoingOnBullrun.mp4"}'
```

## 📌 Notes

- Ensure ffmpeg is installed and accessible in your system path.
- Input video must be publicly accessible.
- Use environment variables or .env files to manage API keys securely.

<!-- CONTACT -->

## Contact

Al-Farabi Akash - alfa.farabi@gmail.com - +8801703212426

Profile Link: [Resume Profile](https://farabiakash.github.io/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Author -->

## 👨‍💻 Author

Al-Farabi Akash — [LinkedIn](https://www.linkedin.com/in/al-farabi-akash/)

```bash
Let me know if you'd like the `requirements.txt` generated as well!
```
