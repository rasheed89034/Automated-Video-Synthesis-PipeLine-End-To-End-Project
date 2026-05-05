import yt_dlp
import os

# --- STEP 1: Dynamic URL Selection ---
# We pick that link which is saved in url.txt by dashboard
if os.path.exists("url.txt"):
    with open("url.txt", "r") as f:
        url = f.read().strip()
else:
    print(" Error: url.txt not found! Start process from Dashboard.")
    exit()

# Mac Homebrew FFmpeg Path
ffmpeg_path = "/opt/homebrew/bin/ffmpeg"

print(f"--- Downloading Video File from: {url} ---")

# ydl_opts = {
#     # Best quality MP4 format select karna
#     'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
#     'outtmpl': 'video_file.mp4', 
#     'ffmpeg_location': ffmpeg_path,
#     # Agar pehle se video_file.mp4 mojud hai, to usay overwrite kar do
#     'overwrites': True, 
# }

ydl_opts = {

    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', 
    'outtmpl': 'video_file.mp4',
    'cookiesfrombrowser': ('chrome',),
    'remote_components': ['ejs:github'],
    'n_check_sig': True,
    'overwrites': True,
}


if os.path.exists("video_file.mp4"):
    os.remove("video_file.mp4")

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print(f"\n Video downlaoded and ready for processing")

except Exception as e:
    print(f"\n Error during download: {e}")