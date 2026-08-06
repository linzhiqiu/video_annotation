#!/usr/bin/env python3
"""
ShotBench & RefineShot Annotation Viewer Server

Serves a web interface for annotators to review ShotBench and RefineShot samples
side-by-side and mark any mistakes found in the benchmark data.

Usage:
    python server.py [--port 8080] [--host 0.0.0.0]
"""

import http.server
import socketserver
import json
import os
import argparse
from pathlib import Path
from urllib.parse import unquote, parse_qs, urlparse
import traceback
import mimetypes

# Configuration
PORT = 8080
HOST = "0.0.0.0"
DATA_DIR = Path("data")
MEDIA_DIR = Path("media")
ANNOTATIONS_DIR = Path("annotations")

# ShotBench dimensions (must match actual category values in dataset)
CATEGORIES = [
    "shot size", "shot framing", "camera angle", "lens size",
    "lighting type", "lighting", "composition", "camera movement"
]

CATEGORY_ABBREVS = {
    "shot size": "SS",
    "shot framing": "SF", 
    "camera angle": "CA",
    "lens size": "LS",
    "lighting type": "LT",
    "lighting": "LC",
    "composition": "SC",
    "camera movement": "CM"
}

# Display-friendly names (real data uses "lighting" but we show "Lighting Condition")
CATEGORY_DISPLAY_NAMES = {
    "shot size": "Shot Size",
    "shot framing": "Shot Framing",
    "camera angle": "Camera Angle",
    "lens size": "Lens Size",
    "lighting type": "Lighting Type",
    "lighting": "Lighting Condition",
    "composition": "Composition",
    "camera movement": "Camera Movement"
}


def load_dataset(filepath):
    """Load a JSON dataset file, sanitizing any stringified-list fields."""
    if filepath.exists():
        with open(filepath, 'r') as f:
            data = json.load(f)
        # Fix paths/types that might be stored as stringified lists
        for item in data:
            if 'path' in item:
                item['path'] = _unwrap_field(item['path'])
            if 'type' in item:
                item['type'] = _unwrap_field(item['type'])
        return data
    return []


def _unwrap_field(value):
    """Unwrap a field that might be a plain string, list, sequence, or stringified list."""
    if value is None:
        return ''
    if not isinstance(value, str) and hasattr(value, '__len__') and hasattr(value, '__getitem__'):
        try:
            return str(value[0]) if len(value) > 0 else ''
        except (IndexError, KeyError):
            pass
    value = str(value).strip()
    if value.startswith('[') and value.endswith(']'):
        inner = value[1:-1].strip()
        if (inner.startswith("'") and inner.endswith("'")) or \
           (inner.startswith('"') and inner.endswith('"')):
            inner = inner[1:-1]
        return inner
    return value


class ReusableTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """Multi-threaded TCPServer that allows immediate port reuse."""
    allow_reuse_address = True
    daemon_threads = True
    request_queue_size = 50


class ShotBenchViewerHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler for the ShotBench/RefineShot annotation viewer."""

    def __init__(self, *args, data_dir=None, media_dir=None, annotations_dir=None, 
                 shotbench_data=None, refineshot_data=None, **kwargs):
        self.data_dir = data_dir
        self.media_dir = media_dir
        self.annotations_dir = annotations_dir
        self.annotations_dir.mkdir(parents=True, exist_ok=True)
        self.shotbench_data = shotbench_data or []
        self.refineshot_data = refineshot_data or []
        
        # Build index mapping for fast lookup
        self.shotbench_by_index = {s['index']: s for s in self.shotbench_data}
        self.refineshot_by_index = {s['index']: s for s in self.refineshot_data}
        
        super().__init__(*args, **kwargs)

    def end_headers(self):
        """Add cache control headers for development."""
        if (self.path.endswith('.html') or self.path.endswith('.css') or 
            self.path.endswith('.js') or self.path == '/' or self.path == '/index.html'):
            self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', 'Thu, 01 Jan 1970 00:00:00 GMT')
        super().end_headers()

    def do_GET(self):
        """Handle GET requests."""
        
        # Redirect root to index.html
        if self.path == '/':
            self.send_response(302)
            self.send_header('Location', '/index.html')
            self.end_headers()
            return

        # API: Get combined dataset info
        if self.path == "/api/info":
            self.send_json_response(self.get_dataset_info())
            return
        
        # API: Get samples with optional filtering
        if self.path.startswith("/api/samples"):
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)
            modality = params.get('modality', [None])[0]
            category = params.get('category', [None])[0]
            page = int(params.get('page', [0])[0])
            per_page = int(params.get('per_page', [50])[0])
            
            data = self.get_samples(modality=modality, category=category, 
                                   page=page, per_page=per_page)
            self.send_json_response(data)
            return
        
        # API: Get single sample (both ShotBench + RefineShot)
        if self.path.startswith("/api/sample/"):
            try:
                sample_index = int(unquote(self.path.split("/api/sample/")[1].split("?")[0]))
                data = self.get_single_sample(sample_index)
                if data:
                    self.send_json_response(data)
                else:
                    self.send_error(404, "Sample not found")
            except (ValueError, IndexError):
                self.send_error(400, "Invalid sample index")
            return
        
        # API: Get annotation for a sample
        if self.path.startswith("/api/annotation/"):
            try:
                sample_index = int(unquote(self.path.split("/api/annotation/")[1]))
                annotation = self.get_annotation(sample_index)
                self.send_json_response(annotation or {})
            except (ValueError, IndexError):
                self.send_error(400, "Invalid sample index")
            return
        
        # API: Get statistics
        if self.path.startswith("/api/stats"):
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)
            stats = self.get_statistics(params)
            self.send_json_response(stats)
            return

        # Serve media files from media directory
        if self.path.startswith("/media/"):
            media_path = unquote(self.path[7:])  # Remove /media/ prefix
            self.serve_media(media_path)
            return
        
        # Serve HuggingFace proxied images/videos
        if self.path.startswith("/hf_media/"):
            media_path = unquote(self.path[10:])  # Remove /hf_media/ prefix
            self.proxy_hf_media(media_path)
            return
        
        # Serve static files (HTML, CSS, JS)
        super().do_GET()

    def do_POST(self):
        """Handle POST requests."""
        
        # API: Save annotation
        if self.path.startswith("/api/annotation/"):
            try:
                sample_index = int(unquote(self.path.split("/api/annotation/")[1]))
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                annotation_data = json.loads(post_data.decode('utf-8'))
                
                success = self.save_annotation(sample_index, annotation_data)
                if success:
                    self.send_json_response({"success": True, "message": "Annotation saved"})
                else:
                    self.send_error(500, "Failed to save annotation")
            except (ValueError, IndexError) as e:
                self.send_error(400, f"Invalid request: {e}")
            return
        
        self.send_error(404, "Endpoint not found")

    def get_dataset_info(self):
        """Get overview info about both datasets."""
        from collections import Counter
        
        sb_types = Counter(s['type'] for s in self.shotbench_data)
        sb_cats = Counter(s['category'] for s in self.shotbench_data)
        
        # Count annotations
        ann_count = 0
        ann_with_mistakes = 0
        if self.annotations_dir.exists():
            for ann_file in self.annotations_dir.glob("*.json"):
                ann_count += 1
                with open(ann_file) as f:
                    ann = json.load(f)
                    if ann.get('shotbench_mistake') or ann.get('refineshot_mistake'):
                        ann_with_mistakes += 1
        
        # Build categories dynamically from data, preserving order from CATEGORIES
        # but adding any unexpected ones at the end
        data_cats = sorted(set(s['category'] for s in self.shotbench_data))
        ordered_cats = [c for c in CATEGORIES if c in data_cats]
        ordered_cats += [c for c in data_cats if c not in ordered_cats]
        
        return {
            "shotbench": {
                "total": len(self.shotbench_data),
                "by_modality": dict(sb_types),
                "by_category": dict(sb_cats)
            },
            "refineshot": {
                "total": len(self.refineshot_data),
                "available": len(self.refineshot_data) > 0
            },
            "annotations": {
                "total": ann_count,
                "with_mistakes": ann_with_mistakes
            },
            "categories": ordered_cats,
            "category_abbrevs": CATEGORY_ABBREVS,
            "category_display_names": CATEGORY_DISPLAY_NAMES
        }

    def get_samples(self, modality=None, category=None, page=0, per_page=50):
        """Get filtered and paginated samples."""
        samples = self.shotbench_data
        
        # Apply filters
        if modality:
            samples = [s for s in samples if s['type'] == modality]
        if category:
            samples = [s for s in samples if s['category'] == category]
        
        total = len(samples)
        start = page * per_page
        end = start + per_page
        page_samples = samples[start:end]
        
        # Add annotation status and same_as_shotbench flag
        result_samples = []
        for s in page_samples:
            ann = self.get_annotation(s['index'])
            
            # Check if RefineShot has different options/answer
            rs = self.refineshot_by_index.get(s['index'])
            is_same = True
            if rs:
                is_same = (s.get('options') == rs.get('options') and s.get('answer') == rs.get('answer'))
            
            item = {
                **s,
                'has_annotation': ann is not None,
                'has_mistake': bool(ann and (ann.get('shotbench_mistake') or ann.get('refineshot_mistake'))),
                'annotation_status': 'reviewed' if ann else 'pending',
                'same_as_shotbench': is_same
            }
            result_samples.append(item)
        
        return {
            "samples": result_samples,
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": (total + per_page - 1) // per_page
        }

    def get_single_sample(self, sample_index):
        """Get a single sample with both ShotBench and RefineShot data."""
        sb_sample = self.shotbench_by_index.get(sample_index)
        if not sb_sample:
            return None
        
        rs_sample = self.refineshot_by_index.get(sample_index)
        annotation = self.get_annotation(sample_index)
        
        # Determine media URL
        media_path = sb_sample.get('path', '')
        modality = sb_sample.get('type', 'image')
        
        # Build HuggingFace direct URL for the media
        hf_url = f"https://huggingface.co/datasets/Vchitect/ShotBench/resolve/main/{media_path}"
        local_url = f"/media/{media_path}"
        
        # Check if media exists locally
        local_media_path = self.media_dir / media_path
        has_local_media = local_media_path.exists()
        
        # Check if options+answer are identical between ShotBench and RefineShot
        is_same = True
        if rs_sample:
            is_same = (sb_sample.get('options') == rs_sample.get('options') and 
                       sb_sample.get('answer') == rs_sample.get('answer'))
        
        return {
            "shotbench": sb_sample,
            "refineshot": rs_sample,
            "annotation": annotation,
            "same_as_shotbench": is_same,
            "media": {
                "path": media_path,
                "modality": modality,
                "hf_url": hf_url,
                "local_url": local_url,
                "has_local": has_local_media
            }
        }

    def get_annotation(self, sample_index):
        """Get annotation for a sample."""
        ann_file = self.annotations_dir / f"sample_{sample_index}.json"
        if ann_file.exists():
            with open(ann_file, 'r') as f:
                return json.load(f)
        return None

    def save_annotation(self, sample_index, annotation_data):
        """Save annotation for a sample."""
        try:
            ann_file = self.annotations_dir / f"sample_{sample_index}.json"
            annotation_data['sample_index'] = sample_index
            
            with open(ann_file, 'w') as f:
                json.dump(annotation_data, f, indent=2)
            
            print(f"✓ Saved annotation: sample_{sample_index}")
            return True
        except Exception as e:
            print(f"❌ Error saving annotation: {e}")
            traceback.print_exc()
            return False

    def get_statistics(self, params=None):
        """Calculate annotation statistics with optional filtering."""
        from collections import Counter, defaultdict
        
        # Load all annotations
        annotations = {}
        if self.annotations_dir.exists():
            for ann_file in self.annotations_dir.glob("sample_*.json"):
                idx = int(ann_file.stem.split('_')[1])
                with open(ann_file) as f:
                    annotations[idx] = json.load(f)
        
        # Overall stats
        total_samples = len(self.shotbench_data)
        total_reviewed = len(annotations)
        
        # Per-category and per-modality stats
        cat_stats = defaultdict(lambda: {"total": 0, "reviewed": 0, "sb_mistakes": 0, "rs_mistakes": 0})
        mod_stats = defaultdict(lambda: {"total": 0, "reviewed": 0, "sb_mistakes": 0, "rs_mistakes": 0})
        cat_mod_stats = defaultdict(lambda: {"total": 0, "reviewed": 0, "sb_mistakes": 0, "rs_mistakes": 0})
        
        sb_mistake_types = Counter()
        rs_mistake_types = Counter()
        
        for sample in self.shotbench_data:
            idx = sample['index']
            cat = sample['category']
            mod = sample['type']
            
            cat_stats[cat]["total"] += 1
            mod_stats[mod]["total"] += 1
            cat_mod_stats[f"{mod}_{cat}"]["total"] += 1
            
            if idx in annotations:
                ann = annotations[idx]
                cat_stats[cat]["reviewed"] += 1
                mod_stats[mod]["reviewed"] += 1
                cat_mod_stats[f"{mod}_{cat}"]["reviewed"] += 1
                
                if ann.get('shotbench_mistake'):
                    cat_stats[cat]["sb_mistakes"] += 1
                    mod_stats[mod]["sb_mistakes"] += 1
                    cat_mod_stats[f"{mod}_{cat}"]["sb_mistakes"] += 1
                    if ann.get('shotbench_mistake_type'):
                        sb_mistake_types[ann['shotbench_mistake_type']] += 1
                
                if ann.get('refineshot_mistake'):
                    cat_stats[cat]["rs_mistakes"] += 1
                    mod_stats[mod]["rs_mistakes"] += 1
                    cat_mod_stats[f"{mod}_{cat}"]["rs_mistakes"] += 1
                    if ann.get('refineshot_mistake_type'):
                        rs_mistake_types[ann['refineshot_mistake_type']] += 1
        
        return {
            "overall": {
                "total_samples": total_samples,
                "total_reviewed": total_reviewed,
                "pending": total_samples - total_reviewed,
                "sb_mistakes": sum(1 for a in annotations.values() if a.get('shotbench_mistake')),
                "rs_mistakes": sum(1 for a in annotations.values() if a.get('refineshot_mistake'))
            },
            "by_category": dict(cat_stats),
            "by_modality": dict(mod_stats),
            "by_category_modality": dict(cat_mod_stats),
            "sb_mistake_types": dict(sb_mistake_types),
            "rs_mistake_types": dict(rs_mistake_types)
        }

    def serve_media(self, media_path):
        """Serve media file from local directory."""
        try:
            local_path = self.media_dir / media_path
            
            if not local_path.exists():
                self.send_error(404, f"Media not found: {media_path}")
                return
            
            self.send_response(200)
            
            # Detect content type
            content_type, _ = mimetypes.guess_type(str(local_path))
            if not content_type:
                ext = local_path.suffix.lower()
                content_type = {
                    '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
                    '.png': 'image/png', '.gif': 'image/gif',
                    '.webp': 'image/webp', '.bmp': 'image/bmp',
                    '.mp4': 'video/mp4', '.mkv': 'video/x-matroska',
                    '.webm': 'video/webm', '.avi': 'video/x-msvideo',
                    '.mov': 'video/quicktime',
                }.get(ext, 'application/octet-stream')
            
            self.send_header('Content-Type', content_type)
            self.send_header('Accept-Ranges', 'bytes')
            
            file_size = os.path.getsize(local_path)
            self.send_header('Content-Length', str(file_size))
            self.end_headers()
            
            with open(local_path, 'rb') as f:
                self.wfile.write(f.read())
                
        except Exception as e:
            print(f"Error serving media {media_path}: {e}")
            traceback.print_exc()
            self.send_error(500, f"Error serving media")

    def proxy_hf_media(self, media_path):
        """Proxy media from HuggingFace with local caching."""
        try:
            # Check local cache first
            local_path = self.media_dir / media_path
            
            if not local_path.exists():
                # Try to download from HuggingFace
                try:
                    from huggingface_hub import hf_hub_download
                    import shutil
                    
                    downloaded = hf_hub_download(
                        repo_id=SHOTBENCH_REPO,
                        filename=media_path,
                        repo_type="dataset",
                        cache_dir="/tmp/hf_cache"
                    )
                    
                    local_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy(downloaded, local_path)
                    
                except Exception as e:
                    print(f"⚠️  Could not download from HF: {e}")
                    self.send_error(404, f"Media not available: {media_path}")
                    return
            
            self.serve_media(media_path)
            
        except Exception as e:
            print(f"Error proxying media {media_path}: {e}")
            self.send_error(500, f"Error proxying media")

    def send_json_response(self, data):
        """Send JSON response."""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        """Override to customize logging."""
        if "api" in args[0] or self.command == "POST":
            print(f"{self.address_string()} - {format % args}")


SHOTBENCH_REPO = "Vchitect/ShotBench"


def create_handler(data_dir, media_dir, annotations_dir, shotbench_data, refineshot_data):
    """Create a handler with the specified configuration."""
    def handler(*args, **kwargs):
        return ShotBenchViewerHandler(
            *args,
            data_dir=data_dir,
            media_dir=media_dir,
            annotations_dir=annotations_dir,
            shotbench_data=shotbench_data,
            refineshot_data=refineshot_data,
            **kwargs
        )
    return handler


def create_sample_data(data_dir):
    """Create sample data for testing when real data isn't available."""
    import random
    print("📝 Creating sample data for testing...")
    
    samples = []
    categories = CATEGORIES
    modalities = ["image", "video"]
    
    sample_questions = {
        "shot size": "What's the shot size of this shot?",
        "shot framing": "What's the shot framing of this shot?",
        "camera angle": "What's the camera angle of this shot?",
        "lens size": "What's the lens type used in this shot?",
        "lighting type": "What's the lighting type in this shot?",
        "lighting": "What's the lighting condition in this shot?",
        "composition": "What's the composition technique used in this shot?",
        "camera movement": "What's the camera movement in this shot?"
    }
    
    # Options use values matching RefineShot's category.json taxonomy
    sample_options = {
        "shot size": {"A": "Extreme Close Up", "B": "Medium Close Up", "C": "Close Up", "D": "Medium Wide"},
        "shot framing": {"A": "Single", "B": "2 shot", "C": "Over the shoulder", "D": "Group shot"},
        "camera angle": {"A": "Eye Level", "B": "Low Angle", "C": "High Angle", "D": "Dutch Angle"},
        "lens size": {"A": "Wide Angle", "B": "Normal", "C": "Telephoto", "D": "Macro"},
        "lighting type": {"A": "Daylight", "B": "Artificial light", "C": "Moonlight", "D": "Mixed light"},
        "lighting": {"A": "Side light", "B": "Backlight", "C": "Soft light", "D": "Silhouette"},
        "composition": {"A": "Rule of Thirds", "B": "Symmetry", "C": "Leading Lines", "D": "Frame within Frame"},
        "camera movement": {"A": "Pan Left", "B": "Tilt Up", "C": "Dolly In", "D": "Zoom In"}
    }
    
    idx = 1
    for cat in categories:
        for mod in modalities:
            count = 8 if mod == "image" else 3
            for j in range(count):
                ext = "jpg" if mod == "image" else "mp4"
                filename = f"SAMPLE{idx:04d}.{ext}"
                
                samples.append({
                    "index": idx,
                    "type": mod,
                    "path": f"{mod}/{filename}",
                    "question": sample_questions[cat],
                    "options": sample_options[cat],
                    "answer": ["A", "B", "C", "D"][j % 4],
                    "category": cat
                })
                idx += 1
    
    output_path = data_dir / "shotbench.json"
    with open(output_path, 'w') as f:
        json.dump(samples, f, indent=2)
    
    # Generate RefineShot using the real refinement logic
    from download_data import generate_refineshot_from_shotbench, download_refineshot
    categories_json = download_refineshot()
    if categories_json:
        rs_samples = generate_refineshot_from_shotbench(samples, categories_json)
    else:
        # Fallback: create simple variant
        rs_samples = []
        for s in samples:
            rs = s.copy()
            rs['source'] = 'refineshot'
            rs['refined'] = False
            rs_samples.append(rs)
        rs_path = data_dir / "refineshot.json"
        with open(rs_path, 'w') as f:
            json.dump(rs_samples, f, indent=2)
    
    # Reload to get what was saved
    with open(data_dir / "refineshot.json") as f:
        rs_samples = json.load(f)
    
    print(f"   Created {len(samples)} sample ShotBench entries")
    print(f"   Created {len(rs_samples)} sample RefineShot entries")
    
    return samples, rs_samples


