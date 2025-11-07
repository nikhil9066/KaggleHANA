#!/usr/bin/env python
# coding: utf-8
"""
Advanced Kaggle to HANA ETL Script
Fetches S&P 500 data from Kaggle and pushes to SAP HANA.
Features: Incremental loading, batch processing, data quality validation, monitoring
"""

import os
import sys
import logging
import json
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.config import setup_logging, load_config
from api.kaggle_api import KaggleApiClient
from db.hana_client import HanaClient
from etl.pipeline import ETLPipeline

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

def main():
    """
    Main ETL function - fetch from Kaggle and push to HANA using advanced pipeline.
    """
    try:
        logger.info("="*80)
        logger.info("Starting Advanced Kaggle to HANA ETL Process")
        logger.info("="*80)

        # Load configuration
        logger.info("Loading configuration...")
        config = load_config()

        # Initialize clients
        logger.info("Initializing Kaggle and HANA clients...")
        kaggle_client = KaggleApiClient(config)
        hana_client = HanaClient(config)

        # Connect to HANA
        logger.info("Connecting to SAP HANA...")
        if not hana_client.connect():
            logger.error("Failed to connect to SAP HANA")
            return 1

        logger.info("✅ Connected to SAP HANA")

        # Get schema and table names
        schema_name = config['hana']['schema']
        table_name = config['hana']['table']

        # Create schema if not exists
        logger.info(f"Ensuring schema '{schema_name}' exists...")
        if not hana_client.create_schema_if_not_exists(schema_name):
            logger.error(f"Failed to create schema: {schema_name}")
            hana_client.close()
            return 1

        # Create table if not exists
        logger.info(f"Ensuring table '{schema_name}.{table_name}' exists...")
        if not hana_client.create_table(schema_name, table_name):
            logger.error(f"Failed to create table: {schema_name}.{table_name}")
            hana_client.close()
            return 1

        # Initialize ETL Pipeline
        logger.info("Initializing advanced ETL pipeline...")
        pipeline = ETLPipeline(kaggle_client, hana_client, config)

        # Run the pipeline with incremental loading enabled
        logger.info("Running ETL pipeline...")
        metrics = pipeline.run(schema_name, table_name, incremental=True)

        # Save metrics to file for monitoring
        metrics_file = 'etl_metrics.json'
        with open(metrics_file, 'w') as f:
            json.dump(metrics, f, indent=2)

        logger.info(f"\n✅ Metrics saved to {metrics_file}")

        # Close connection
        hana_client.close()

        logger.info("\n✅ ETL Process completed successfully!")
        return 0

    except Exception as e:
        logger.error(f"\n❌ ETL Process failed: {str(e)}", exc_info=True)
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
