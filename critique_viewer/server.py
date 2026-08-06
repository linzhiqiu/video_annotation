#!/usr/bin/env python3
"""
Server for Critique Viewer - displays failed/missing critiques.

Usage:
    python server.py [--port 8081] [--host 0.0.0.0]
"""

import http.server
import socketserver
import json
import argparse
from pathlib import Path
from urllib.parse import unquote

# Configuration - look in caption folder for output_critiques
# The script is in critique_viewer/, so parent is video_annotation/
# We want video_annotation/caption/output_critiques
SCRIPT_DIR = Path(__file__).parent.resolve()
OUTPUT_CRITIQUES_DIR = SCRIPT_DIR.parent / "caption" / "output_critiques"
PORT = 8081
HOST = "0.0.0.0"


class CritiqueViewerHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler for the critique viewer."""

    def __init__(self, *args, output_dir=None, **kwargs):
        self.output_dir = output_dir
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Handle GET requests."""
        
        # API endpoint: Get available export folders
        if self.path == "/api/critique-folders":
            self.send_json_response(self.get_export_folders())
            return
        
        # API endpoint: Get critique data for an export folder
        if self.path.startswith("/api/critiques/"):
            export_folder = unquote(self.path.split("/api/critiques/")[1])
            data = self.get_critique_data(export_folder)
            if data is not None:
                self.send_json_response(data)
            else:
                self.send_error(404, "Export folder not found or no critiques available")
            return
        
        # Serve static files (HTML, CSS, JS)
        super().do_GET()

    def get_export_folders(self):
        """Get list of export folders by scanning caption_export directory."""
        export_folders = []
        
        try:
            # caption_export is at video_annotation/caption_export (sibling to caption/)
            caption_export_dir = self.output_dir.parent.parent / "caption_export"
            
            print(f"Scanning for export folders in: {caption_export_dir}")
            
            if not caption_export_dir.exists():
                print(f"Warning: caption_export directory not found at {caption_export_dir}")
                return []
            
            # Find all export_* directories
            for item in caption_export_dir.iterdir():
                if item.is_dir() and item.name.startswith("export_"):
                    export_folders.append(item.name)
                    print(f"  Found export folder: {item.name}")
            
            print(f"Total export folders found: {len(export_folders)}")
            return sorted(export_folders)
            
        except Exception as e:
            print(f"Error getting export folders: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_critique_data(self, export_folder_name):
        """Get all critiques for a specific export folder."""
        critiques = []
        
        try:
            if not self.output_dir.exists():
                print(f"Output directory does not exist: {self.output_dir}")
                return None
            
            print(f"Loading critiques for export folder: {export_folder_name}")
            
            # Scan through all critique files
            for critique_type_dir in self.output_dir.iterdir():
                if not critique_type_dir.is_dir():
                    continue
                
                critique_type = critique_type_dir.name
                
                for caption_type_dir in critique_type_dir.iterdir():
                    if not caption_type_dir.is_dir():
                        continue
                    
                    caption_type = caption_type_dir.name
                    
                    for critique_file in caption_type_dir.glob("*_critique.json"):
                        try:
                            with open(critique_file, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                            
                            # Check if this critique belongs to the requested export folder
                            source_folder = data.get("source_export_folder", "")
                            # Handle both full paths and just folder names
                            source_folder_name = Path(source_folder).name if source_folder else ""
                            
                            if source_folder_name != export_folder_name:
                                continue
                            
                            # Extract relevant fields for display
                            critique_info = {
                                "video_id": data.get("video_id"),
                                "caption_type": data.get("caption_type", caption_type),
                                "critique_type": data.get("critique_type", critique_type),
                                "status": data.get("status"),
                                "error_message": data.get("error_message"),
                                "skip_reason": data.get("skip_reason"),
                                "attempts_made": data.get("attempts_made"),
                                "model": data.get("model"),
                                "prompt_name": data.get("prompt_name"),
                                "generation_timestamp": data.get("generation_timestamp"),
                                "source_export_folder": source_folder
                            }
                            
                            critiques.append(critique_info)
                            
                        except Exception as e:
                            print(f"Error reading critique file {critique_file}: {e}")
                            continue
            
            print(f"Found {len(critiques)} critiques for {export_folder_name}")
            return critiques
            
        except Exception as e:
            print(f"Error getting critique data for {export_folder_name}: {e}")
            import traceback
            traceback.print_exc()
            return None

    def send_json_response(self, data):
        """Send a JSON response."""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8'))

    def log_message(self, format, *args):
        """Override to customize logging."""
        # Only log API calls, skip static file requests
        try:
            if args and len(args) > 0 and isinstance(args[0], str) and "api" in args[0]:
                print(f"{self.address_string()} - {format % args}")
        except:
            pass  # Ignore logging errors


def create_handler(output_dir):
    """Create a handler with the specified directory."""
    def handler(*args, **kwargs):
        return CritiqueViewerHandler(*args, output_dir=output_dir, **kwargs)
    return handler


def main():
    parser = argparse.ArgumentParser(description="Critique Viewer Server")
    parser.add_argument("--port", type=int, default=PORT, help=f"Port to run server on (default: {PORT})")
    parser.add_argument("--host", type=str, default=HOST, help=f"Host to bind to (default: {HOST})")
    parser.add_argument("--output_dir", type=str, default=None, help="Path to output_critiques directory")
    args = parser.parse_args()

    # Determine script directory
    script_dir = Path(__file__).parent.resolve()
    
    # Set output directory - default to caption/output_critiques
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        output_dir = OUTPUT_CRITIQUES_DIR
    
    # Check if directory exists
    if not output_dir.exists():
        print(f"⚠️  Warning: output_critiques directory not found at {output_dir}")
        print(f"    Please ensure critiques are in: {output_dir.resolve()}")
    else:
        print(f"✓ Found output_critiques directory: {output_dir.resolve()}")
    
    # Check for caption_export directory
    caption_export_dir = output_dir.parent.parent / "caption_export"
    if not caption_export_dir.exists():
        print(f"⚠️  Warning: caption_export directory not found at {caption_export_dir}")
    else:
        export_count = len([x for x in caption_export_dir.iterdir() if x.is_dir() and x.name.startswith("export_")])
        print(f"✓ Found caption_export directory with {export_count} export folders")
    
    # Change to the script directory to serve index.html
    import os
    os.chdir(script_dir)
    
    # Create handler with custom directory
    handler = create_handler(output_dir)
    
    # Create server
    with socketserver.TCPServer((args.host, args.port), handler) as httpd:
        print("=" * 60)
        print(f"🔍 Critique Viewer Server")
        print("=" * 60)
        print(f"📁 Critiques:    {output_dir.resolve()}")
        print(f"📁 Exports:      {caption_export_dir.resolve()}")
        print(f"🌐 Server:       http://{args.host}:{args.port}")
        if args.host == "0.0.0.0":
            import socket
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            print(f"🔗 Local URL:    http://{local_ip}:{args.port}")
            print(f"🔗 Localhost:    http://localhost:{args.port}")
        print("=" * 60)
        print("\n✨ Server is running. Press Ctrl+C to stop.\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Shutting down server...")


if __name__ == "__main__":
    main()