def main():
    parser = argparse.ArgumentParser(description="ShotBench & RefineShot Annotation Viewer")
    parser.add_argument("--port", type=int, default=PORT, help=f"Port (default: {PORT})")
    parser.add_argument("--host", type=str, default=HOST, help=f"Host (default: {HOST})")
    parser.add_argument("--data_dir", type=str, default=None, help="Data directory")
    parser.add_argument("--media_dir", type=str, default=None, help="Media directory")
    parser.add_argument("--annotations_dir", type=str, default=None, help="Annotations directory")
    parser.add_argument("--sample-data", action="store_true", help="Use sample data for testing")
    args = parser.parse_args()

    script_dir = Path(__file__).parent.resolve()
    data_dir = Path(args.data_dir) if args.data_dir else script_dir / DATA_DIR
    media_dir = Path(args.media_dir) if args.media_dir else script_dir / MEDIA_DIR
    annotations_dir = Path(args.annotations_dir) if args.annotations_dir else script_dir / ANNOTATIONS_DIR
    
    data_dir.mkdir(parents=True, exist_ok=True)
    media_dir.mkdir(parents=True, exist_ok=True)
    annotations_dir.mkdir(parents=True, exist_ok=True)
    
    # Load datasets
    shotbench_path = data_dir / "shotbench.json"
    refineshot_path = data_dir / "refineshot.json"
    
    if args.sample_data or not shotbench_path.exists():
        if not shotbench_path.exists():
            print("⚠️  No data found. Creating sample data...")
            print("   Run download_data.py first to get real data.\n")
        shotbench_data, refineshot_data = create_sample_data(data_dir)
    else:
        shotbench_data = load_dataset(shotbench_path)
        refineshot_data = load_dataset(refineshot_path) if refineshot_path.exists() else []
    
    os.chdir(script_dir)
    
    handler = create_handler(data_dir, media_dir, annotations_dir, shotbench_data, refineshot_data)
    
    with ReusableTCPServer((args.host, args.port), handler) as httpd:
        print("=" * 70)
        print(f"🎬 ShotBench & RefineShot Annotation Viewer")
        print("=" * 70)
        print(f"💾 Data:             {data_dir.resolve()}")
        print(f"📁 Media:            {media_dir.resolve()}")
        print(f"📝 Annotations:      {annotations_dir.resolve()}")
        print(f"📦 ShotBench:        {len(shotbench_data)} samples")
        print(f"📦 RefineShot:       {len(refineshot_data)} samples")
        print(f"🌐 Server:           http://{args.host}:{args.port}")
        if args.host == "0.0.0.0":
            import socket
            hostname = socket.gethostname()
            try:
                local_ip = socket.gethostbyname(hostname)
                print(f"🔗 Local URL:        http://{local_ip}:{args.port}")
            except:
                pass
            print(f"🔗 Localhost:        http://localhost:{args.port}")
        print("=" * 70)
        print("\n✨ Server running with multi-threading support")
        print("💡 Annotations saved locally in real-time")
        print("💡 Hard refresh (Ctrl+Shift+R / Cmd+Shift+R) to see code changes\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Shutting down server...")
            print("✅ All annotations saved successfully")


if __name__ == "__main__":
    main()