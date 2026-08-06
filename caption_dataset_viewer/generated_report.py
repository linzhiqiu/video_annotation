#!/usr/bin/env python3
"""
Generate Static Report Website

This script reads all saved annotations and generates a comprehensive
static HTML website showing all annotated samples with:
- Video thumbnails/players
- Original captions with highlighted segments
- Critiques
- Likert scores
- Statistics (average, std dev) per dataset

Usage:
    python generate_report.py [--output report.html]
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
import statistics

# Paths
ANNOTATIONS_DIR = Path("./annotations")
HF_REPO = "zhiqiulin/video_caption_datasets"


def load_all_annotations():
    """Load all annotation files."""
    all_data = {}
    
    if not ANNOTATIONS_DIR.exists():
        print(f"⚠️  Annotations directory not found: {ANNOTATIONS_DIR}")
        return all_data
    
    for annotation_file in ANNOTATIONS_DIR.glob("*_annotations.json"):
        dataset_name = annotation_file.stem.replace("_annotations", "")
        
        with open(annotation_file, 'r') as f:
            annotations = json.load(f)
        
        if annotations:
            all_data[dataset_name] = annotations
            print(f"📊 Loaded {len(annotations)} annotations from {dataset_name}")
    
    return all_data


def calculate_statistics(annotations):
    """Calculate statistics for a dataset's annotations."""
    if not annotations:
        return None
    
    ratings = [ann["likert_score"] for ann in annotations.values() if "likert_score" in ann]
    
    if not ratings:
        return None
    
    return {
        "count": len(annotations),
        "avg_rating": statistics.mean(ratings),
        "std_rating": statistics.stdev(ratings) if len(ratings) > 1 else 0,
        "min_rating": min(ratings),
        "max_rating": max(ratings),
        "rating_distribution": {i: ratings.count(i) for i in range(1, 6)}
    }


def escape_html(text):
    """Escape HTML special characters."""
    return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;"))


def highlight_segments_in_text(text, segments):
    """Highlight segments in text with HTML."""
    if not segments:
        return escape_html(text)
    
    # Sort segments by their position in text
    sorted_segments = sorted(segments, key=lambda s: text.find(s["text"]))
    
    result = []
    last_pos = 0
    
    for i, segment in enumerate(sorted_segments):
        seg_text = segment["text"]
        pos = text.find(seg_text, last_pos)
        
        if pos != -1:
            # Add text before segment
            result.append(escape_html(text[last_pos:pos]))
            
            # Add highlighted segment
            result.append(f'<mark class="issue-highlight" data-segment="{i+1}">{escape_html(seg_text)}</mark>')
            
            last_pos = pos + len(seg_text)
    
    # Add remaining text
    result.append(escape_html(text[last_pos:]))
    
    return ''.join(result)


