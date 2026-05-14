# Comicify 🦸

[![Deploy on Render](https://img.shields.io/badge/Deploy-Live%20on%20Render-46E3B7?style=for-the-badge&logo=render)](https://comicify-2.onrender.com)

Turn any YouTube video into a Comic Book PDF!

## How it works

1. Paste a YouTube link
2. The app fetches subtitles (or transcribes audio using Whisper)
3. Key frames are extracted from the video
4. Frames are combined with dialogue in speech bubbles
5. A comic book PDF is generated and downloaded

## Tech Stack

- **Python** — core language
- **Flask** — web framework
- **yt-dlp** — YouTube video/audio downloader
- **OpenCV** — frame extraction and image processing
- **Whisper** — AI audio transcription (fallback)
- **youtube-transcript-api** — subtitle fetching
- **img2pdf** — PDF generation

## Run Locally

```bash
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000` in your browser.

## Deploy

Deployed on Render. See `render.yaml` for config.

## Requirements

- Python 3.10+
- ffmpeg installed on system
