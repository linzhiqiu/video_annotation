#!/usr/bin/env python3
"""
CameraBench-Pro Taxonomy Editor Server

Serves static files AND handles saving taxonomy JSON back to the folder.

Usage:
    cd taxonomy/
    python3 server.py

Then open http://localhost:8090
"""
import http.server
import json
import os
import sys

PORT = 8090
DIRECTORY = os.path.dirname(os.path.abspath(__file__)) or '.'


class TaxonomyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        if self.path == '/manifest':
            files = sorted(f for f in os.listdir(DIRECTORY)
                           if f.startswith('taxonomy_') and f.endswith('.json'))
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(json.dumps(files).encode())
            return
        super().do_GET()

    def do_POST(self):
        if self.path == '/save':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                payload = json.loads(body)
                filename = payload.get('filename', '')
                data = payload.get('data')

                # Validate filename: must be taxonomy_vN.json
                if not filename or not filename.startswith('taxonomy_v') or not filename.endswith('.json'):
                    self.send_error(400, 'Invalid filename')
                    return
                # Prevent path traversal
                if '/' in filename or '\\' in filename or '..' in filename:
                    self.send_error(400, 'Invalid filename')
                    return

                filepath = os.path.join(DIRECTORY, filename)
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'ok': True, 'path': filepath}).encode())
                print(f'  ✓ Saved {filename} ({os.path.getsize(filepath):,} bytes)')

            except Exception as e:
                self.send_error(500, str(e))
        else:
            self.send_error(404, 'Not found')

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        # Only log POST, manifest, and errors
        msg = str(args[0]) if args else ''
        code = str(args[1]) if len(args) > 1 else ''
        if 'POST' in msg or 'manifest' in msg or ('200' not in code and '304' not in code):
            super().log_message(format, *args)


def main():
    # List JSON files in directory
    jsons = sorted(f for f in os.listdir(DIRECTORY) if f.startswith('taxonomy_') and f.endswith('.json'))
    print(f'\n  CameraBench-Pro Taxonomy Editor')
    print(f'  ────────────────────────────────')
    print(f'  Directory: {DIRECTORY}')
    print(f'  JSON files: {", ".join(jsons) if jsons else "(none found)"}')
    print(f'\n  → http://localhost:{PORT}/taxonomy_editor.html\n')

    server = http.server.HTTPServer(('', PORT), TaxonomyHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n  Shutting down.')
        server.shutdown()


if __name__ == '__main__':
    main()