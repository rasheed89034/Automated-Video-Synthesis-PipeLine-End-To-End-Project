import streamlit as st
import subprocess
import os
import json
import base64


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_PATH = os.path.join(SCRIPT_DIR, "Animate_this_image.mov")

# 1. Page Configuration
st.set_page_config(page_title="NeuroClip AI - Viral Shorts", page_icon="🎬", layout="wide")


def get_base64_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_bg_video(video_file):
    bin_str = get_base64_bin_file(video_file)
    bg_video_html = f'''
    <style>
    #video-bg {{
        position: fixed;
        right: 0; bottom: 0;
        min-width: 100%; min-height: 100%;
        z-index: -1;
        filter: brightness(0.4) contrast(1.2);
        object-fit: cover;
    }}
    .stApp {{
        background: transparent;
    }}
    /* Sidebar styling for assets */
    [data-testid="stSidebar"] {{
        background-color: rgba(255, 215, 0, 0.5) !important;
        border-right: 1px solid rgba(255, 215, 0, 0.3);
    }}
    .sidebar-card {{
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        text-align: center;
        backdrop-filter: blur(5px);
    }}
    </style>
    <video autoplay muted loop playsinline id="video-bg">
        <source src="data:video/quicktime;base64,{bin_str}" type="video/quicktime">
    </video>
    '''
    st.markdown(bg_video_html, unsafe_allow_html=True)

if os.path.exists(VIDEO_PATH):
    set_bg_video(VIDEO_PATH)

# --- 3. SIDEBAR: Generated Assets Section ---
with st.sidebar:
    st.markdown("<h2 style='color: #FFD700; text-align: center; font-size: 30px;font-weight: bold;'>📁 Generated Assets</h2>", unsafe_allow_html=True)
    st.write("---")

    # Section 1: Audio
    st.markdown('<div class="sidebar-card">🎧 <b style="color: #FFFFFF;">Audio Extracted</b></div>', unsafe_allow_html=True)
    if os.path.exists("audio_file.mp3"):
        with open("audio_file.mp3", "rb") as f:
            st.download_button("Download MP3", f, file_name="audio_hq.mp3", use_container_width=True)
    else: st.caption("Status: Waiting...")

    # Section 2: Text
    st.markdown('<div class="sidebar-card">📝 <b style="color: #FFFFFF;">AI Transcript</b></div>', unsafe_allow_html=True)
    if os.path.exists("transcript_data.json"):
        with open("transcript_data.json", "rb") as f:
            st.download_button("Download JSON", f, file_name="transcript.json", use_container_width=True)
    else: st.caption("Status: Waiting...")

    # Section 3: Full Video
    st.markdown('<div class="sidebar-card">📺 <b style="color: #FFFFFF;">Source Video</b></div>', unsafe_allow_html=True)
    if os.path.exists("video_file.mp4"):
        with open("video_file.mp4", "rb") as f:
            st.download_button("Download Full", f, file_name="original_video.mp4", use_container_width=True)
    else: st.caption("Status: Waiting...")

    # Section 4: AI Short
    st.markdown('<div class="sidebar-card">⚡ <b style="color: #FFFFFF;">Viral Short</b></div>', unsafe_allow_html=True)
    if os.path.exists("viral_short_with_captions.mp4"):
        with open("viral_short_with_captions.mp4", "rb") as f:
            st.download_button("Download Short", f, file_name="viral_ai_short.mp4", use_container_width=True)
    else: st.caption("Status: Waiting...")


st.markdown("<h1 style='text-align: center; color: #FFD700; font-size: 100px;'>🛸 NEUROCLIP AI</h1>", unsafe_allow_html=True)
st.markdown("""
    <p style='text-align: center; font-size: 30px; color: white; text-shadow: 2px 2px 4px #000000;'>
        Unleash the power of AI to automatically detect and extract viral moments from long-form content. <br>
        An intelligent multimodal pipeline designed to transform your videos into high-impact social media shorts instantly.
    </p>
""", unsafe_allow_html=True)

st.divider()

col_in1, col_in2, col_in3 = st.columns([1, 2, 1])
with col_in2:
    url = st.text_input("🔗 YouTube URL",placeholder="https://www.youtube.com/watch?v=...")
    process_btn = st.button("Start AI Pipeline", use_container_width=True)

# --- 5. LOGIC: Pipeline Execution ---
if process_btn and url:
    try:
        with st.status("AI Workers are processing...", expanded=True) as status:
            with open("url.txt", "w") as f: f.write(url)
            
            st.write("Phase 01: Extracting Audio...")
            subprocess.run(["python", "phase_01.py"], check=True) 
            
            st.write("Phase 02: AI Selection...")
            subprocess.run(["python", "phase_02.py"], check=True) 
            
            if os.path.exists("download_video.py"):
                st.write("Acquisition: Downloading Video...")
                subprocess.run(["python", "download_video.py"], check=True) 
            
            st.write("Phase 03: Clipping & Cropping...")
            subprocess.run(["python", "phase_03.py"], check=True) 
            
            st.write("Phase 04: Captioning...")
            subprocess.run(["python", "phase_04.py"], check=True) 
            
            status.update(label="All Phases Complete!", state="complete", expanded=False)
        st.balloons()
        st.rerun() 
    except Exception as e:
        st.error(f"Execution Error: {e}")

# Video Preview 
if os.path.exists("viral_short_with_captions.mp4"):
    st.divider()
    st.markdown("<h4 style='text-align: center; color: #FFD700;'>Short Preview</h4>", unsafe_allow_html=True)
    st.video("viral_short_with_captions.mp4")