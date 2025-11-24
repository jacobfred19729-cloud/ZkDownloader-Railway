# Simple Flask Backend for ZKDownloader
# Run: python backend.py

from flask import Flask, request, jsonify, send_file, send_from_directory, Response, stream_with_context, session
from flask_cors import CORS
from flask_session import Session
import yt_dlp
import os
import tempfile
from threading import Thread, Lock
import time
import uuid
from datetime import datetime, timedelta
import shutil
import re

app = Flask(__name__, static_folder='.', static_url_path='')

# Configure session for Railway deployment
secret_key = os.environ.get('SECRET_KEY', 'zkdownloader-secret-key-change-in-production')
if not secret_key or secret_key == '':
    secret_key = 'zkdownloader-railway-secret-key-2024'
app.config['SECRET_KEY'] = secret_key
print(f"Secret key configured: {secret_key[:10]}...")

# Use simple client-side session for Railway compatibility
app.config['SESSION_TYPE'] = 'null'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = False

# Initialize session
try:
    Session(app)
    print("Session initialized successfully")
except Exception as e:
    print(f"Session initialization failed: {e}")
    # Continue without session - will use fallback mechanism

CORS(app, supports_credentials=True)  # Allow credentials for sessions

# User-specific download manager
user_download_managers = {}
user_sessions = {}

def sanitize_filename(title, max_length=50):
    """Sanitize and shorten filename to prevent file system errors"""
    if not title:
        return "video"
    
    # Remove special characters and emojis
    # Keep only alphanumeric, spaces, and basic punctuation
    sanitized = re.sub(r'[^\w\s\-_.(),]', '', title)
    
    # Replace multiple spaces with single space
    sanitized = re.sub(r'\s+', ' ', sanitized).strip()
    
    # Remove leading/trailing punctuation
    sanitized = sanitized.strip('._-()')
    
    # Limit length
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length].rstrip()
    
    # Ensure it's not empty
    if not sanitized:
        sanitized = "video"
    
    return sanitized

def get_user_id():
    """Get or create user ID from session"""
    try:
        # Try to get user ID from session
        user_id = session.get('user_id')
        if not user_id:
            # Generate unique user ID
            user_id = str(uuid.uuid4())
            session['user_id'] = user_id
            session['created_at'] = datetime.now()
            
            # Initialize user download manager
            user_download_managers[user_id] = {
                'downloads': {},  # Active downloads for this user
                'lock': Lock()
            }
        
        # Update session activity
        session['last_activity'] = datetime.now()
        return user_id
    except Exception as e:
        print(f"Session error in get_user_id: {e}")
        # Fallback to a temporary user ID
        return f"temp_{uuid.uuid4()}"

def get_user_download_manager():
    """Get download manager for current user"""
    try:
        user_id = get_user_id()
        if user_id not in user_download_managers:
            user_download_managers[user_id] = {
                'downloads': {},
                'lock': Lock()
            }
        return user_download_managers[user_id]
    except Exception as e:
        print(f"Session error in get_user_download_manager: {e}")
        # Create a fallback user ID and manager
        fallback_id = f"fallback_{uuid.uuid4()}"
        if fallback_id not in user_download_managers:
            user_download_managers[fallback_id] = {
                'downloads': {},
                'lock': Lock()
            }
        return user_download_managers[fallback_id]

def cleanup_old_sessions():
    """Clean up sessions older than 24 hours"""
    current_time = datetime.now()
    expired_users = []
    
    for user_id, session_data in user_sessions.items():
        if 'last_activity' in session_data:
            if current_time - session_data['last_activity'] > timedelta(hours=24):
                expired_users.append(user_id)
    
    # Clean up expired users
    for user_id in expired_users:
        if user_id in user_download_managers:
            # Clean up temp directories
            for download_data in user_download_managers[user_id]['downloads'].values():
                if 'temp_dir' in download_data and os.path.exists(download_data['temp_dir']):
                    import shutil
                    shutil.rmtree(download_data['temp_dir'])
            
            del user_download_managers[user_id]
        del user_sessions[user_id]

