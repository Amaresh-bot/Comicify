from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import SRTFormatter

def genSubfromYoutube(link, sub_file='videosub.srt'):
    try:
        # Extract video ID — handles both full URLs and short URLs
        if 'v=' in link:
            video_id = link.split('v=')[1].split('&')[0]
        elif 'youtu.be/' in link:
            video_id = link.split('youtu.be/')[1].split('?')[0]
        else:
            return 0

        ytt = YouTubeTranscriptApi()
        transcript = ytt.fetch(video_id)
        formatter = SRTFormatter()
        srt_format = formatter.format_transcript(transcript)

        with open(sub_file, 'w', encoding='utf-8') as f:
            f.write(srt_format)
        return 1
    except Exception as e:
        print(f"YouTube transcript failed: {e}")
        return 0