import os
from typing import Dict, List, Any
from datetime import datetime
import json
import logging
from flask import Flask, render_template, jsonify, send_from_directory, request
import shutil
from batch import Batch
from video_data import VideoData
from scripts.process_ndjson import process_ndjson_files
from ..params.visualization_params import VisualizationParams
from label import Label  # Add this import

class BatchVisualizer:
    """Class for visualizing batches of videos based on labels."""
    
    def __init__(self, config_path: str, batch_folder: str = None):
        self.config = VisualizationParams.from_yaml(config_path)
        self.labels = Label.load_all_labels()  # Load all labels
        self.app = Flask(__name__, 
                        template_folder='../templates',  
                        static_folder='../static')
        
        # Process NDJSON files during initialization
        logging.info("Processing NDJSON files...")
        data_config = self.config['data']
        
        # Use batch folder from constructor or config
        batch_folder = batch_folder or data_config.get('batch_folder')
        
        # If batch folder is provided, use its ndjson and issues directories
        if batch_folder:
            ndjson_dir = os.path.join(batch_folder, 'ndjson')
            issues_dir = os.path.join(batch_folder, 'issues_ndjson')
            batch_configs_dir = os.path.join(batch_folder, 'batch_configs')
            
            # Check required directories exist
            if not os.path.exists(ndjson_dir) or not os.path.exists(issues_dir):
                raise ValueError(f"Batch folder {batch_folder} must contain 'ndjson' and 'issues_ndjson' directories")
            if not os.path.exists(batch_configs_dir):
                raise ValueError(f"Batch folder {batch_folder} must contain 'batch_configs' directory")
                
            logging.info(f"Using batch folder: {batch_folder}")
            logging.info(f"NDJSON directory: {ndjson_dir}")
            logging.info(f"Issues directory: {issues_dir}")
            logging.info(f"Batch configs directory: {batch_configs_dir}")
            
            # Get YAML configs from batch_configs directory
            yaml_configs = []
            # for file in os.listdir(batch_configs_dir):
            #     if file.endswith('.yaml'):
            #         yaml_configs.append(os.path.join(batch_configs_dir, file))
            # logging.info(f"Found {len(yaml_configs)} YAML configs in batch_configs directory")
            
        else:
            ndjson_dir = data_config.get('ndjson_dir', 'exports/ndjson')
            issues_dir = data_config.get('issues_dir', 'exports/issues_ndjson')
            yaml_configs = []
            logging.info(f"No batch folder specified, using default directories:")
            logging.info(f"NDJSON directory: {ndjson_dir}")
            logging.info(f"Issues directory: {issues_dir}")
            
        # Create batch and get video data
        batch = Batch.from_configs(yaml_configs, ndjson_dir, issues_dir)
        self.all_videos = batch.get_all_videos()
        logging.info(f"Loaded {len(self.all_videos)} total videos from NDJSON files")
        
        # Try to load state file if available
        self.state = None
        state_path = self.config.get('saved_states', {}).get('load_path')
        if state_path:
            # Make path absolute relative to config file directory
            config_dir = os.path.dirname(os.path.abspath(config_path))
            state_path = os.path.join(config_dir, state_path)
            
            if os.path.exists(state_path):
                logging.info(f"Loading state from {state_path}")
                with open(state_path, 'r') as f:
                    self.state = json.load(f)
                logging.info(f"Loaded state with {len(self.state)} labels")
            else:
                logging.info(f"State file not found at {state_path}")
        
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

        @self.app.route('/export_videos/<path:label_id>', methods=['POST'])
        def export_videos(label_id):
            """Export video names to a JSON file and copy label JSON."""
            try:
                # Get export configuration
                export_config = self.config.get('visualization', {}).get('export', {})
                local_save = export_config.get('local_save', False)
                allow_download = export_config.get('allow_download', True)
                
                if not local_save and not allow_download:
                    return jsonify({
                        'success': False,
                        'message': 'No export method enabled in configuration'
                    }), 400

                # Format label name for folder
                label_name = label_id.replace('/', '_')
                
                # Load the full label JSON file
                label_parts = label_id.split('/')
                label_json_path = os.path.join('labels', *label_parts) + '.json'
                label_data = {}
                if os.path.exists(label_json_path):
                    with open(label_json_path, 'r') as f:
                        label_data = json.load(f)
                
                # Organize videos by category
                video_categories = {
                    'positive': [],
                    'negative': [],
                    'easy_negative': [],
                    'hard_negative': [],
                    'uncategorized': []
                }
                
                # Sort videos into categories
                for name, details in self.video_details.items():
                    category = details['category']
                    if category == 'positive':
                        video_categories['positive'].append(name)
                    elif category == 'negative':
                        video_categories['negative'].append(name)
                    elif category.startswith('easy_negative_'):
                        video_categories['easy_negative'].append(name)
                    elif category.startswith('hard_negative_'):
                        video_categories['hard_negative'].append(name)
                    else:
                        video_categories['uncategorized'].append(name)
                
                # Remove empty categories
                video_categories = {k: v for k, v in video_categories.items() if v}
                
                # Create export data
                export_data = {
                    'label_info': {
                        'name': label_data.get('label_name', ''),
                        'label': label_data.get('label', ''),
                        'definition_questions': label_data.get('def_question', []),
                        'alternative_questions': label_data.get('alt_question', []),
                        'definition_prompts': label_data.get('def_prompt', []),
                        'alternative_prompts': label_data.get('alt_prompt', []),
                        'positive_rule': label_data.get('pos_rule_str', ''),
                        'negative_rule': label_data.get('neg_rule_str', ''),
                        'easy_negative_rules': label_data.get('easy_neg_rule_str', {}),
                        'hard_negative_rules': label_data.get('hard_neg_rule_str', {})
                    },
                    'video_categories': video_categories,
                    'export_timestamp': datetime.now().strftime('%Y%m%d_%H%M%S')
                }

                if local_save:
                    # Get label directory from config
                    label_dir = self.config['data'].get('label_dir', 'label_dirs')
                    if not os.path.exists(label_dir):
                        os.makedirs(label_dir)
                    
                    # Create timestamp for unique folder
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    
                    # Create label-specific directory with timestamp
                    label_export_dir = os.path.join(label_dir, f"{label_name}_{timestamp}")
                    os.makedirs(label_export_dir)
                    
                    # Save export data to JSON file
                    export_path = os.path.join(label_export_dir, 'export_data.json')
                    with open(export_path, 'w') as f:
                        json.dump(export_data, f, indent=2)
                    
                    return jsonify({
                        'success': True,
                        'message': f'Successfully exported data to {label_export_dir}',
                        'export_dir': label_export_dir
                    })
                
                if allow_download:
                    # Return the export data directly for download
                    response = jsonify(export_data)
                    response.headers['Content-Disposition'] = f'attachment; filename={label_name}_export.json'
                    return response
                    
            except Exception as e:
                logging.error(f"Error exporting data: {str(e)}")
                return jsonify({
                    'success': False,
                    'message': f'Error exporting data: {str(e)}'
                }), 500

        @self.app.route('/visualize/<path:label_id>')
        def visualize(label_id):
            """Show visualization for specific label."""
            try:
                # Set current label
                self.current_label = self._get_label(label_id)
                
                # Generate visualization for this label
                self.generate_visualization()
                
                if not self.video_details:
                    return "Failed to generate visualization data", 500
                
                return render_template('index.html',
                                    categories=self._organize_videos(),
                                    label_info=self._get_label_info(),
                                    label_id=label_id,
                                    show_debug=self.config.get('visualization', {}).get('show_debug_info', False),
                                    lazy_load=self.config.get('visualization', {}).get('lazy_load_videos', True))
            except Exception as e:
                logging.error(f"Error visualizing label: {str(e)}")
                return f"Error loading label: {str(e)}", 400

        @self.app.route('/videos/<path:video_name>')
        def serve_video(video_name):
            """Serve video files."""
            # Find the video in the directory structure
            directory, filename = self.find_video_path(video_name)
            
            if directory and filename:
                # logging.info(f"Serving video from: {directory}, filename: {filename}")
                try:
                    return send_from_directory(
                        directory,
                        filename,
                        mimetype='video/mp4',
                        as_attachment=False
                    )
                except Exception as e:
                    logging.error(f"Error serving video {filename} from {directory}: {str(e)}")
                    return f"Error serving video: {str(e)}", 500
            else:
                logging.warning(f"Video {video_name} not found")
                return f"Video {video_name} not found", 404

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

        @self.app.route('/api/debug_info/<path:label_id>')
        def get_debug_info(label_id):
            """Generate and return debug information for all videos."""
            try:
                # Process videos without using state file
                self.state = None  # Clear state to force processing
                self.current_label = self._get_label(label_id)
                self.generate_visualization()
                
                debug_info = {}
                for name, video in self.all_videos.items():
                    try:
                        debug_data = {
                            'camera_motion': {},
                            'camera_setup': {},
                            'lighting_setup': {}
                        }
                        
                        # Get camera motion data
                        try:
                            motion = video.cam_motion
                            for attr in dir(motion):
                                if not attr.startswith('_') and not callable(getattr(motion, attr)):
                                    debug_data['camera_motion'][attr] = str(getattr(motion, attr))
                        except Exception as e:
                            debug_data['camera_motion']['error'] = str(e)
                        
                        # Get camera setup data
                        try:
                            setup = video.cam_setup
                            for attr in dir(setup):
                                if not attr.startswith('_') and not callable(getattr(setup, attr)):
                                    debug_data['camera_setup'][attr] = str(getattr(setup, attr))
                        except Exception as e:
                            debug_data['camera_setup']['error'] = str(e)
                        
                        # Get lighting setup data
                        try:
                            light = video.light_setup
                            for attr in dir(light):
                                if not attr.startswith('_') and not callable(getattr(light, attr)):
                                    debug_data['lighting_setup'][attr] = str(getattr(light, attr))
                        except Exception as e:
                            debug_data['lighting_setup']['error'] = str(e)
                        
                        debug_info[name] = debug_data
                    except Exception as e:
                        debug_info[name] = {'error': str(e)}
                
                return jsonify(debug_info)
            except Exception as e:
                return jsonify({'error': str(e)}), 500

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
            # Convert URL path format (/) to state file format (.)
            label_name = label_name.replace('/', '.')
            
            # Navigate through the label hierarchy using dots
            current = self.labels
            path_parts = []
            for part in label_name.split('.'):
                current = getattr(current, part)
                path_parts.append(part)
            
            # Store the full path in the label object
            current.label_name = '.'.join(path_parts)  # Override label_name with full path
            return current
        except AttributeError:
            raise ValueError(
                f"Label '{label_name}' not found. Available labels:\n{self.labels}"
            )
    
    def _get_video_details(self, video: VideoData) -> dict:
        """Get relevant details from a video for categorization."""
        details = {
            'camera_motion': {},
            'camera_setup': {},
            'lighting_setup': {}
        }
        
        try:
            motion_data = video.cam_motion
            details['camera_motion'] = {
                'major_simple': motion_data.camera_movement,
                'forward': motion_data.camera_forward_backward,
                'backward': motion_data.camera_forward_backward,
                'steadiness': motion_data.steadiness,
                'pan_right': motion_data.pan_right,
                'camera_pan': motion_data.camera_pan,
                'complex_motion_description': motion_data.complex_motion_description
            }
        except AttributeError as e:
            # logging.warning(f"Camera motion not set: {e}")
            details['camera_motion'] = {
                'major_simple': False,
                'forward': False,
                'backward': False,
                'steadiness': 'unknown',
                'pan_right': None,
                'camera_pan': 'no',
                'complex_motion_description': ''
            }
            
        try:
            setup_data = video.cam_setup
            # Initialize camera angle info and focus info
            setup_data._set_camera_angle_attributes()
            setup_data._set_height_relative_to_ground_attributes()  # Make sure height attributes are initialized
            details['camera_setup'] = {
                'camera_angle_info': setup_data.camera_angle_info,
                'is_camera_angle_applicable': setup_data.is_camera_angle_applicable,
                'camera_angle_start': setup_data.camera_angle_start,
                'camera_angle_end': setup_data.camera_angle_end,
                'is_dutch_angle': setup_data.is_dutch_angle,
                'is_dutch_angle_varying': setup_data.is_dutch_angle_varying,
                'is_dutch_angle_fixed': setup_data.is_dutch_angle_fixed,
                'camera_angle_change_from_high_to_low': setup_data.camera_angle_change_from_high_to_low,
                'camera_angle_change_from_low_to_high': setup_data.camera_angle_change_from_low_to_high,
                'height_wrt_ground_info': setup_data.height_wrt_ground_info,
                'is_height_wrt_ground_applicable': setup_data.is_height_wrt_ground_applicable,
                'height_wrt_ground_start': setup_data.overall_height_start,
                'height_wrt_ground_end': setup_data.overall_height_end
            }
        except AttributeError as e:
            # logging.warning(f"Camera setup not set: {e}")
            details['camera_setup'] = {
                'camera_angle_info': {'start': 'unknown', 'end': 'unknown'},
                'is_camera_angle_applicable': False,
                'camera_angle_start': 'unknown',
                'camera_angle_end': 'unknown',
                'is_dutch_angle': False,
                'is_dutch_angle_varying': False,
                'is_dutch_angle_fixed': False,
                'camera_angle_change_from_high_to_low': False,
                'camera_angle_change_from_low_to_high': False,
                'focus_info': {'start': 'unknown', 'end': 'unknown'},
                'camera_focus': 'unknown',
                'focus_plane_start': 'unknown',
                'focus_plane_end': 'unknown',
                'focus_change_reason': 'no_change',
                'height_wrt_ground_info': 'unknown',
                'is_height_wrt_ground_applicable': False,
                'height_wrt_ground_start': 'unknown',
                'height_wrt_ground_end': 'unknown'
            }
            
        try:
            light_data = video.light_setup
            details['lighting_setup'] = {
                # Add lighting setup details here if needed
            }
        except AttributeError as e:
            # logging.warning(f"Light setup not set: {e}")
            pass
            
        return details

    def create_batch(self, all_videos: Dict[str, VideoData]) -> Batch:
        """Create a batch from all available videos."""
        # logging.info(f"Creating batch with all {len(all_videos)} videos")
        batch = Batch(all_videos)
        # logging.info(f"Created batch with {len(batch)} videos")
        return batch
    
    def categorize_videos(self, batch: Batch) -> Dict[str, Dict[str, Any]]:
        """Categorize videos and collect their details."""
        video_details = {}
        
        # logging.info("\nStarting video categorization:")
        # logging.info(f"Batch size: {len(batch)}")
        
        for name, video in batch:
            # logging.info(f"\nProcessing video: {name}")
            try:
                # Get all video details
                details = self._get_video_details(video)
                # logging.info("Got video details")
                
                # # Debug video attributes
                # logging.info("Video attributes:")
                # try:
                #     logging.info(f"  Camera motion: {video.cam_motion.camera_movement}")
                #     logging.info(f"  Forward/Backward: {video.cam_motion.camera_forward_backward}")
                # except AttributeError:
                #     logging.info("  Camera motion: Not set")
                #     logging.info("  Forward/Backward: Not set")

                # try:
                #     # Print detailed camera angle info
                #     logging.info(f"  Camera angle info:")
                #     logging.info(f"    Start: {video.cam_setup.camera_angle_info['start']}")
                #     logging.info(f"    End: {video.cam_setup.camera_angle_info['end']}")
                #     logging.info(f"    Is applicable: {video.cam_setup.is_camera_angle_applicable}")
                # except AttributeError:
                #     logging.info("  Camera angle: Not set")

                # try:
                #     logging.info(f"  Steadiness: {video.cam_motion.steadiness}")
                # except AttributeError:
                #     logging.info("  Steadiness: Not set")
                
                # Determine category using label rules
                category = 'uncategorized'  # Default category
                # logging.info("Checking label rules:")
                
                # Debug positive rule evaluation
                pos_result = self.current_label.pos_rule(video)
                # logging.info(f"Positive rule result: {pos_result}")
                
                # Debug negative rule evaluation
                neg_result = self.current_label.neg_rule(video)
                # logging.info(f"Negative rule result: {neg_result}")
                
                if pos_result:
                    category = 'positive'
                    # logging.info("Categorized as positive")
                elif neg_result:
                    category = 'negative'
                    # logging.info("Categorized as negative")
                    
                    # Check for easy negative subcategories
                    for rule_name, rule in self.current_label.easy_neg_rules.items():
                        rule_result = rule(video)
                        logging.info(f"Easy negative rule '{rule_name}' result: {rule_result}")
                        if rule_result:
                            category = f'easy_negative_{rule_name}'
                            # logging.info(f"Categorized as easy negative: {rule_name}")
                            break
                            
                    # Check for hard negative subcategories
                    for rule_name, rule in self.current_label.hard_neg_rules.items():
                        rule_result = rule(video)
                        logging.info(f"Hard negative rule '{rule_name}' result: {rule_result}")
                        if rule_result:
                            category = f'hard_negative_{rule_name}'
                            # logging.info(f"Categorized as hard negative: {rule_name}")
                            break
                
                # Add reason for uncategorized videos
                if category == 'uncategorized':
                    reason = []
                    # Add camera motion details
                    try:
                        motion = video.cam_motion
                        reason.append("Camera Motion:")
                        for attr in dir(motion):
                            if not attr.startswith('_') and not callable(getattr(motion, attr)):
                                value = getattr(motion, attr)
                                reason.append(f"  {attr}: {value}")
                    except AttributeError:
                        reason.append("Camera motion data not set")

                    # Add camera setup details
                    try:
                        setup = video.cam_setup
                        reason.append("\nCamera Setup:")
                        for attr in dir(setup):
                            if not attr.startswith('_') and not callable(getattr(setup, attr)):
                                value = getattr(setup, attr)
                                reason.append(f"  {attr}: {value}")
                    except AttributeError:
                        reason.append("Camera setup data not set")

                    # Add lighting setup details
                    try:
                        light = video.light_setup
                        reason.append("\nLighting Setup:")
                        for attr in dir(light):
                            if not attr.startswith('_') and not callable(getattr(light, attr)):
                                value = getattr(light, attr)
                                reason.append(f"  {attr}: {value}")
                    except AttributeError:
                        reason.append("Lighting setup data not set")

                    # logging.info(f"Video uncategorized. Debug info:\n{'\n'.join(reason)}")
                
                video_details[name] = {
                    'details': details,
                    'category': category,
                    'video_path': self.get_video_path(name),
                    'categorization_reason': reason if category == 'uncategorized' else None
                }
                # logging.info(f"Added video to details with category: {category}")
                
            except Exception as e:
                # logging.error(f"Error processing video {name}: {str(e)}")
                # logging.error(f"Error type: {type(e)}")
                # import traceback
                # logging.error(f"Traceback: {traceback.format_exc()}")
                pass
                
        # logging.info(f"\nFinished categorization. Processed {len(video_details)} videos")
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
            # logging.info(f"Found video in path: {full_path}")
            return full_path
            
        # Fallback to direct path
        full_path = os.path.join(videos_dir, video_name)
        # logging.info(f"Using direct video path: {full_path}")
        return full_path
    
    def generate_visualization(self):
        """Generate visualization data for the batch."""
        # Create batch with constraints
        batch = self.create_batch(self.all_videos)
        
        # Get detailed categorization
        if self.state and self.current_label:
            # Get the label name directly from the label object
            label_path = self.current_label.label_name
            
            if label_path in self.state:
                logging.info(f"Using pre-categorized videos from state file for {label_path}")
                state_categories = self.state[label_path]
                
                # Initialize video details with categories from state
                self.video_details = {}
                
                # Handle all categories directly from state
                for category in ['positive', 'negative', 'easy_negative', 'hard_negative', 'uncategorized']:
                    if category in state_categories:
                        for name in state_categories[category]:
                            if name in self.all_videos:
                                self.video_details[name] = {
                                    'details': self._get_video_details(self.all_videos[name]),
                                    'category': category,
                                    'video_path': self.get_video_path(name)
                                }
                
                # Log summary statistics
                category_counts = {}
                for details in self.video_details.values():
                    category = details['category']
                    category_counts[category] = category_counts.get(category, 0) + 1
                    
                logging.info("\nVisualization data loaded from state:")
                logging.info(f"Total videos in batch: {len(batch)}")
                logging.info("Categories:")
                for category, count in category_counts.items():
                    logging.info(f"  {category}: {count} videos")
                return
            else:
                logging.info(f"Label {label_path} not found in state file, falling back to processing")
        
        # Fall back to processing videos if no state or label not found
        self.video_details = self.categorize_videos(batch)
        
        # Log summary statistics
        category_counts = {}
        for details in self.video_details.values():
            category = details['category']
            category_counts[category] = category_counts.get(category, 0) + 1
            
        # logging.info("\nVisualization data generated:")
        # logging.info(f"Total videos in batch: {len(batch)}")
        # logging.info("Categories:")
        # for category, count in category_counts.items():
        #     logging.info(f"  {category}: {count} videos")
            
        # # Verify self.video_details is not None
        # if self.video_details is None:
        #     logging.error("self.video_details is None after generation!")
        # else:
        #     logging.info(f"\nNumber of videos in self.video_details: {len(self.video_details)}")

    def _organize_videos(self):
        """Organize videos by category."""
        preview_mode = self.config.get('visualization', {}).get('preview_mode', False)
        preview_count = self.config.get('visualization', {}).get('preview_count', 5)
        
        categories = {
            'positive': [],
            'negative': [],
            'easy_negative': [],  # Changed to list since we're not using rule-specific lists
            'hard_negative': [],  # Changed to list since we're not using rule-specific lists
            'uncategorized': []
        }
        
        # Also create preview categories if in preview mode
        preview_categories = {
            'positive': [],
            'negative': [],
            'easy_negative': [],
            'hard_negative': [],
            'uncategorized': []
        } if preview_mode else None
        
        for name, details in self.video_details.items():
            category = details['category']
            video_info = {
                'name': name,
                'details': details['details'],
                'categorization_reason': details.get('categorization_reason')
            }
            
            # Map the category to one of our main categories
            target_category = category
            if category.startswith('easy_negative_'):
                target_category = 'easy_negative'
            elif category.startswith('hard_negative_'):
                target_category = 'hard_negative'
            elif category not in categories:
                target_category = 'uncategorized'
            
            categories[target_category].append(video_info)
            # Add to preview if we haven't reached preview_count
            if preview_mode and len(preview_categories[target_category]) < preview_count:
                preview_categories[target_category].append(video_info)
        
        # Remove empty categories
        categories = {k: v for k, v in categories.items() if v}
        if preview_mode:
            preview_categories = {k: v for k, v in preview_categories.items() if v}
            
            # Calculate total remaining videos
            total_remaining = sum(len(categories[k]) - len(v) for k, v in preview_categories.items() if k in categories)
            
            return {
                'preview': preview_categories,
                'full': categories,
                'total_remaining': total_remaining
            }
        
        return categories

    def _get_label_info(self):
        """Get label information."""
        return {
            'name': self.current_label.label_name,  # Use label_name directly
            'description': self.current_label.label,
            'positive_rule': self.current_label.pos_rule.rule,
            'negative_rule': self.current_label.neg_rule.rule,
            'easy_negative_rules': {k: v.rule for k, v in self.current_label.easy_neg_rules.items()},
            'hard_negative_rules': {k: v.rule for k, v in self.current_label.hard_neg_rules.items()}
        }

    def find_video_path(self, video_name: str) -> tuple[str, str]:
        """Find the directory and filename for a video.
        
        Args:
            video_name: Name of the video to find
            
        Returns:
            Tuple of (directory, filename) if found, (None, None) if not found
        """
        # Get videos_dir from config
        videos_dir = self.config['data'].get('videos_dir')
        if not videos_dir:
            logging.warning("Videos directory not specified in config")
            return None, None
            
        # Convert to absolute path if it's relative
        if not os.path.isabs(videos_dir):
            # Get the directory where the config file is located
            config_dir = os.path.dirname(os.path.abspath('visualization/configs/visualizer_config.yaml'))
            # Resolve the relative path from the config directory
            videos_dir = os.path.abspath(os.path.join(config_dir, videos_dir))
        
        # logging.info(f"Searching for {video_name} in videos directory: {videos_dir}")
        
        if not os.path.exists(videos_dir):
            logging.warning(f"Videos directory does not exist: {videos_dir}")
            return None, None
            
        # Walk through all subdirectories
        for root, _, files in os.walk(videos_dir):
            # logging.info(f"Checking directory: {root}")
            if video_name in files:
                full_path = os.path.join(root, video_name)
                # logging.info(f"Found video at: {full_path}")
                return root, video_name
        
        logging.warning(f"Video {video_name} not found in videos directory")
        return None, None 