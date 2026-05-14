import whisper
from datetime import timedelta

def transcribe_audio(path, sub_file='videosub.srt'):
    model = whisper.load_model("base")
    transcribe = model.transcribe(audio=path, fp16=False)
    segments = transcribe['segments']

    for segment in segments:
        startTime = str(0) + str(timedelta(seconds=int(segment['start']))) + ',000'
        endTime   = str(0) + str(timedelta(seconds=int(segment['end']))) + ',000'
        text = segment['text']
        segmentId = segment['id'] + 1
        entry = f"{segmentId}\n{startTime} --> {endTime}\n{text.lstrip()}\n\n"

        with open(sub_file, 'a', encoding='utf-8') as f:
            f.write(entry)

    return sub_file