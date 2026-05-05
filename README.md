# 🎥 NeuroClip AI: Intelligent Video Summarization Pipeline
NeuroClip AI is an end-to-end automated pipeline designed to transform long-form video content into viral, social-media-ready shorts. By leveraging Whisper AI for high-fidelity transcription and Google Gemini for semantic highlight extraction, this project automates the most tedious parts of video editing.
# 🚀 Features
AI-Powered Highlight Extraction: Uses Gemini 2.5 Flash to analyze transcripts and identify high-impact, viral moments based on "Excitement" and "Coding Logic."
Speech-to-Text Excellence: Integrated with OpenAI's Whisper AI (Transformer-based architecture) for accurate time-synced transcriptions.
Automated Video Editing: Powered by MoviePy for memory-efficient sub-clipping and vertical cropping (9:16 aspect ratio).\
Dynamic AI Captions: Automatic generation of stylized, temporal-aligned subtitles with word-wrap support.
Cinematic Export: Optimized rendering at 24 FPS with FFmpeg parameters for maximum compatibility across TikTok, Instagram Reels, and YouTube Shorts.
# 📐 Pipeline Architecture
Phase 01 - Transcription: Whisper AI processes the raw audio using a Transformer Encoder-Decoder architecture to generate a transcript_data.json.
Phase 02 - Intelligence: Gemini analyzes the transcript to find the best start/end timestamps, saving them to clip_metadata.json.
Phase 03 - Visual Processing: MoviePy extracts the sub-clip and applies a vertical crop centered on the action.
Phase 04 - Captioning & Export: Subtitles are layered using CompositeVideoClip with relative temporal alignment, then rendered into the final .mp4.
