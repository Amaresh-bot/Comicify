import yt_dlp
import os

def _setup_cookies():
    cookies_content = os.environ.get('YOUTUBE_COOKIES')
    if cookies_content and not os.path.exists('cookies.txt'):
        with open('cookies.txt', 'w') as f:
            f.write(cookies_content)
    return 'cookies.txt' if os.path.exists('cookies.txt') else None

def Download(link, output_file='videoclip.mp4'):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'outtmpl': output_file,
        'merge_output_format': 'mp4',
        'cookiefile': _setup_cookies(),
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
        'cookiefile': _setup_cookies(),
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
