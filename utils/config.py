"""
Configuration utilities for Kaggle to HANA integration
"""

import os
import logging
import logging.handlers
from dotenv import load_dotenv
from pathlib import Path

def setup_logging(log_dir="logs"):
    """
    Set up logging configuration.

    Args:
        log_dir (str): Directory to store log files
    """
    # Create logs directory if it doesn't exist
    Path(log_dir).mkdir(parents=True, exist_ok=True)

    # Configure the root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create formatters
    file_formatter = logging.Formatter('%(asctime)s [%(levelname)-8s] [%(name)s:%(lineno)s]: %(message)s')
    console_formatter = logging.Formatter('[%(levelname)-8s] %(message)s')

    # Create and configure file handler (with rotation)
    log_file = os.path.join(log_dir, "kaggle_to_hana.log")
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=10*1024*1024, backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)

    # Create and configure console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def load_config():
    """
    Load configuration from .env file and environment variables.

    Returns:
        dict: Configuration parameters
    """
    # Load environment variables from .env file
    load_dotenv()

    config = {
        # Kaggle API settings
        'kaggle': {
            'username': os.getenv('KAGGLE_USERNAME'),
            'key': os.getenv('KAGGLE_KEY'),
            'dataset_name': os.getenv('KAGGLE_DATASET', 'camnugent/sandp500')
        },

        # SAP HANA settings
        'hana': {
            'address': os.getenv('HANA_ADDRESS'),
            'port': os.getenv('HANA_PORT', '443'),
            'user': os.getenv('HANA_USER'),
            'password': os.getenv('HANA_PASSWORD'),
            'schema': os.getenv('HANA_SCHEMA', 'SP500_DATA'),
            'table': os.getenv('HANA_TABLE', 'STOCK_PRICES')
        },

        # File paths
        'paths': {
            'data_dir': os.getenv('DATA_DIR', 'data'),
            'downloads_dir': os.getenv('DOWNLOADS_DIR', 'downloads')
        },

        # ETL Pipeline settings
        'etl': {
            'batch_size': int(os.getenv('ETL_BATCH_SIZE', '1000')),
            'incremental': os.getenv('ETL_INCREMENTAL', 'true').lower() == 'true',
            'enable_validation': os.getenv('ETL_ENABLE_VALIDATION', 'true').lower() == 'true'
        }
    }

    # Validate required configuration
    missing_kaggle = []
    if not config['kaggle']['username']:
        missing_kaggle.append('KAGGLE_USERNAME')
    if not config['kaggle']['key']:
        missing_kaggle.append('KAGGLE_KEY')

    if missing_kaggle:
        raise ValueError(f"Missing required Kaggle API configuration: {', '.join(missing_kaggle)}")

    # Create directories if they don't exist
    for dir_path in [config['paths']['data_dir'], config['paths']['downloads_dir']]:
        Path(dir_path).mkdir(parents=True, exist_ok=True)

    return config
