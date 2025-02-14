from visualization import BatchVisualizer
import logging
import argparse

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run the batch visualizer')
    parser.add_argument('--batch-folder', type=str, help='Path to the batch folder to visualize')
    args = parser.parse_args()

    # Create visualizer with config file
    config_path = 'visualization/configs/visualizer_config.yaml'
    
    # If batch folder is provided, update the config with it
    if args.batch_folder:
        logging.info(f"Using batch folder: {args.batch_folder}")
    
    visualizer = BatchVisualizer(config_path, batch_folder=args.batch_folder)
    
    # Run the server
    logging.info(f"Starting server...")
    visualizer.run_server()

if __name__ == "__main__":
    main() 