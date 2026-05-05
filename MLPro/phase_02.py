from google import genai
import json
import os

# 1. Setup
API_KEY = "AIzaSyBHSDaYp-aGnhfQow3Kyr0WZ279xmU1O4Y"
client = genai.Client(api_key=API_KEY)

# 2. Data Load
print("Loading transcript...")
with open("transcript_data.json", "r") as f:
    segments = json.load(f)

# Convert data to clean string
text_data = "\n".join([f"{s['start']}s: {s['text']}" for s in segments])

prompt = f"""
Pick ONE viral coding clip (30-60s) from this transcript. 
Return ONLY a JSON object: {{"start": float, "end": float, "title": "string", "reason": "string"}}

Transcript:
{text_data}
"""

print("Gemini (2.5-Flash) analyzing")

try:
    # 2026 Modern SDK Call with the CORRECT model from your list
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=prompt
    )

    # Extract JSON
    raw_response = response.text.strip().replace('```json', '').replace('```', '')
    result = json.loads(raw_response)

    print(f"\n Finalized Choice: {result['title']}")
    print(f"Start: {result['start']}s | End: {result['end']}s")

    with open("clip_metadata.json", "w") as f:
        json.dump(result, f)
    print("\nPhase 2 Complete! clip_metadata.json is ready.")

except Exception as e:
    print(f"\n Error: {e}")