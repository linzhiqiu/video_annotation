#!/usr/bin/env python3
"""
Simple server for Label Video Viewer.

Usage:
    python server.py [--port 8080] [--host 0.0.0.0]
"""

import http.server
import socketserver
import json
import os
import argparse
from pathlib import Path
from urllib.parse import unquote

# Configuration
VIDEO_LABELS_DIR = Path("../video_labels")  # Relative to script location
VIDEOS_DIR = Path("../videos")  # Relative to script location
PORT = 8080
HOST = "0.0.0.0"  # 0.0.0.0 allows external access, use "localhost" for local only


class ReusableTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """Multi-threaded TCPServer that allows immediate port reuse."""
    allow_reuse_address = True  # This fixes the "Address already in use" error
    daemon_threads = True  # Threads will close when main thread exits
    request_queue_size = 50  # Handle up to 50 pending connections


class LabelViewerHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler for the label viewer."""

    def __init__(self, *args, video_labels_dir=None, videos_dir=None, **kwargs):
        self.video_labels_dir = video_labels_dir
        self.videos_dir = videos_dir
        super().__init__(*args, **kwargs)

    def get_video_urls(self, folder_name):
        """Get video URL mapping from video_urls.json for a specific folder."""
        try:
            json_path = self.video_labels_dir / folder_name / "video_urls.json"
            if not json_path.exists():
                return None
            
            with open(json_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading video URLs for {folder_name}: {e}")
            return None

    def send_header(self, keyword, value):
        """Override to add cache control headers for HTML/CSS/JS files."""
        super().send_header(keyword, value)
        
    def end_headers(self):
        """Override to add cache control headers for development files."""
        # Disable caching for HTML, CSS, and JS files to see updates immediately
        if (self.path.endswith('.html') or self.path.endswith('.css') or 
            self.path.endswith('.js') or self.path == '/' or self.path == '/index.html'):
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0, post-check=0, pre-check=0')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', 'Thu, 01 Jan 1970 00:00:00 GMT')
        super().end_headers()

    # def do_GET(self):
    #     """Handle GET requests."""
        
    #     # API endpoint: Get available folders
    #     if self.path == "/api/folders":
    #         self.send_json_response(self.get_folders())
    #         return
        
    #     # API endpoint: Get label data for a folder
    #     if self.path.startswith("/api/labels/"):
    #         folder_name = unquote(self.path.split("/api/labels/")[1])
    #         data = self.get_label_data(folder_name)
    #         if data:
    #             self.send_json_response(data)
    #         else:
    #             self.send_error(404, "Folder not found")
    #         return
        
    #     # Serve videos
    #     if self.path.startswith("/videos/"):
    #         video_name = unquote(self.path.split("/videos/")[1])
    #         self.serve_video(video_name)
    #         return
        
    #     # Serve static files (HTML, CSS, JS)
    #     super().do_GET()

    def do_GET(self):
        """Handle GET requests."""
        
        # API endpoint: Get available folders
        if self.path == "/api/folders":
            self.send_json_response(self.get_folders())
            return
        
        # API endpoint: Get label data for a folder
        if self.path.startswith("/api/labels/"):
            folder_name = unquote(self.path.split("/api/labels/")[1])
            data = self.get_label_data(folder_name)
            if data:
                self.send_json_response(data)
            else:
                self.send_error(404, "Folder not found")
            return
        
        # API endpoint: Get video URLs for a folder
        if self.path.startswith("/api/video_urls/"):
            folder_name = unquote(self.path.split("/api/video_urls/")[1])
            data = self.get_video_urls(folder_name)
            if data:
                self.send_json_response(data)
            else:
                self.send_error(404, "Video URLs not found")
            return
        
        # Serve videos
        if self.path.startswith("/videos/"):
            video_name = unquote(self.path.split("/videos/")[1])
            self.serve_video(video_name)
            return
        
        # Serve static files (HTML, CSS, JS)
        super().do_GET()

    def get_folders(self):
        """Get list of available video_labels folders."""
        try:
            folders = []
            if self.video_labels_dir.exists():
                for item in self.video_labels_dir.iterdir():
                    if item.is_dir() and (item / "all_labels.json").exists():
                        folders.append(item.name)
            return sorted(folders)
        except Exception as e:
            print(f"Error getting folders: {e}")
            return []

    def get_label_data(self, folder_name):
        """Get label data from all_labels.json for a specific folder."""
        try:
            json_path = self.video_labels_dir / folder_name / "all_labels.json"
            if not json_path.exists():
                return None
            
            with open(json_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading label data for {folder_name}: {e}")
            return None

    def serve_video(self, video_name):
        """Serve a video file with optimized streaming."""
        try:
            video_path = self.videos_dir / video_name
            
            if not video_path.exists():
                print(f"❌ Video not found: {video_name}")
                self.send_error(404, f"Video not found: {video_name}")
                return
            
            # Get file size
            file_size = video_path.stat().st_size
            
            # Determine content type based on extension
            content_type = 'video/mp4'
            ext = video_path.suffix.lower()
            if ext == '.webm':
                content_type = 'video/webm'
            elif ext == '.ogg':
                content_type = 'video/ogg'
            elif ext == '.mov':
                content_type = 'video/quicktime'
            
            # Simple streaming without range requests for faster initial load
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(file_size))
            self.send_header('Cache-Control', 'public, max-age=3600')  # Cache videos for 1 hour
            self.end_headers()
            
            # Stream the file in chunks for better performance
            with open(video_path, 'rb') as f:
                chunk_size = 1024 * 1024  # 1MB chunks
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    
        except Exception as e:
            print(f"Error serving video {video_name}: {e}")
            self.send_error(500, str(e))

    def send_json_response(self, data):
        """Send a JSON response."""
        response_bytes = json.dumps(data).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(response_bytes)))
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        self.wfile.write(response_bytes)

    def log_message(self, format, *args):
        """Override to customize logging."""
        # Only log errors and API calls
        if "api" in args[0] or self.command == "POST":
            print(f"{self.address_string()} - {format % args}")


def create_handler(video_labels_dir, videos_dir):
    """Create a handler with the specified directories."""
    def handler(*args, **kwargs):
        return LabelViewerHandler(*args, video_labels_dir=video_labels_dir, videos_dir=videos_dir, **kwargs)
    return handler


def main():
    parser = argparse.ArgumentParser(description="Label Video Viewer Server")
    parser.add_argument("--port", type=int, default=PORT, help=f"Port to run server on (default: {PORT})")
    parser.add_argument("--host", type=str, default=HOST, help=f"Host to bind to (default: {HOST})")
    parser.add_argument("--video_labels_dir", type=str, default=None, help="Path to video_labels directory")
    parser.add_argument("--videos_dir", type=str, default=None, help="Path to videos directory")
    args = parser.parse_args()

    # Determine script directory
    script_dir = Path(__file__).parent.resolve()
    
    # Set directories
    video_labels_dir = Path(args.video_labels_dir) if args.video_labels_dir else script_dir / VIDEO_LABELS_DIR
    videos_dir = Path(args.videos_dir) if args.videos_dir else script_dir / VIDEOS_DIR
    
    # Check if directories exist
    if not video_labels_dir.exists():
        print(f"⚠️  Warning: video_labels directory not found at {video_labels_dir}")
        print(f"    Creating directory...")
        video_labels_dir.mkdir(parents=True, exist_ok=True)
    
    if not videos_dir.exists():
        print(f"⚠️  Warning: videos directory not found at {videos_dir}")
        print(f"    Please ensure videos are in: {videos_dir.resolve()}")
    
    # Change to the script directory to serve index.html
    os.chdir(script_dir)
    
    # Create handler with custom directories
    handler = create_handler(video_labels_dir, videos_dir)
    
    # Use ReusableTCPServer instead of socketserver.TCPServer
    with ReusableTCPServer((args.host, args.port), handler) as httpd:
        print("=" * 60)
        print(f"🚀 Label Video Viewer Server (Multi-threaded)")
        print("=" * 60)
        print(f"📁 Video labels: {video_labels_dir.resolve()}")
        print(f"📹 Videos:       {videos_dir.resolve()}")
        print(f"🌐 Server:       http://{args.host}:{args.port}")
        if args.host == "0.0.0.0":
            import socket
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            print(f"🔗 Local URL:    http://{local_ip}:{args.port}")
            print(f"🔗 Localhost:    http://localhost:{args.port}")
        print("=" * 60)
        print("\n✨ Server is running with multi-threading support")
        print("💡 Can handle multiple users simultaneously")
        print("💡 Hard refresh browser (Ctrl+Shift+R / Cmd+Shift+R) to see changes\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Shutting down server...")
            print("✅ Port released successfully")


if __name__ == "__main__":
    main()