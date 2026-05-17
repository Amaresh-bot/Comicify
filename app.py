from flask import Flask, render_template, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcript', methods=['POST'])
def transcript():
    data = request.get_json()
    link = data.get('link', '').strip()

    try:
        if 'v=' in link:
            video_id = link.split('v=')[1].split('&')[0]
        elif 'youtu.be/' in link:
            video_id = link.split('youtu.be/')[1].split('?')[0]
        else:
            return jsonify({'error': 'Invalid YouTube URL'}), 400

        ytt = YouTubeTranscriptApi()
        transcript_data = ytt.fetch(video_id)
        segments = [{'start': s['start'], 'duration': s['duration'], 'text': s['text']} for s in transcript_data]
        return jsonify({'segments': segments, 'video_id': video_id})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import os
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
