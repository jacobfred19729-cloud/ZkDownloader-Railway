# Simple Flask Backend for ZKDownloader
# Run: python backend.py

from flask import Flask, request, jsonify, send_file, send_from_directory, Response, stream_with_context
from flask_cors import CORS
import yt_dlp
import os
import tempfile
from threading import Thread, Lock
import time
import uuid

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # Allow frontend to access

# Global download manager
download_manager = {
    'downloads': {},  # Active downloads
    'lock': Lock()
}

@app.route('/api/info', methods=['GET'])
def get_video_info():
    """Get video information and formats"""
    url = request.args.get('url')
    
    if not url:
        return jsonify({'error': 'URL required'}), 400
    
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,  # Bypass SSL issues for thumbnails
            'extract_flat': False,  # Extract full info including thumbnails
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Handle Instagram thumbnails specifically
            thumbnail = info.get('thumbnail', '')
            if 'instagram.com' in url and not thumbnail:
                # Try to get thumbnail from alternatives
                thumbnails = info.get('thumbnails', [])
                if thumbnails:
                    # Get the largest thumbnail
                    thumbnail = max(thumbnails, key=lambda x: x.get('height', 0)).get('url', '')
            
            return jsonify({
                'title': info.get('title', 'Unknown'),
                'thumbnail': thumbnail,
                'duration': info.get('duration', 0),
                'uploader': info.get('uploader', 'Unknown'),
                'webpage_url': info.get('webpage_url', info.get('original_url', url)),
                'formats': [
                    {
                        'format_id': f.get('format_id'),
                        'ext': f.get('ext', 'mp4'),
                        'height': f.get('height', 0),
                        'width': f.get('width', 0),
                        'filesize': f.get('filesize') or f.get('filesize_approx') or 0,
                        'filesize_approx': f.get('filesize_approx') or f.get('filesize') or 0,
                        'vcodec': f.get('vcodec', 'none'),
                        'acodec': f.get('acodec', 'none'),
                        'abr': f.get('abr', 0),
                        'fps': f.get('fps', 0),
                        'tbr': f.get('tbr', 0),
                    }
                    for f in info.get('formats', [])
                ]
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/start-download', methods=['POST'])
def start_download():
    """Start a new download task"""
    data = request.json
    url = data.get('url')
    format_id = data.get('format', 'best')
    title = data.get('title', 'video')
    
    if not url:
        return jsonify({'error': 'URL required'}), 400
    
    # Generate unique download ID
    download_id = str(uuid.uuid4())
    
    # Create temp directory
    temp_dir = tempfile.mkdtemp()
    output_path = os.path.join(temp_dir, '%(title)s.%(ext)s')
    
    # Initialize download data
    with download_manager['lock']:
        download_manager['downloads'][download_id] = {
            'id': download_id,
            'url': url,
            'format_id': format_id,
            'title': title,
            'status': 'preparing',
            'progress': 0,
            'downloaded': 0,
            'total': 0,
            'speed': 0,
            'eta': 0,
            'temp_dir': temp_dir,
            'output_path': output_path,
            'file_path': None,
            'error': None,
            'paused': False
        }
    
    # Start download in background thread
    thread = Thread(target=download_worker, args=(download_id,))
    thread.daemon = True
    thread.start()
    
    return jsonify({'download_id': download_id, 'status': 'started'})

def download_worker(download_id):
    """Background worker for downloading"""
    download_data = download_manager['downloads'].get(download_id)
    if not download_data:
        return
    
    try:
        def progress_hook(d):
            if download_data['paused']:
                raise Exception('Download paused')
            
            if d['status'] == 'downloading':
                download_data['status'] = 'downloading'
                download_data['downloaded'] = d.get('downloaded_bytes', 0)
                download_data['total'] = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                download_data['speed'] = d.get('speed', 0) or 0
                download_data['eta'] = d.get('eta', 0) or 0
                
                if download_data['total'] > 0:
                    download_data['progress'] = (download_data['downloaded'] / download_data['total']) * 100
                    
            elif d['status'] == 'finished':
                download_data['status'] = 'processing'
                download_data['progress'] = 100
        
        # For Instagram, ensure audio is merged with video
        format_id = download_data['format_id']
        url = download_data['url']
        
        # Check if this is Instagram and format needs audio merging
        if 'instagram.com' in url:
            # For Instagram, use format that includes both video and audio without FFmpeg
            ydl_opts = {
                'format': 'best[height<=720]/best',
                'outtmpl': download_data['output_path'],
                'quiet': True,
                'no_warnings': True,
                'progress_hooks': [progress_hook],
                'extractaudio': False,  # Don't extract audio separately
                'embed_subs': False,     # Don't embed subtitles
                'writethumbnail': False, # Don't write thumbnail
            }
        else:
            ydl_opts = {
                'format': format_id,
                'outtmpl': download_data['output_path'],
                'quiet': True,
                'no_warnings': True,
                'progress_hooks': [progress_hook],
            }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([download_data['url']])
        
        # Find downloaded file
        files = os.listdir(download_data['temp_dir'])
        if files:
            download_data['file_path'] = os.path.join(download_data['temp_dir'], files[0])
            download_data['status'] = 'completed'
        else:
            download_data['status'] = 'error'
            download_data['error'] = 'File not found after download'
            
    except Exception as e:
        if 'paused' in str(e).lower():
            download_data['status'] = 'paused'
        else:
            download_data['status'] = 'error'
            download_data['error'] = str(e)

@app.route('/api/download-progress/<download_id>', methods=['GET'])
def get_download_progress(download_id):
    """Get real-time download progress"""
    download_data = download_manager['downloads'].get(download_id)
    
    if not download_data:
        return jsonify({'error': 'Download not found'}), 404
    
    return jsonify({
        'id': download_data['id'],
        'title': download_data['title'],
        'status': download_data['status'],
        'progress': download_data['progress'],
        'downloaded': download_data['downloaded'],
        'total': download_data['total'],
        'speed': download_data['speed'],
        'eta': download_data['eta'],
        'error': download_data['error']
    })

@app.route('/api/pause-download/<download_id>', methods=['POST'])
def pause_download(download_id):
    """Pause a download"""
    download_data = download_manager['downloads'].get(download_id)
    
    if not download_data:
        return jsonify({'error': 'Download not found'}), 404
    
    download_data['paused'] = True
    download_data['status'] = 'paused'
    
    return jsonify({'status': 'paused'})

@app.route('/api/resume-download/<download_id>', methods=['POST'])
def resume_download(download_id):
    """Resume a paused download"""
    download_data = download_manager['downloads'].get(download_id)
    
    if not download_data:
        return jsonify({'error': 'Download not found'}), 404
    
    download_data['paused'] = False
    
    # Restart download in background
    thread = Thread(target=download_worker, args=(download_id,))
    thread.daemon = True
    thread.start()
    
    return jsonify({'status': 'resumed'})

@app.route('/api/cancel-download/<download_id>', methods=['POST'])
def cancel_download(download_id):
    """Cancel a download"""
    download_data = download_manager['downloads'].get(download_id)
    
    if not download_data:
        return jsonify({'error': 'Download not found'}), 404
    
    download_data['status'] = 'cancelled'
    download_data['paused'] = True
    
    # Cleanup
    try:
        if os.path.exists(download_data['temp_dir']):
            import shutil
            shutil.rmtree(download_data['temp_dir'])
    except:
        pass
    
    with download_manager['lock']:
        del download_manager['downloads'][download_id]
    
    return jsonify({'status': 'cancelled'})

@app.route('/api/get-file/<download_id>', methods=['GET'])
def get_downloaded_file(download_id):
    """Get the downloaded file"""
    download_data = download_manager['downloads'].get(download_id)
    
    if not download_data:
        return jsonify({'error': 'Download not found'}), 404
    
    if download_data['status'] != 'completed':
        return jsonify({'error': 'Download not completed'}), 400
    
    if not download_data['file_path'] or not os.path.exists(download_data['file_path']):
        return jsonify({'error': 'File not found'}), 404
    
    filename = os.path.basename(download_data['file_path'])
    return send_file(download_data['file_path'], as_attachment=True, download_name=filename)

@app.route('/api/active-downloads', methods=['GET'])
def get_active_downloads():
    """Get all active downloads"""
    downloads = []
    for download_id, data in download_manager['downloads'].items():
        downloads.append({
            'id': data['id'],
            'title': data['title'],
            'status': data['status'],
            'progress': data['progress'],
            'downloaded': data['downloaded'],
            'total': data['total'],
            'speed': data['speed'],
            'eta': data['eta']
        })
    
    return jsonify({'downloads': downloads})

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'ok'})

@app.route('/api/proxy-thumbnail')
def proxy_thumbnail():
    """Proxy thumbnail to avoid CORS issues"""
    thumbnail_url = request.args.get('url')
    if not thumbnail_url:
        return jsonify({'error': 'URL required'}), 400
    
    try:
        import requests
        response = requests.get(thumbnail_url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        if response.status_code == 200:
            # Determine content type
            content_type = response.headers.get('content-type', 'image/jpeg')
            return Response(response.content, mimetype=content_type)
        else:
            return jsonify({'error': 'Failed to fetch thumbnail'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    """Serve frontend"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('.', path)

if __name__ == '__main__':
    # Get port from environment (for cloud deployment) or use default
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print("🚀 ZKDownloader Backend Starting...")
    print(f"📱 Frontend: http://localhost:{port}")
    print(f"🔧 API: http://localhost:{port}/api/info")
    app.run(host='0.0.0.0', port=port, debug=debug)

