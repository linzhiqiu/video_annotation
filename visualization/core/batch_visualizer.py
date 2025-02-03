import os
from typing import Dict, List, Any
from datetime import datetime
import json
import logging
from flask import Flask, render_template, jsonify, send_from_directory
from batch import Batch
from video_data import VideoData
from process_ndjson import process_ndjson_files
from ..params.visualization_params import VisualizationParams
from label import Label  # Add this import

class BatchVisualizer:
    """Class for visualizing batches of videos based on labels."""
    
    def __init__(self, config_path: str):
        self.config = VisualizationParams.from_yaml(config_path)
        self.labels = Label.load_all_labels()  # Load all labels
        self.app = Flask(__name__, 
                        template_folder='../templates',  
                        static_folder='../static')
        
        # Process NDJSON files during initialization
        logging.info("Processing NDJSON files...")
        data_config = self.config['data']
        self.all_videos = process_ndjson_files(
            data_config['ndjson_dir'], 
            data_config['issues_dir']
        )
        logging.info(f"Loaded {len(self.all_videos)} total videos from NDJSON files")
        
        self.video_details = None
        self.current_label = None
        self.setup_routes()
        
    def setup_routes(self):
        """Setup Flask routes."""
        
        @self.app.route('/')
        def index():
            """Show label selection interface."""
            # Get all available labels recursively
            label_paths = []
            labels_dir = 'labels'
            
            for root, _, files in os.walk(labels_dir):
                for file in files:
                    if file.endswith('.json'):
                        # Get relative path from labels directory
                        rel_path = os.path.relpath(os.path.join(root, file), labels_dir)
                        label_id = os.path.splitext(rel_path)[0]
                        readable_name = label_id.replace('/', ' > ').replace('_', ' ').title()
                        label_paths.append({
                            'id': label_id,
                            'name': readable_name,
                            'path': os.path.join(root, file)
                        })
            
            return render_template('label_selection.html', labels=label_paths)

        @self.app.route('/visualize/<path:label_id>')
        def visualize(label_id):
            """Show visualization for specific label."""
            try:
                # Set current label
                self.current_label = self._get_label(label_id.replace('/', '.'))
                
                # Generate visualization for this label
                self.generate_visualization()
                
                if not self.video_details:
                    return "Failed to generate visualization data", 500
                
                return render_template('index.html',
                                    categories=self._organize_videos(),
                                    label_info=self._get_label_info(),
                                    lazy_load=self.config.get('visualization', {}).get('lazy_load_videos', True))
            except Exception as e:
                logging.error(f"Error visualizing label: {str(e)}")
                return f"Error loading label: {str(e)}", 400

        @self.app.route('/videos/<path:video_name>')
        def serve_video(video_name):
            """Serve video files."""
            videos_dir = self.config['data']['videos_dir']
            
            # Get the actual path of the video from our stored paths
            video_paths = self.config.get('_video_paths', {})
            if video_name in video_paths:
                # If we have a stored subdirectory path for this video
                subdir = video_paths[video_name]
                full_path = os.path.join(videos_dir, subdir)
                logging.info(f"Serving video from: {full_path}, filename: {video_name}")
                return send_from_directory(
                    full_path,
                    video_name,
                    mimetype='video/mp4',
                    as_attachment=False
                )
            
            # Fallback to direct path
            logging.info(f"Serving video directly from: {videos_dir}, filename: {video_name}")
            return send_from_directory(
                videos_dir,
                video_name,
                mimetype='video/mp4',
                as_attachment=False
            )

        @self.app.route('/api/categories')
        def get_categories():
            """Get video categorization."""
            if not self.video_details:
                return jsonify({'error': 'No visualization data available'})
            
            categories = {
                'positive': [],
                'negative': [],
                'easy_negative': {},
                'hard_negative': {}
            }
            
            for name, details in self.video_details.items():
                category = details['category']
                if category == 'positive':
                    categories['positive'].append(name)
                elif category == 'negative':
                    categories['negative'].append(name)
                elif category.startswith('easy_negative_'):
                    rule_name = category.replace('easy_negative_', '')
                    if rule_name not in categories['easy_negative']:
                        categories['easy_negative'][rule_name] = []
                    categories['easy_negative'][rule_name].append(name)
                elif category.startswith('hard_negative_'):
                    rule_name = category.replace('hard_negative_', '')
                    if rule_name not in categories['hard_negative']:
                        categories['hard_negative'][rule_name] = []
                    categories['hard_negative'][rule_name].append(name)
                    
            return jsonify(categories)

        @self.app.route('/api/video/<video_name>')
        def get_video_details(video_name):
            """Get details for a specific video."""
            if not self.video_details or video_name not in self.video_details:
                return jsonify({'error': 'Video not found'})
            return jsonify(self.video_details[video_name])

    def run_server(self):
        """Run the Flask server."""
        logging.info("\nStarting server...")
        server_config = self.config.get('server', {})
        host = server_config.get('host', 'localhost')
        port = server_config.get('port', 8085)
        
        self.app.run(host=host, port=port)
        
    def _get_label(self, label_name: str):
        """Get the label class by name."""
        try:
            # Navigate through the label hierarchy using dots
            current = self.labels
            for part in label_name.split('.'):
                current = getattr(current, part)
            return current
        except AttributeError:
            raise ValueError(
                f"Label '{label_name}' not found. Available labels:\n{self.labels}"
            )
    
    def _get_video_details(self, video: VideoData) -> Dict[str, Any]:
        """Extract all relevant details from a video."""
        details = {
            'camera_motion': {
                attr: getattr(video.cam_motion, attr)
                for attr in dir(video.cam_motion)
                if not attr.startswith('_') and not callable(getattr(video.cam_motion, attr))
            },
            'camera_setup': {
                attr: getattr(video.cam_setup, attr)
                for attr in dir(video.cam_setup)
                if not attr.startswith('_') and not callable(getattr(video.cam_setup, attr))
            },
            'lighting_setup': {}  # Default empty dict if light_setup is not set
        }
        
        # Try to get lighting setup details if available
        try:
            details['lighting_setup'] = {
                attr: getattr(video.light_setup, attr)
                for attr in dir(video.light_setup)
                if not attr.startswith('_') and not callable(getattr(video.light_setup, attr))
            }
        except AttributeError:
            logging.info(f"Light setup not set for video, using default empty values")
            
        return details

    def create_batch(self, all_videos: Dict[str, VideoData]) -> Batch:
        """Create a batch based on configuration."""
        # Get video names from config
        logging.info("Getting video names from config...")
        video_names = VisualizationParams.get_video_names(self.config)
        
        if not video_names:
            raise ValueError("No video names found in config")
            
        logging.info(f"Found {len(video_names)} videos in video names file: {video_names}")
        
        # Create batch
        batch = Batch.create(
            all_videos=all_videos,
            video_names=video_names,
            approver=self.config.get('constraints', {}).get('approver'),
            time_range=VisualizationParams.get_time_range(self.config.get('constraints', {}))
        )
        
        logging.info(f"Created batch with {len(batch)} videos")
        logging.info(f"Batch video names: {batch.get_video_names()}")
        return batch
    
    def categorize_videos(self, batch: Batch) -> Dict[str, Dict[str, Any]]:
        """Categorize videos and collect their details."""
        video_details = {}
        
        logging.info("\nStarting video categorization:")
        logging.info(f"Batch size: {len(batch)}")
        
        for name, video in batch:
            logging.info(f"\nProcessing video: {name}")
            try:
                # Get all video details
                details = self._get_video_details(video)
                logging.info("Got video details")
                
                # Debug video attributes
                logging.info("Video attributes:")
                logging.info(f"  Camera motion: {video.cam_motion.camera_movement}")
                logging.info(f"  Forward/Backward: {video.cam_motion.camera_forward_backward}")
                logging.info(f"  Camera angle: {video.cam_setup.camera_angle_start}")
                logging.info(f"  Steadiness: {video.cam_motion.steadiness}")
                
                # Determine category using label rules
                category = 'uncategorized'  # Default category
                logging.info("Checking label rules:")
                
                # Debug positive rule evaluation
                pos_result = self.current_label.pos_rule(video)
                logging.info(f"Positive rule result: {pos_result}")
                
                # Debug negative rule evaluation
                neg_result = self.current_label.neg_rule(video)
                logging.info(f"Negative rule result: {neg_result}")
                
                if pos_result:
                    category = 'positive'
                    logging.info("Categorized as positive")
                elif neg_result:
                    category = 'negative'
                    logging.info("Categorized as negative")
                    
                    # Check for easy negative subcategories
                    for rule_name, rule in self.current_label.easy_neg_rules.items():
                        rule_result = rule(video)
                        logging.info(f"Easy negative rule '{rule_name}' result: {rule_result}")
                        if rule_result:
                            category = f'easy_negative_{rule_name}'
                            logging.info(f"Categorized as easy negative: {rule_name}")
                            break
                            
                    # Check for hard negative subcategories
                    for rule_name, rule in self.current_label.hard_neg_rules.items():
                        rule_result = rule(video)
                        logging.info(f"Hard negative rule '{rule_name}' result: {rule_result}")
                        if rule_result:
                            category = f'hard_negative_{rule_name}'
                            logging.info(f"Categorized as hard negative: {rule_name}")
                            break
                
                # Add reason for uncategorized videos
                if category == 'uncategorized':
                    reason = []
                    if video.cam_motion.camera_movement not in ['major_simple', 'major_complex']:
                        reason.append(f"Invalid camera movement: {video.cam_motion.camera_movement}")
                    if video.cam_motion.camera_forward_backward not in ['forward', 'backward']:
                        reason.append(f"Invalid forward/backward motion: {video.cam_motion.camera_forward_backward}")
                    if video.cam_setup.camera_angle_start in ['bird_eye_angle', 'worm_eye_angle', 'unknown']:
                        reason.append(f"Invalid camera angle: {video.cam_setup.camera_angle_start}")
                    if video.cam_motion.steadiness in ['unsteady', 'very_unsteady']:
                        reason.append(f"Invalid steadiness: {video.cam_motion.steadiness}")
                    logging.info(f"Video uncategorized due to: {', '.join(reason)}")
                
                video_details[name] = {
                    'details': details,
                    'category': category,
                    'video_path': self.get_video_path(name),
                    'categorization_reason': reason if category == 'uncategorized' else None
                }
                logging.info(f"Added video to details with category: {category}")
                
            except Exception as e:
                logging.error(f"Error processing video {name}: {str(e)}")
                logging.error(f"Error type: {type(e)}")
                import traceback
                logging.error(f"Traceback: {traceback.format_exc()}")
                
        logging.info(f"\nFinished categorization. Processed {len(video_details)} videos")
        return video_details
    
    def get_video_path(self, video_name: str) -> str:
        """Get the full path to a video file."""
        videos_dir = self.config['data']['videos_dir']
        if not videos_dir:
            raise ValueError("Videos directory not specified in config")
            
        # Use stored path from earlier search if available
        video_paths = self.config.get('_video_paths', {})
        if video_name in video_paths:
            full_path = os.path.join(videos_dir, video_paths[video_name], video_name)
            logging.info(f"Found video in path: {full_path}")
            return full_path
            
        # Fallback to direct path
        full_path = os.path.join(videos_dir, video_name)
        logging.info(f"Using direct video path: {full_path}")
        return full_path
    
    def generate_visualization(self):
        """Generate visualization data for the batch."""
        # Create batch with constraints
        batch = self.create_batch(self.all_videos)
        
        # Get detailed categorization
        self.video_details = self.categorize_videos(batch)
        
        # Log summary statistics
        category_counts = {}
        for details in self.video_details.values():
            category = details['category']
            category_counts[category] = category_counts.get(category, 0) + 1
            
        logging.info("\nVisualization data generated:")
        logging.info(f"Total videos in batch: {len(batch)}")
        logging.info("Categories:")
        for category, count in category_counts.items():
            logging.info(f"  {category}: {count} videos")
            
        # Debug: Print out the full visualization data
        logging.info("\nFull visualization data:")
        logging.info("Label information:")
        label_info = {
            'name': self.current_label.label_name,
            'description': self.current_label.label,
            'positive_rule': self.current_label.pos_rule.rule,
            'negative_rule': self.current_label.neg_rule.rule,
            'easy_negative_rules': {k: v.rule for k, v in self.current_label.easy_neg_rules.items()},
            'hard_negative_rules': {k: v.rule for k, v in self.current_label.hard_neg_rules.items()}
        }
        logging.info(json.dumps(label_info, indent=2))
        
        logging.info("\nVideo details:")
        for video_name, details in self.video_details.items():
            logging.info(f"\nVideo: {video_name}")
            logging.info(f"Category: {details['category']}")
            logging.info(f"Video path: {details['video_path']}")
            logging.info("Details:")
            logging.info(json.dumps(details['details'], indent=2))
            
        # Verify self.video_details is not None
        if self.video_details is None:
            logging.error("self.video_details is None after generation!")
        else:
            logging.info(f"\nNumber of videos in self.video_details: {len(self.video_details)}")

    def _organize_videos(self):
        """Organize videos by category."""
        categories = {
            'positive': [],
            'negative': [],
            'easy_negative': [],
            'hard_negative': [],
            'uncategorized': []
        }
        
        for name, details in self.video_details.items():
            category = details['category']
            video_info = {
                'name': name,
                'details': details['details'],
                'categorization_reason': details.get('categorization_reason')
            }
            
            if category == 'positive':
                categories['positive'].append(video_info)
            elif category == 'negative':
                categories['negative'].append(video_info)
            elif category.startswith('easy_negative_'):
                categories['easy_negative'].append(video_info)
            elif category.startswith('hard_negative_'):
                categories['hard_negative'].append(video_info)
            else:
                categories['uncategorized'].append(video_info)
        
        # Remove empty categories
        categories = {k: v for k, v in categories.items() if v}
        
        return categories

    def _get_label_info(self):
        """Get label information."""
        return {
            'name': self.current_label.label_name,
            'description': self.current_label.label,
            'positive_rule': self.current_label.pos_rule.rule,
            'negative_rule': self.current_label.neg_rule.rule,
            'easy_negative_rules': {k: v.rule for k, v in self.current_label.easy_neg_rules.items()},
            'hard_negative_rules': {k: v.rule for k, v in self.current_label.hard_neg_rules.items()}
        } 