import cv2, os
import extractframes
import srtsplit
import downloadvideo
import youtubesrt
import helpers
import generatesubtitle

def convertVideoToComic(youtube_link, job_id='local'):
    video_file   = f'videoclip_{job_id}.mp4'
    audio_file   = f'videoaudio_{job_id}.mp3'
    sub_file     = f'videosub_{job_id}.srt'
    frames_dir   = f'frames_{job_id}'
    output_pdf   = f'output_{job_id}.pdf'

    os.makedirs(frames_dir, exist_ok=True)

    # Step 1: Get subtitles (YouTube API first, Whisper fallback)
    res = youtubesrt.genSubfromYoutube(youtube_link, sub_file)
    if res == 0:
        print("YouTube transcript unavailable, using Whisper...")
        downloadvideo.DownloadAudio(youtube_link, audio_file)
        generatesubtitle.transcribe_audio(audio_file, sub_file)

    # Step 2: Download video
    downloadvideo.Download(youtube_link, video_file)

    # Step 3: Extract frames and build comic
    startstr = '00:00'
    endstr   = '00:00'
    dialogues = srtsplit.subtitleSplit(sub_file)
    count = 0
    for frames in dialogues:
        startstr = frames[1][3:8]
        if helpers.timediffsec(startstr, endstr) > 2:
            count = extractframes.extract_frame(video_file, endstr, startstr, count, frames_dir=frames_dir)
        endstr = frames[1][20:25]
        count = extractframes.extract_frame(video_file, startstr, endstr, count, len(frames[2])+1, frames[2], frames_dir=frames_dir)

    startstr = endstr
    video = cv2.VideoCapture(video_file)
    endstr = helpers.frametommss(video)
    if helpers.timediffsec(startstr, endstr) > 2:
        extractframes.extract_frame(video_file, startstr, endstr, count, frames_dir=frames_dir)
    video.release()

    # Step 4: Convert frames to PDF
    helpers.converttopdf(frames_dir, output_pdf)

    # Step 5: Cleanup
    helpers.deletefiles(frames_dir)
    os.rmdir(frames_dir)
    if os.path.exists(video_file):  os.remove(video_file)
    if os.path.exists(sub_file):    os.remove(sub_file)
    if os.path.exists(audio_file):  os.remove(audio_file)