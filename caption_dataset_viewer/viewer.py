#!/usr/bin/env python3
"""
Caption Dataset Viewer - Read-Only Interface for Viewing Annotations

Usage:
    python viewer.py [--port 8081] [--host 0.0.0.0] [--videos_dir ./videos]
"""

import http.server
import socketserver
import json
import os
import argparse
from pathlib import Path
from urllib.parse import unquote
import traceback

# Configuration
PORT = 8081
HOST = "0.0.0.0"
ANNOTATIONS_DIR = Path("annotations")  # Local directory with annotations
VIDEOS_DIR = Path("videos")  # Local directory with videos


class ReusableTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """Multi-threaded TCPServer that allows immediate port reuse."""
    allow_reuse_address = True
    daemon_threads = True
    request_queue_size = 50


class CaptionViewerHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler for the caption dataset viewer."""

    def __init__(self, *args, annotations_dir=None, videos_dir=None, **kwargs):
        self.annotations_dir = annotations_dir
        self.videos_dir = videos_dir
        super().__init__(*args, **kwargs)

    def end_headers(self):
        """Override to add cache control headers for development files."""
        if (self.path.endswith('.html') or self.path.endswith('.css') or 
            self.path.endswith('.js') or self.path == '/' or self.path == '/viewer.html'):
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', 'Thu, 01 Jan 1970 00:00:00 GMT')
        super().end_headers()

    def do_GET(self):
        """Handle GET requests."""
        
        # Redirect root to viewer.html
        if self.path == '/':
            self.send_response(302)
            self.send_header('Location', '/viewer.html')
            self.end_headers()
            return
        
        # API: Get available datasets
        if self.path == "/api/datasets":
            self.send_json_response(self.get_datasets())
            return
        
        # API: Get dataset samples (completed only)
        if self.path.startswith("/api/dataset/"):
            dataset_name = unquote(self.path.split("/api/dataset/")[1].split("?")[0])
            data = self.get_dataset_samples(dataset_name)
            if data:
                self.send_json_response(data)
            else:
                self.send_error(404, "Dataset not found")
            return
        
        # API: Get single sample with annotation
        if self.path.startswith("/api/sample/"):
            parts = unquote(self.path.split("/api/sample/")[1]).split("/")
            if len(parts) >= 2:
                dataset_name = parts[0]
                sample_index = int(parts[1])
                data = self.get_single_sample(dataset_name, sample_index)
                if data:
                    self.send_json_response(data)
                else:
                    self.send_error(404, "Sample not found")
            return
        
        # API: Get annotation statistics
        if self.path.startswith("/api/stats/"):
            dataset_name = unquote(self.path.split("/api/stats/")[1])
            stats = self.get_annotation_stats(dataset_name)
            self.send_json_response(stats)
            return
        
        # Serve local videos
        if self.path.startswith("/videos/"):
            video_path = unquote(self.path.split("/videos/")[1])
            self.serve_local_video(video_path)
            return
        
        # Serve static files (HTML, CSS, JS)
        super().do_GET()

    def get_datasets(self):
        """Get list of available datasets from annotations directory."""
        try:
            if not self.annotations_dir.exists():
                return []
            
            datasets = []
            for dataset_dir in self.annotations_dir.iterdir():
                if dataset_dir.is_dir():
                    # Count completed annotations
                    annotation_files = list(dataset_dir.glob("sample_*.json"))
                    completed_count = 0
                    
                    for ann_file in annotation_files:
                        with open(ann_file, 'r') as f:
                            ann = json.load(f)
                            if self.is_annotation_complete(ann):
                                completed_count += 1
                    
                    if completed_count > 0:  # Only show datasets with completed annotations
                        datasets.append({
                            "name": dataset_dir.name,
                            "completed_count": completed_count
                        })
            
            return datasets
        except Exception as e:
            print(f"Error listing datasets: {e}")
            traceback.print_exc()
            return []

    def is_annotation_complete(self, annotation):
        """Check if an annotation is complete."""
        if not annotation:
            return False
        
        required_fields = ['overall', 'camera', 'subject', 'motion', 'scene', 'spatial']
        all_ratings_complete = all(
            annotation.get(field) is not None 
            for field in required_fields
        )
        
        segments_valid = True
        if annotation.get('segments') and len(annotation['segments']) > 0:
            segments_valid = all(
                seg.get('startIndex') is not None and seg.get('endIndex') is not None
                for seg in annotation['segments']
            )
        
        return all_ratings_complete and segments_valid

    def get_dataset_samples(self, dataset_name):
        """Get all completed samples from a dataset."""
        try:
            dataset_dir = self.annotations_dir / dataset_name
            if not dataset_dir.exists():
                return None
            
            # Load all annotation files
            annotation_files = sorted(dataset_dir.glob("sample_*.json"))
            samples = []
            
            for ann_file in annotation_files:
                sample_idx = int(ann_file.stem.split('_')[1])
                
                with open(ann_file, 'r') as f:
                    annotation = json.load(f)
                
                # Only include completed annotations
                if self.is_annotation_complete(annotation):
                    # Extract sample data from annotation
                    sample = {
                        'sample_index': sample_idx,
                        'video_id': annotation.get('video_id', f'sample_{sample_idx}'),
                        'video_path': annotation.get('video_path', ''),
                        'captions': annotation.get('captions', {}),
                        'metadata': annotation.get('metadata', {}),
                        'annotation': annotation
                    }
                    samples.append(sample)
            
            return {
                'dataset_name': dataset_name,
                'samples': samples,
                'total_completed': len(samples)
            }
        except Exception as e:
            print(f"Error loading dataset {dataset_name}: {e}")
            traceback.print_exc()
            return None

    def get_single_sample(self, dataset_name, sample_index):
        """Get a single sample with its annotation."""
        try:
            annotation_file = self.annotations_dir / dataset_name / f"sample_{sample_index}.json"
            
            if not annotation_file.exists():
                return None
            
            with open(annotation_file, 'r') as f:
                annotation = json.load(f)
            
            if not self.is_annotation_complete(annotation):
                return None  # Only show completed annotations
            
            sample = {
                'video_id': annotation.get('video_id', f'sample_{sample_index}'),
                'video_path': annotation.get('video_path', ''),
                'captions': annotation.get('captions', {}),
                'metadata': annotation.get('metadata', {})
            }
            
            return {
                "sample": sample,
                "annotation": annotation,
                "dataset_info": {
                    "name": dataset_name,
                    "sample_index": sample_index
                }
            }
        except Exception as e:
            print(f"Error loading sample {dataset_name}/{sample_index}: {e}")
            traceback.print_exc()
            return None

    def get_annotation_stats(self, dataset_name):
        """Get annotation statistics for a dataset."""
        try:
            dataset_dir = self.annotations_dir / dataset_name
            
            if not dataset_dir.exists():
                return self._empty_stats_response()
            
            annotation_files = sorted(dataset_dir.glob("sample_*.json"))
            
            total_segments = 0
            segment_count = 0
            scores = {
                "overall": [],
                "camera": [],
                "subject": [],
                "motion": [],
                "scene": [],
                "spatial": []
            }
            completed_count = 0
            
            for ann_file in annotation_files:
                with open(ann_file, 'r') as f:
                    annotation = json.load(f)
                
                if not self.is_annotation_complete(annotation):
                    continue
                
                completed_count += 1
                
                # Count segments
                if annotation.get('segments'):
                    total_segments += len(annotation['segments'])
                    segment_count += 1
                
                # Collect scores
                for field in scores.keys():
                    if annotation.get(field) is not None:
                        scores[field].append(annotation[field])
            
            # Calculate averages
            avg_segments = total_segments / segment_count if segment_count > 0 else None
            avg_scores = {}
            for field, values in scores.items():
                if values:
                    avg_scores[field] = round(sum(values) / len(values), 2)
                else:
                    avg_scores[field] = None
            
            return {
                "total": completed_count,
                "avg_segments": round(avg_segments, 2) if avg_segments else None,
                "avg_scores": avg_scores
            }
            
        except Exception as e:
            print(f"Error calculating stats: {e}")
            traceback.print_exc()
            return self._empty_stats_response()
    
    def _empty_stats_response(self):
        """Return empty stats response."""
        return {
            "total": 0,
            "avg_segments": None,
            "avg_scores": {
                "overall": None,
                "camera": None,
                "subject": None,
                "motion": None,
                "scene": None,
                "spatial": None
            }
        }

    def serve_local_video(self, video_path):
        """Serve video from local videos directory."""
        try:
            local_path = self.videos_dir / video_path
            
            if not local_path.exists():
                self.send_error(404, f"Video not found: {video_path}")
                return
            
            # Serve the video
            self.send_response(200)
            
            # Detect video type
            if video_path.lower().endswith('.mkv'):
                content_type = 'video/x-matroska'
            elif video_path.lower().endswith('.webm'):
                content_type = 'video/webm'
            elif video_path.lower().endswith('.mp4'):
                content_type = 'video/mp4'
            else:
                content_type = 'video/mp4'
            
            self.send_header('Content-Type', content_type)
            self.send_header('Accept-Ranges', 'bytes')
            
            file_size = os.path.getsize(local_path)
            self.send_header('Content-Length', str(file_size))
            self.end_headers()
            
            with open(local_path, 'rb') as f:
                self.wfile.write(f.read())
        except Exception as e:
            print(f"Error serving video {video_path}: {e}")
            traceback.print_exc()
            self.send_error(500, f"Error serving video: {video_path}")

    def send_json_response(self, data):
        """Send JSON response."""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Cache-Control', 'no-cache')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        """Override to customize logging."""
        if "api" in args[0]:
            print(f"{self.address_string()} - {format % args}")


def create_handler(annotations_dir, videos_dir):
    """Create a handler with the specified configuration."""
    def handler(*args, **kwargs):
        return CaptionViewerHandler(*args, annotations_dir=annotations_dir,
                                   videos_dir=videos_dir, **kwargs)
    return handler


def main():
    parser = argparse.ArgumentParser(description="Caption Dataset Viewer - Read-Only")
    parser.add_argument("--port", type=int, default=PORT, help=f"Port (default: {PORT})")
    parser.add_argument("--host", type=str, default=HOST, help=f"Host (default: {HOST})")
    parser.add_argument("--annotations_dir", type=str, default=None, help="Annotations directory")
    parser.add_argument("--videos_dir", type=str, default=None, help="Videos directory")
    args = parser.parse_args()

    script_dir = Path(__file__).parent.resolve()
    annotations_dir = Path(args.annotations_dir) if args.annotations_dir else script_dir / ANNOTATIONS_DIR
    videos_dir = Path(args.videos_dir) if args.videos_dir else script_dir / VIDEOS_DIR
    
    if not annotations_dir.exists():
        print(f"❌ Annotations directory not found: {annotations_dir}")
        print(f"   Please create it or specify with --annotations_dir")
        return
    
    if not videos_dir.exists():
        print(f"⚠️  Videos directory not found: {videos_dir}")
        print(f"   Creating directory. Please download videos using download_videos.py")
        videos_dir.mkdir(parents=True, exist_ok=True)
    
    os.chdir(script_dir)
    
    handler = create_handler(annotations_dir, videos_dir)
    
    with ReusableTCPServer((args.host, args.port), handler) as httpd:
        print("=" * 70)
        print(f"👀 Caption Dataset Viewer (Read-Only)")
        print("=" * 70)
        print(f"💾 Annotations:      {annotations_dir.resolve()}")
        print(f"🎬 Videos:           {videos_dir.resolve()}")
        print(f"🌐 Server:           http://{args.host}:{args.port}")
        if args.host == "0.0.0.0":
            import socket
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            print(f"🔗 Local URL:        http://{local_ip}:{args.port}")
            print(f"🔗 Localhost:        http://localhost:{args.port}")
        print("=" * 70)
        print("\n✨ Server running - viewing completed annotations only")
        print("💡 Use download_videos.py to download videos if not present\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Shutting down server...")


if __name__ == "__main__":
    main()