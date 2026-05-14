from flask import Flask, render_template, request, send_file, jsonify
import threading
import uuid
import os
import traceback
from converttocomic import convertVideoToComic
import static_ffmpeg
static_ffmpeg.add_paths()

app = Flask(__name__)

# Track job status
jobs = {}

def run_job(job_id, youtube_link):
    try:
        jobs[job_id] = {'status': 'running', 'message': 'Downloading video...'}
        convertVideoToComic(youtube_link, job_id)
        jobs[job_id] = {'status': 'done', 'message': 'PDF ready!'}
    except Exception as e:
        jobs[job_id] = {'status': 'error', 'message': str(e)}
        traceback.print_exc()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    link = data.get('link', '').strip()
    if not link or 'youtube.com' not in link and 'youtu.be' not in link:
        return jsonify({'error': 'Please provide a valid YouTube URL'}), 400

    job_id = str(uuid.uuid4())
    jobs[job_id] = {'status': 'pending', 'message': 'Starting...'}
    thread = threading.Thread(target=run_job, args=(job_id, link))
    thread.daemon = True
    thread.start()
    return jsonify({'job_id': job_id})

@app.route('/status/<job_id>')
def status(job_id):
    job = jobs.get(job_id, {'status': 'not_found', 'message': 'Job not found'})
    return jsonify(job)

@app.route('/download/<job_id>')
def download(job_id):
    pdf_path = f'output_{job_id}.pdf'
    if os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=True, download_name='comic.pdf')
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
