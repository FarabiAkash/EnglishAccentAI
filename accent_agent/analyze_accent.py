
client = openai.OpenAI()

def analyze_accent(input_data: str) -> dict:
    """
    Analyze and classify accent using GPT-4 based on text or audio input.

    Args:
        input_data (str): Either a transcription text or path to audio file.
        is_audio (bool): If True, input_data is treated as an audio file path.

    Returns:
        dict: Accent classification result with confidence and explanation.
    """

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