@app.route('/api/info', methods=['GET'])
def get_video_info():
    """Get video information and formats"""
    url = request.args.get('url')
    
    if not url:
        return jsonify({'error': 'URL required'}), 400
    
    try:
        # Special handling for different platforms
        if 'tiktok.com' in url:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'nocheckcertificate': True,
                'extract_flat': False,
                'extractor_args': {
                    'tiktok': {
                        'api_hostname': 'api16-normal-c-useast1a.tiktokv.com',
                    }
                }
            }
        elif 'facebook.com' in url or 'fb.watch' in url:
            # Special handling for Facebook to get formats with audio
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'nocheckcertificate': True,
                'extract_flat': False,
                'extractor_args': {
                    'facebook': {
                        'extract_flat': False,
                    }
                }
            }
        else:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'nocheckcertificate': True,  # Bypass SSL issues for thumbnails
                'extract_flat': False,  # Extract full info including thumbnails
            }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Handle Instagram and Facebook thumbnails specifically
            thumbnail = info.get('thumbnail', '')
            if ('instagram.com' in url or 'facebook.com' in url or 'fb.watch' in url) and not thumbnail:
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
                'webpage_url': info.get('webpage_url', ''),
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
                        'url': f.get('url', ''),
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
    
    # Sanitize title for filename
    sanitized_title = sanitize_filename(title)
    output_path = os.path.join(temp_dir, f'{sanitized_title}.%(ext)s')
    
    # Get user ID first (session access in main thread)
    user_id = get_user_id()
    
    # Ensure user manager exists for this user ID
    if user_id not in user_download_managers:
        user_download_managers[user_id] = {
            'downloads': {},
            'lock': Lock()
        }
    
    user_manager = user_download_managers[user_id]
    
    # Initialize download data for this user
    with user_manager['lock']:
        user_manager['downloads'][download_id] = {
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
    thread = Thread(target=download_worker, args=(download_id, user_id))
    thread.daemon = True
    thread.start()
    
    return jsonify({'download_id': download_id, 'status': 'started'})

def download_worker(download_id, user_id):
    """Background worker for downloading"""
    try:
        user_manager = user_download_managers[user_id]
    except KeyError:
        print(f"User manager not found for user_id: {user_id}")
        return
    
    download_data = user_manager['downloads'].get(download_id)
    if not download_data:
        print(f"Download data not found for download_id: {download_id}")
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
        
        # Check if this is Instagram or Facebook and format needs audio merging
        if 'instagram.com' in url or 'facebook.com' in url or 'fb.watch' in url:
            # For Instagram and Facebook, use format that includes both video and audio
            ydl_opts = {
                'format': 'best[height<=720]/best',
                'outtmpl': download_data['output_path'],
                'quiet': True,
                'no_warnings': True,
                'progress_hooks': [progress_hook],
                'extractaudio': False,  # Don't extract audio separately
                'embed_subs': False,     # Don't embed subtitles
                'writethumbnail': False, # Don't write thumbnail
                # Additional options for Facebook
                'extract_flat': False,
                'nocheckcertificate': True,
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
    user_manager = get_user_download_manager()
    download_data = user_manager['downloads'].get(download_id)
    
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
    user_manager = get_user_download_manager()
    download_data = user_manager['downloads'].get(download_id)
    
    if not download_data:
        return jsonify({'error': 'Download not found'}), 404
    
    download_data['paused'] = True
    download_data['status'] = 'paused'
    
    return jsonify({'status': 'paused'})

@app.route('/api/resume-download/<download_id>', methods=['POST'])
def resume_download(download_id):
    """Resume a paused download"""
    user_manager = get_user_download_manager()
    download_data = user_manager['downloads'].get(download_id)
    
    if not download_data:
        return jsonify({'error': 'Download not found'}), 404
    
    download_data['paused'] = False
    
    # Restart download in background
    user_id = get_user_id()
    thread = Thread(target=download_worker, args=(download_id, user_id))
    thread.daemon = True
    thread.start()
    
    return jsonify({'status': 'resumed'})

@app.route('/api/cancel-download/<download_id>', methods=['POST'])
def cancel_download(download_id):
    """Cancel a download"""
    user_manager = get_user_download_manager()
    download_data = user_manager['downloads'].get(download_id)
    
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
    
    with user_manager['lock']:
        del user_manager['downloads'][download_id]
    
    return jsonify({'status': 'cancelled'})

@app.route('/api/get-file/<download_id>', methods=['GET'])
def get_downloaded_file(download_id):
    """Get the downloaded file"""
    user_manager = get_user_download_manager()
    download_data = user_manager['downloads'].get(download_id)
    
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
    """Get all active downloads for current user"""
    user_manager = get_user_download_manager()
    downloads = []
    for download_id, data in user_manager['downloads'].items():
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
    try:
        # Test session functionality
        test_user_id = get_user_id()
        return jsonify({
            'status': 'ok',
            'session_test': 'working',
            'user_id': test_user_id[:8] + '...',  # Only show first 8 chars for privacy
            'active_users': len(user_download_managers)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

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