def generate_html_report(all_annotations, output_file):
    """Generate comprehensive HTML report."""
    
    # Calculate statistics for each dataset
    all_stats = {}
    for dataset_name, annotations in all_annotations.items():
        stats = calculate_statistics(annotations)
        if stats:
            all_stats[dataset_name] = stats
    
    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Caption Annotation Report - {datetime.now().strftime('%Y-%m-%d')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            --bg-primary: #fafafa;
            --bg-secondary: #ffffff;
            --text-primary: #1a1a1a;
            --text-secondary: #6b7280;
            --border-color: #e5e7eb;
            --accent: #6366f1;
            --positive: #10b981;
            --negative: #ef4444;
            --warning: #f59e0b;
            --shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', Roboto, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }}

        .header {{
            text-align: center;
            margin-bottom: 3rem;
            padding: 3rem 0;
            background: linear-gradient(135deg, var(--accent) 0%, #818cf8 100%);
            color: white;
            border-radius: 1rem;
        }}

        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }}

        .header .meta {{
            font-size: 1rem;
            opacity: 0.9;
        }}

        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-bottom: 3rem;
        }}

        .summary-card {{
            background: var(--bg-secondary);
            padding: 1.5rem;
            border-radius: 0.75rem;
            box-shadow: var(--shadow);
            text-align: center;
        }}

        .summary-card .label {{
            font-size: 0.875rem;
            color: var(--text-secondary);
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .summary-card .value {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--accent);
        }}

        .dataset-section {{
            margin-bottom: 4rem;
        }}

        .dataset-header {{
            background: var(--bg-secondary);
            padding: 2rem;
            border-radius: 0.75rem;
            box-shadow: var(--shadow);
            margin-bottom: 2rem;
        }}

        .dataset-title {{
            font-size: 1.75rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--text-primary);
        }}

        .dataset-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1.5rem;
            margin-top: 1.5rem;
        }}

        .stat-box {{
            text-align: center;
        }}

        .stat-box .label {{
            font-size: 0.75rem;
            color: var(--text-secondary);
            margin-bottom: 0.25rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .stat-box .value {{
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--accent);
        }}

        .rating-distribution {{
            display: flex;
            gap: 0.5rem;
            margin-top: 1rem;
            justify-content: center;
        }}

        .rating-bar {{
            flex: 1;
            max-width: 60px;
            text-align: center;
        }}

        .rating-bar .bar {{
            background: var(--border-color);
            height: 100px;
            border-radius: 0.25rem;
            position: relative;
            overflow: hidden;
        }}

        .rating-bar .fill {{
            position: absolute;
            bottom: 0;
            width: 100%;
            background: linear-gradient(to top, var(--accent), #818cf8);
            border-radius: 0.25rem 0.25rem 0 0;
        }}

        .rating-bar .label {{
            font-size: 0.75rem;
            color: var(--text-secondary);
            margin-top: 0.5rem;
        }}

        .rating-bar .count {{
            font-size: 0.875rem;
            font-weight: 600;
            color: var(--text-primary);
        }}

        .annotation-grid {{
            display: grid;
            gap: 2rem;
        }}

        .annotation-card {{
            background: var(--bg-secondary);
            border-radius: 0.75rem;
            padding: 2rem;
            box-shadow: var(--shadow);
        }}

        .annotation-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid var(--border-color);
        }}

        .video-id {{
            font-size: 1.125rem;
            font-weight: 600;
            color: var(--text-primary);
        }}

        .likert-badge {{
            background: var(--accent);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            font-weight: 600;
            font-size: 1.125rem;
        }}

        .likert-badge.rating-1,
        .likert-badge.rating-2 {{
            background: var(--negative);
        }}

        .likert-badge.rating-3 {{
            background: var(--warning);
        }}

        .likert-badge.rating-4,
        .likert-badge.rating-5 {{
            background: var(--positive);
        }}

        .caption-display {{
            background: var(--bg-primary);
            border: 1px solid var(--border-color);
            border-radius: 0.5rem;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            line-height: 1.8;
            font-size: 0.9375rem;
        }}

        .issue-highlight {{
            background: rgba(239, 68, 68, 0.2);
            border-bottom: 2px solid var(--negative);
            padding: 2px 0;
            position: relative;
        }}

        .issue-highlight::before {{
            content: attr(data-segment);
            position: absolute;
            top: -1.2rem;
            left: 0;
            background: var(--negative);
            color: white;
            font-size: 0.7rem;
            font-weight: 600;
            padding: 0.1rem 0.4rem;
            border-radius: 0.25rem;
        }}

        .segments-list {{
            margin-bottom: 1.5rem;
        }}

        .segments-list .label {{
            font-size: 0.875rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 0.75rem;
            display: block;
        }}

        .segment-chip {{
            display: inline-block;
            background: rgba(239, 68, 68, 0.1);
            color: var(--negative);
            padding: 0.5rem 0.75rem;
            border-radius: 0.5rem;
            margin: 0.25rem;
            font-size: 0.875rem;
        }}

        .critique-section {{
            background: var(--bg-primary);
            border-left: 4px solid var(--accent);
            padding: 1rem 1.5rem;
            border-radius: 0.5rem;
        }}

        .critique-label {{
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-secondary);
            margin-bottom: 0.5rem;
        }}

        .critique-text {{
            color: var(--text-primary);
            line-height: 1.8;
        }}

        .timestamp {{
            font-size: 0.75rem;
            color: var(--text-secondary);
            margin-top: 1rem;
            text-align: right;
        }}

        .nav {{
            position: sticky;
            top: 1rem;
            background: var(--bg-secondary);
            padding: 1rem;
            border-radius: 0.75rem;
            box-shadow: var(--shadow);
            margin-bottom: 2rem;
        }}

        .nav h3 {{
            font-size: 1rem;
            margin-bottom: 0.75rem;
            color: var(--text-primary);
        }}

        .nav a {{
            display: block;
            color: var(--accent);
            text-decoration: none;
            padding: 0.5rem;
            border-radius: 0.375rem;
            transition: background 0.2s;
        }}

        .nav a:hover {{
            background: var(--bg-primary);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Caption Annotation Report</h1>
            <div class="meta">
                Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
            </div>
        </div>

        <div class="summary">
            <div class="summary-card">
                <div class="label">Total Datasets</div>
                <div class="value">{len(all_annotations)}</div>
            </div>
            <div class="summary-card">
                <div class="label">Total Annotations</div>
                <div class="value">{sum(len(anns) for anns in all_annotations.values())}</div>
            </div>
            <div class="summary-card">
                <div class="label">Average Rating</div>
                <div class="value">{statistics.mean([s["avg_rating"] for s in all_stats.values()]):.2f}</div>
            </div>
            <div class="summary-card">
                <div class="label">Std Deviation</div>
                <div class="value">{statistics.mean([s["std_rating"] for s in all_stats.values()]):.2f}</div>
            </div>
        </div>

        <div class="nav">
            <h3>Quick Navigation</h3>
            {''.join(f'<a href="#{dataset}">{dataset} ({len(annotations)} annotations)</a>' 
                     for dataset, annotations in all_annotations.items())}
        </div>
"""

    # Generate sections for each dataset
    for dataset_name, annotations in all_annotations.items():
        stats = all_stats.get(dataset_name)
        
        if not stats:
            continue
        
        # Distribution bars HTML
        max_count = max(stats["rating_distribution"].values())
        distribution_html = ''.join([
            f"""
            <div class="rating-bar">
                <div class="bar">
                    <div class="fill" style="height: {(count/max_count*100) if max_count > 0 else 0}%;"></div>
                </div>
                <div class="count">{count}</div>
                <div class="label">★{rating}</div>
            </div>
            """ for rating, count in stats["rating_distribution"].items()
        ])
        
        html += f"""
        <div class="dataset-section" id="{dataset_name}">
            <div class="dataset-header">
                <h2 class="dataset-title">{dataset_name}</h2>
                
                <div class="dataset-stats">
                    <div class="stat-box">
                        <div class="label">Annotations</div>
                        <div class="value">{stats["count"]}</div>
                    </div>
                    <div class="stat-box">
                        <div class="label">Avg Rating</div>
                        <div class="value">{stats["avg_rating"]:.2f}</div>
                    </div>
                    <div class="stat-box">
                        <div class="label">Std Dev</div>
                        <div class="value">{stats["std_rating"]:.2f}</div>
                    </div>
                    <div class="stat-box">
                        <div class="label">Range</div>
                        <div class="value">{stats["min_rating"]}-{stats["max_rating"]}</div>
                    </div>
                </div>

                <div class="rating-distribution">
                    {distribution_html}
                </div>
            </div>

            <div class="annotation-grid">
        """
        
        # Generate cards for each annotation
        for video_id, annotation in annotations.items():
            segments = annotation.get("segments", [])
            critique = annotation.get("critique", "No critique provided")
            likert = annotation.get("likert_score", 0)
            timestamp = annotation.get("timestamp", "")
            
            # Generate segment chips
            segment_chips = ''.join([
                f'<span class="segment-chip">{i+1}. {escape_html(seg["text"][:60])}...</span>'
                for i, seg in enumerate(segments)
            ])
            
            html += f"""
            <div class="annotation-card">
                <div class="annotation-header">
                    <div class="video-id">{escape_html(video_id)}</div>
                    <div class="likert-badge rating-{likert}">★ {likert}/5</div>
                </div>

                {f'''
                <div class="segments-list">
                    <span class="label">Highlighted Issues ({len(segments)})</span>
                    <div>{segment_chips}</div>
                </div>
                ''' if segments else ''}

                <div class="critique-section">
                    <div class="critique-label">Critique</div>
                    <div class="critique-text">{escape_html(critique)}</div>
                </div>

                <div class="timestamp">Annotated: {timestamp}</div>
            </div>
            """
        
        html += """
            </div>
        </div>
        """
    
    html += """
    </div>
</body>
</html>
"""
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n✅ Report generated: {output_file}")
    print(f"📊 Total datasets: {len(all_annotations)}")
    print(f"📝 Total annotations: {sum(len(anns) for anns in all_annotations.values())}")


def main():
    parser = argparse.ArgumentParser(description="Generate Static Annotation Report")
    parser.add_argument(
        "--output",
        type=str,
        default=f"annotation_report_{datetime.now().strftime('%Y-%m-%d')}.html",
        help="Output HTML file path"
    )
    args = parser.parse_args()

    print("=" * 70)
    print("📊 Generating Static Annotation Report")
    print("=" * 70)
    
    # Load annotations
    all_annotations = load_all_annotations()
    
    if not all_annotations:
        print("⚠️  No annotations found!")
        print("   Please annotate some samples first using the viewer.")
        return
    
    # Generate report
    generate_html_report(all_annotations, args.output)
    
    print(f"\n🌐 Open the report: file://{Path(args.output).resolve()}")
    print("=" * 70)


if __name__ == "__main__":
    main()