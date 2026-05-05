import json
import os
from moviepy import VideoFileClip, TextClip, CompositeVideoClip

# 1. Setup Environment
os.environ["IMAGEMAGICK_BINARY"] = "/opt/homebrew/bin/magick"
font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"

# 2. Data Load (From Phase 1 and 2)
with open("clip_metadata.json", "r") as f:
    meta = json.load(f)
with open("transcript_data.json", "r") as f:
    transcript = json.load(f)

# Load video from Phase 3
video = VideoFileClip("final_short_even.mp4")
clip_start, clip_end = meta['start'], meta['end']

# 3. Create Subtitle Layers
subtitle_clips = []
for s in transcript:
    if s['start'] >= clip_start and s['end'] <= clip_end:
        start_in_clip = s['start'] - clip_start
        duration = s['end'] - s['start']
        
        txt = (TextClip(
                text=s['text'], 
                font_size=40, 
                color='yellow',
                font=font_path,
                method='caption',
                size=(int(video.w * 0.8), None)
            )
            .with_start(start_in_clip)
            .with_duration(duration)
            .with_position(('center', int(video.h * 0.70))))
        subtitle_clips.append(txt)

# 4. Merge Layers
print(f"Merging {len(subtitle_clips)} layers...")
final_video = CompositeVideoClip([video] + subtitle_clips).with_duration(video.duration)
final_video.audio = video.audio 

# --- Add here  ---
output = "viral_short_with_captions.mp4" 

final_video.write_videofile(
    output, 
    codec="libx264", 
    audio_codec="aac", 
    fps=24, 
    ffmpeg_params=[
        "-pix_fmt", "yuv420p", 
        "-movflags", "+faststart", # QuickTime compatibility fix
        "-profile:v", "main",     ## -profile:v and -level are used for to make video compatible with all devices 
        "-level", "3.1"
    ]
)

print(f"\nFinal File Ready: {output}")