import yt_dlp
import whisper
import os
import json

# Now we read the link from url.txt
if os.path.exists("url.txt"):
    with open("url.txt", "r") as f:
        url = f.read().strip()
else:
    print("Error: url.txt not found!")
    exit()

ffmpeg_path = "/opt/homebrew/bin/ffmpeg"

print(f"Step 1: Downloading Audio from {url}")

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'audio_file', 
    'ffmpeg_location': ffmpeg_path,
    'cookiesfrombrowser': ('chrome',), ## to use cookies from chrome
    'remote_components': ['ejs:github'], 
    'n_check_sig': True,
    'quiet': False, 
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3', ## to save in mp3 format
        'preferredquality': '192', ## to save as 192kbps
    }],
}

# Cleanup
if os.path.exists("audio_file.mp3"): os.remove("audio_file.mp3")

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

# 2. Transcription
print("Step 2: AI Text Extraction (Whisper)")
audio_filename = "audio_file.mp3"

if os.path.exists(audio_filename):
    model = whisper.load_model("base") ## ML Model use for Transcribe Audio to Text (Base, Small, Medium, Large)
    result = model.transcribe(audio_filename, fp16=False) ## fp16=False is for CPU processing
    
    with open("transcript_data.json", "w", encoding="utf-8") as f:
        json.dump(result['segments'], f, indent=4)
    print("Phase 1 Done: Data saved")
else:
    print("Error: Audio file downloading failed")