from google import genai

client = genai.Client(api_key="AIzaSyDJwUFtylEGA1_-WsjLV01kTSokiBkN_WY")

print("--- Checking available models ---")
try:
    # Sirf model ka naam aur description print karte hain
    for m in client.models.list():
        print(f"Model ID: {m.name}")
except Exception as e:
    print(f" Error: {e}")