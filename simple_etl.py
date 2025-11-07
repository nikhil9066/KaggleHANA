#!/usr/bin/env python
# coding: utf-8
"""
Simple Kaggle to HANA ETL Script
Fetches S&P 500 data from Kaggle and pushes to SAP HANA.
No web interface - pure backend processing.
"""

import os
import sys
import logging
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.config import setup_logging, load_config
from api.kaggle_api import KaggleApiClient
from db.hana_client import HanaClient

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

def main():
    """
    Main ETL function - fetch from Kaggle and push to HANA.
    """
    try:
        logger.info("="*80)
        logger.info("Starting Kaggle to HANA ETL Process")
        logger.info("="*80)
        
        # Load configuration
        logger.info("Loading configuration...")
        config = load_config()
        
        # Step 1: Fetch data from Kaggle
        logger.info("\n[STEP 1] Fetching data from Kaggle...")
        kaggle_client = KaggleApiClient(config)
        df = kaggle_client.fetch_stock_data()
        
        if df is None or df.empty:
            logger.error("Failed to fetch data from Kaggle or data is empty")
            return 1
        
        logger.info(f"✅ Successfully fetched {len(df)} rows from Kaggle")
        logger.info(f"   Date range: {df['Date'].min()} to {df['Date'].max()}")
        logger.info(f"   Unique tickers: {df['Ticker'].nunique()}")

        # Limit to first 50 rows only
        df = df.head(50)
        logger.info(f"⚠️  Limited dataset to 50 rows for testing")

        # Step 2: Connect to HANA
        logger.info("\n[STEP 2] Connecting to SAP HANA...")
        hana_client = HanaClient(config)
        
        if not hana_client.connect():
            logger.error("Failed to connect to SAP HANA")
            return 1
        
        logger.info("✅ Connected to SAP HANA")
        
        # Step 3: Create schema
        logger.info("\n[STEP 3] Creating schema (if not exists)...")
        schema_name = config['hana']['schema']
        
        if not hana_client.create_schema_if_not_exists(schema_name):
            logger.error(f"Failed to create schema: {schema_name}")
            hana_client.close()
            return 1
        
        logger.info(f"✅ Schema '{schema_name}' ready")
        
        # Step 4: Create table
        logger.info("\n[STEP 4] Creating table (if not exists)...")
        table_name = config['hana']['table']
        
        if not hana_client.create_table(schema_name, table_name):
            logger.error(f"Failed to create table: {schema_name}.{table_name}")
            hana_client.close()
            return 1
        
        logger.info(f"✅ Table '{schema_name}.{table_name}' ready")
        
        # Step 5: Insert data
        logger.info("\n[STEP 5] Inserting data into HANA...")
        rows_affected = hana_client.insert_data(df, schema_name, table_name)
        
        if rows_affected == 0:
            logger.error("Failed to insert data into SAP HANA")
            hana_client.close()
            return 1
        
        logger.info(f"✅ Successfully processed {rows_affected} rows")
        
        # Step 6: Get statistics
        logger.info("\n[STEP 6] Retrieving database statistics...")
        stats = hana_client.get_table_stats(schema_name, table_name)
        
        logger.info("\n" + "="*80)
        logger.info("DATABASE STATISTICS")
        logger.info("="*80)
        logger.info(f"Total rows in table: {stats.get('total_rows', 'N/A')}")
        logger.info(f"Unique tickers: {stats.get('unique_tickers', 'N/A')}")
        logger.info(f"Date range: {stats.get('min_date', 'N/A')} to {stats.get('max_date', 'N/A')}")
        logger.info("="*80)
        
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
