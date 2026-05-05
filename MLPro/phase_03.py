import json
import os
from moviepy import VideoFileClip
import moviepy.video.fx as vfx

# 1. Load Metadata
print("Loading timestamps from Phase 2...")
with open("clip_metadata.json", "r") as f:
    metadata = json.load(f)

start_t = metadata['start']
end_t = metadata['end']

# 2. Load Original Video
video_path = "video_file.mp4" 

if not os.path.exists(video_path):
    print(f"Error: {video_path} not found!")
    exit()

clip_full = VideoFileClip(video_path)
if start_t >= clip_full.duration:
    # If AI gives wrong time
    start_t = max(0, clip_full.duration - 40)
    end_t = clip_full.duration
# ----------------------------------------------

print(f"Processing clip: {start_t}s to {end_t}s...")

# 3. Cutting and Cropping
# Now we use 'clip_full' which we loaded above
clip = clip_full.subclipped(start_t, end_t)

# --- THE EVEN MATH FIX ---
(w, h) = clip.size
target_ratio = 9/16

# We first calculate width and then make it "Even"
target_w = int(h * target_ratio)
if target_w % 2 != 0:
    target_w -= 1  

print(f"Original Size: {w}x{h} | New Vertical Size: {target_w}x{h}")

# Calculate center coordinates
x1 = (w - target_w) / 2
y1 = 0
x2 = x1 + target_w
y2 = h

# Crop according to new MoviePy Standard
final_clip = vfx.Crop(x1=x1, y1=y1, x2=x2, y2=y2).apply(clip)

# 4. Save with Mac/QuickTime Compatibility
output_name = "final_short_even.mp4"
print("Rendering your AI Short (Even dimensions)")

final_clip.write_videofile(
    output_name, 
    codec="libx264", 
    audio_codec="aac", 
    fps=24, 
    ffmpeg_params=["-pix_fmt", "yuv420p"] 
)

print(f"\nCONGRATULATIONS! '{output_name}' is ready and will run!")