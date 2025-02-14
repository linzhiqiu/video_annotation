import os
from typing import Dict, List, Any
import logging
from flask import Flask, render_template, send_from_directory
from batch import Batch
from video_data import VideoData
from scripts.process_ndjson import process_ndjson_files
from ..params.visualization_params import VisualizationParams
from label import Label
import base64

class CombinationVisualizer:
    """Class for visualizing label combinations as a correlation matrix."""
    
    def __init__(self, config_path: str, batch_folder: str = None):
        self.config_path = config_path  # Store the config path
        self.config = VisualizationParams.from_yaml(config_path)
        
        # Process NDJSON files during initialization
        logging.info("Processing NDJSON files...")
        data_config = self.config['data']
        
        # Use batch folder from constructor or config
        batch_folder = batch_folder or data_config.get('batch_folder')
        
        # If batch folder is provided, use its ndjson and issues directories
        if batch_folder:
            ndjson_dir = os.path.join(batch_folder, 'ndjson')
            issues_dir = os.path.join(batch_folder, 'issues_ndjson')
            if not os.path.exists(ndjson_dir) or not os.path.exists(issues_dir):
                raise ValueError(f"Batch folder {batch_folder} must contain 'ndjson' and 'issues_ndjson' directories")
            logging.info(f"Using batch folder: {batch_folder}")
            logging.info(f"NDJSON directory: {ndjson_dir}")
            logging.info(f"Issues directory: {issues_dir}")
        else:
            ndjson_dir = data_config.get('ndjson_dir', 'exports/ndjson')
            issues_dir = data_config.get('issues_dir', 'exports/issues_ndjson')
            logging.info(f"No batch folder specified, using default directories:")
            logging.info(f"NDJSON directory: {ndjson_dir}")
            logging.info(f"Issues directory: {issues_dir}")
            
        self.all_videos = process_ndjson_files(
            ndjson_dir, 
            issues_dir
        )
        logging.info(f"Loaded {len(self.all_videos)} total videos from NDJSON files")
        
        self.labels = Label.load_all_labels()
        self.app = Flask(__name__, template_folder='../templates')
        self.setup_routes()
        
    def setup_routes(self):
        @self.app.route('/')
        def index():
            """Show the correlation matrix."""
            matrix_data = self.generate_correlation_matrix()
            return render_template('correlation_matrix.html', 
                                matrix_data=matrix_data,
                                labels=self.config['labels'])

        @self.app.route('/visualize/<path:label1>/<path:label2>')
        def visualize_combination(label1: str, label2: str):
            """Show detailed visualization for a label combination."""
            try:
                # Decode the base64 encoded labels
                decoded_label1 = base64.b64decode(label1).decode('utf-8')
                decoded_label2 = base64.b64decode(label2).decode('utf-8')
                
                # Get the label objects
                label1_obj = self._get_label(decoded_label1)
                label2_obj = self._get_label(decoded_label2)
                
                # Create batch
                batch = self.create_batch(self.all_videos)
                
                # Find positive and negative videos
                positive_videos = []
                negative_videos = []
                
                for name, video in batch:
                    try:
                        is_positive_1 = label1_obj.pos_rule(video)
                        is_positive_2 = label2_obj.pos_rule(video)
                        
                        if is_positive_1 and is_positive_2:
                            positive_videos.append(name)
                        else:
                            negative_videos.append(name)
                    except Exception as e:
                        logging.error(f"Error checking rules for video {name}: {str(e)}")
                
                return render_template('combination_visualization.html',
                                    label1=decoded_label1,
                                    label2=decoded_label2,
                                    positive_videos=positive_videos,
                                    negative_videos=negative_videos)
                                    
            except Exception as e:
                logging.error(f"Error visualizing combination: {str(e)}")
                return f"Error: {str(e)}", 400

        @self.app.route('/videos/<path:video_name>')
        def serve_video(video_name):
            """Serve video files."""
            try:
                # Get videos_dir from config and convert to absolute path
                videos_dir = self.config['data']['videos_dir']
                if not os.path.isabs(videos_dir):
                    # Get the directory where the config file is located
                    config_dir = os.path.dirname(os.path.abspath(self.config_path))
                    # Resolve the relative path from the config directory
                    videos_dir = os.path.abspath(os.path.join(config_dir, videos_dir))
                
                logging.info(f"Resolved videos directory to: {videos_dir}")
                
                if not os.path.exists(videos_dir):
                    raise FileNotFoundError(f"Videos directory not found: {videos_dir}")
                
                # Search for the video file recursively
                for root, _, files in os.walk(videos_dir):
                    if video_name in files:
                        # Found the video, serve it from its subdirectory
                        relative_path = os.path.relpath(root, videos_dir)
                        if relative_path == '.':
                            # Video is in the root directory
                            return send_from_directory(videos_dir, video_name, mimetype='video/mp4')
                        else:
                            # Video is in a subdirectory
                            return send_from_directory(
                                os.path.join(videos_dir, relative_path),
                                video_name,
                                mimetype='video/mp4'
                            )
                
                # If we get here, the video wasn't found
                raise FileNotFoundError(f"Video file not found: {video_name}")
            
            except Exception as e:
                logging.error(f"Error serving video {video_name}: {str(e)}")
                return f"Error: Could not serve video {video_name}", 404

    def _get_label(self, label_path: str):
        """Get the label class by path."""
        try:
            # Split path and get components
            parts = label_path.split('/')
            
            # Start from root of labels
            current = self.labels
            
            # Get the first component to determine which root to use
            if parts[0] == 'cam_setup':
                current = self.labels.cam_setup
                # Skip the cam_setup part since we're already there
                parts = parts[1:]
            elif parts[0] == 'cam_motion':
                current = self.labels.cam_motion
                # Skip the cam_motion part since we're already there
                parts = parts[1:]
            else:
                raise ValueError(f"Invalid label path: {label_path}. Must start with 'cam_setup' or 'cam_motion'")
            
            # Navigate through remaining parts
            for part in parts:
                if part:
                    current = getattr(current, part)
                    logging.info(f"Successfully accessed {part}")
            
            return current
        
        except AttributeError as e:
            logging.error(f"Failed to get label '{label_path}': {str(e)}")
            # Print the available attributes for debugging
            if current:
                available = [attr for attr in dir(current) if not attr.startswith('_')]
                logging.error(f"Available attributes at failed point: {available}")
            raise ValueError(f"Label '{label_path}' not found")

    def generate_correlation_matrix(self):
        """Generate a matrix showing number of videos positive for each label pair."""
        labels = self.config['labels']
        matrix = []
        
        logging.info("Generating correlation matrix...")
        batch = self.create_batch(self.all_videos)
        
        # For each pair of labels
        for row_label in labels:
            row = []
            row_label_obj = self._get_label(row_label)
            
            for col_label in labels:
                col_label_obj = self._get_label(col_label)
                
                # Count videos positive for both labels
                positive_count = 0
                for name, video in batch:
                    try:
                        if row_label == col_label:
                            if row_label_obj.pos_rule(video):
                                positive_count += 1
                        else:
                            if row_label_obj.pos_rule(video) and col_label_obj.pos_rule(video):
                                positive_count += 1
                    except Exception as e:
                        logging.error(f"Error checking rules for video {name}: {str(e)}")
                
                cell = {
                    'row_label': row_label,  # Store complete row label path
                    'col_label': col_label,  # Store complete column label path
                    'count': positive_count
                }
                row.append(cell)
                
                if row_label == col_label:
                    logging.info(f"Label {row_label}: {positive_count} positive videos")
                else:
                    logging.info(f"Label pair ({row_label}, {col_label}): {positive_count} positive videos")
            
            matrix.append(row)
        
        return matrix

    def create_batch(self, all_videos: Dict[str, VideoData]) -> Batch:
        """Create a batch from all available videos."""
        logging.info(f"Creating batch with all {len(all_videos)} videos")
        batch = Batch(all_videos)
        logging.info(f"Created batch with {len(batch)} videos")
        return batch

    def find_video_path(self, video_name: str) -> tuple:
        """Find a video file by searching through subdirectories.
        Returns a tuple of (directory_path, filename) if found, (None, None) if not found."""
        videos_dir = self.config['data']['videos_dir']
        logging.info(f"Searching for video {video_name} in {videos_dir}")
        
        # Walk through all subdirectories
        for root, _, files in os.walk(videos_dir):
            if video_name in files:
                logging.info(f"Found video {video_name} in directory {root}")
                return root, video_name
                
        logging.warning(f"Video {video_name} not found in {videos_dir} or its subdirectories")
        return None, None

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
            }
        }
        return details

    def run_server(self):
        """Run the Flask server."""
        logging.info("\nStarting server...")
        server_config = self.config.get('server', {})
        host = server_config.get('host', 'localhost')
        port = server_config.get('port', 8086)
        
        self.app.run(host=host, port=port) 