from visualization import BatchVisualizer
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def main():
    # Create visualizer with config file
    config_path = 'visualization/configs/visualizer_config.yaml'
    visualizer = BatchVisualizer(config_path)
    
    # Run the server
    logging.info(f"Starting server...")
    visualizer.run_server()

if __name__ == "__main__":
    main() 