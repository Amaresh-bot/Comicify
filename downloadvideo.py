import yt_dlp
import os

def Download(link, output_file='videoclip.mp4'):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'outtmpl': output_file,
        'merge_output_format': 'mp4',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        print("Download completed successfully")
    except Exception as e:
        print(f"Download error: {e}")
        raise

def DownloadAudio(link, output_file='videoaudio.mp3'):
    base = output_file.replace('.mp3', '')
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': base + '.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        print("Audio download completed successfully")
    except Exception as e:
        print(f"Audio download error: {e}")
        raise