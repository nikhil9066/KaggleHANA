"""
Advanced ETL Pipeline for Kaggle to SAP HANA
Includes incremental loading, batch processing, monitoring, and data quality checks
"""

import logging
import time
import json
from datetime import datetime
from typing import Dict, Any, Optional
import pandas as pd


class ETLMetrics:
    """Track ETL process metrics and statistics"""

    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.rows_fetched = 0
        self.rows_validated = 0
        self.rows_inserted = 0
        self.rows_updated = 0
        self.rows_failed = 0
        self.errors = []
        self.warnings = []

    def start(self):
        """Start timing the ETL process"""
        self.start_time = datetime.now()

    def stop(self):
        """Stop timing the ETL process"""
        self.end_time = datetime.now()

    def duration_seconds(self):
        """Calculate duration in seconds"""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0

    def add_error(self, error_msg: str):
        """Add an error message"""
        self.errors.append({
            'timestamp': datetime.now().isoformat(),
            'message': error_msg
        })

    def add_warning(self, warning_msg: str):
        """Add a warning message"""
        self.warnings.append({
            'timestamp': datetime.now().isoformat(),
            'message': warning_msg
        })

    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary"""
        return {
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration_seconds': self.duration_seconds(),
            'rows_fetched': self.rows_fetched,
            'rows_validated': self.rows_validated,
            'rows_inserted': self.rows_inserted,
            'rows_updated': self.rows_updated,
            'rows_failed': self.rows_failed,
            'success_rate': round((self.rows_inserted + self.rows_updated) / max(self.rows_fetched, 1) * 100, 2),
            'errors_count': len(self.errors),
            'warnings_count': len(self.warnings),
            'errors': self.errors,
            'warnings': self.warnings
        }

    def log_summary(self, logger: logging.Logger):
        """Log a summary of the metrics"""
        logger.info("=" * 80)
        logger.info("ETL PIPELINE METRICS")
        logger.info("=" * 80)
        logger.info(f"Duration: {self.duration_seconds():.2f} seconds")
        logger.info(f"Rows Fetched: {self.rows_fetched}")
        logger.info(f"Rows Validated: {self.rows_validated}")
        logger.info(f"Rows Inserted: {self.rows_inserted}")
        logger.info(f"Rows Updated: {self.rows_updated}")
        logger.info(f"Rows Failed: {self.rows_failed}")
        logger.info(f"Success Rate: {(self.rows_inserted + self.rows_updated) / max(self.rows_fetched, 1) * 100:.2f}%")
        logger.info(f"Errors: {len(self.errors)}")
        logger.info(f"Warnings: {len(self.warnings)}")
        logger.info("=" * 80)


class DataQualityValidator:
    """Validate data quality before insertion"""

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def validate_dataframe(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Validate DataFrame data quality

        Returns:
            dict: Validation results with issues found
        """
        issues = {
            'duplicates': [],
            'missing_values': {},
            'invalid_dates': [],
            'invalid_numbers': [],
            'outliers': []
        }

        # Check for duplicates
        if 'Ticker' in df.columns and 'Date' in df.columns:
            duplicates = df[df.duplicated(subset=['Ticker', 'Date'], keep=False)]
            if len(duplicates) > 0:
                issues['duplicates'] = duplicates[['Ticker', 'Date']].to_dict('records')
                self.logger.warning(f"Found {len(duplicates)} duplicate records")

        # Check for missing values
        for col in df.columns:
            missing_count = df[col].isna().sum()
            if missing_count > 0:
                issues['missing_values'][col] = int(missing_count)
                self.logger.warning(f"Column '{col}' has {missing_count} missing values")

        # Validate dates
        if 'Date' in df.columns:
            invalid_dates = df[df['Date'].isna()]
            if len(invalid_dates) > 0:
                issues['invalid_dates'] = len(invalid_dates)
                self.logger.warning(f"Found {len(invalid_dates)} invalid dates")

        # Validate numeric columns
        numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume', 'Daily_Range', 'Daily_Return']
        for col in numeric_cols:
            if col in df.columns:
                # Check for negative values where they shouldn't be
                if col in ['Open', 'High', 'Low', 'Close', 'Volume']:
                    invalid = df[df[col] < 0]
                    if len(invalid) > 0:
                        issues['invalid_numbers'].append({
                            'column': col,
                            'count': len(invalid),
                            'reason': 'negative_values'
                        })
                        self.logger.warning(f"Column '{col}' has {len(invalid)} negative values")

        # Check for price outliers (High < Low shouldn't happen)
        if 'High' in df.columns and 'Low' in df.columns:
            outliers = df[df['High'] < df['Low']]
            if len(outliers) > 0:
                issues['outliers'] = len(outliers)
                self.logger.warning(f"Found {len(outliers)} records where High < Low")

        return issues

    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean DataFrame by removing invalid records

        Args:
            df: Input DataFrame

        Returns:
            Cleaned DataFrame
        """
        original_count = len(df)

        # Remove duplicates
        if 'Ticker' in df.columns and 'Date' in df.columns:
            df = df.drop_duplicates(subset=['Ticker', 'Date'], keep='last')
            removed = original_count - len(df)
            if removed > 0:
                self.logger.info(f"Removed {removed} duplicate records")

        # Remove records with invalid dates
        if 'Date' in df.columns:
            df = df[df['Date'].notna()]

        # Remove records with invalid prices (negative values)
        price_cols = ['Open', 'High', 'Low', 'Close']
        for col in price_cols:
            if col in df.columns:
                df = df[df[col] > 0]

        # Remove records where High < Low
        if 'High' in df.columns and 'Low' in df.columns:
            df = df[df['High'] >= df['Low']]

        final_count = len(df)
        total_removed = original_count - final_count

        if total_removed > 0:
            self.logger.info(f"Cleaned data: removed {total_removed} invalid records ({original_count} -> {final_count})")

        return df


class ETLPipeline:
    """Advanced ETL Pipeline with incremental loading and batch processing"""

    def __init__(self, kaggle_client, hana_client, config: Dict[str, Any]):
        """
        Initialize ETL Pipeline

        Args:
            kaggle_client: KaggleApiClient instance
            hana_client: HanaClient instance
            config: Configuration dictionary
        """
        self.kaggle_client = kaggle_client
        self.hana_client = hana_client
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.metrics = ETLMetrics()
        self.validator = DataQualityValidator(self.logger)

        # Get batch size from config or use default
        self.batch_size = config.get('etl', {}).get('batch_size', 1000)

    def get_last_loaded_date(self, schema_name: str, table_name: str) -> Optional[datetime]:
        """
        Get the last loaded date from HANA table for incremental loading

        Args:
            schema_name: Schema name
            table_name: Table name

        Returns:
            Last loaded date or None
        """
        try:
            cursor = self.hana_client.connection.cursor()

            query = f"""
            SELECT MAX("DATE")
            FROM "{schema_name}"."{table_name}"
            """

            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()

            if result and result[0]:
                last_date = result[0]
                self.logger.info(f"Last loaded date in HANA: {last_date}")
                return last_date
            else:
                self.logger.info("No existing data in HANA table - full load will be performed")
                return None

        except Exception as e:
            self.logger.warning(f"Could not determine last loaded date: {str(e)}")
            return None

    def filter_incremental_data(self, df: pd.DataFrame, last_date: Optional[datetime]) -> pd.DataFrame:
        """
        Filter DataFrame to only include new records since last_date

        Args:
            df: Full DataFrame
            last_date: Last loaded date

        Returns:
            Filtered DataFrame with only new records
        """
        if last_date is None:
            self.logger.info("Performing full data load")
            return df

        if 'Date' not in df.columns:
            self.logger.warning("Date column not found - cannot perform incremental load")
            return df

        # Convert last_date to pandas Timestamp for comparison
        last_date_ts = pd.Timestamp(last_date)

        # Filter for dates after last_date
        new_data = df[df['Date'] > last_date_ts]

        self.logger.info(f"Incremental load: filtered {len(df)} -> {len(new_data)} new records (after {last_date})")

        return new_data

    def insert_data_batch(self, df_batch: pd.DataFrame, schema_name: str, table_name: str) -> tuple:
        """
        Insert a batch of data into HANA

        Args:
            df_batch: Batch DataFrame
            schema_name: Schema name
            table_name: Table name

        Returns:
            Tuple of (inserted_count, updated_count, failed_count)
        """
        if not self.hana_client.connection:
            self.logger.error("No HANA connection available")
            return (0, 0, len(df_batch))

        try:
            cursor = self.hana_client.connection.cursor()
            inserted = 0
            updated = 0
            failed = 0
            timestamp = datetime.now()

            for index, row in df_batch.iterrows():
                try:
                    # Extract data
                    ticker = str(row.get('Ticker', ''))
                    date = row.get('Date')
                    open_price = float(row.get('Open', 0)) if pd.notna(row.get('Open')) else None
                    high_price = float(row.get('High', 0)) if pd.notna(row.get('High')) else None
                    low_price = float(row.get('Low', 0)) if pd.notna(row.get('Low')) else None
                    close_price = float(row.get('Close', 0)) if pd.notna(row.get('Close')) else None
                    volume = int(row.get('Volume', 0)) if pd.notna(row.get('Volume')) else None
                    daily_range = float(row.get('Daily_Range', 0)) if pd.notna(row.get('Daily_Range')) else None
                    daily_return = float(row.get('Daily_Return', 0)) if pd.notna(row.get('Daily_Return')) else None

                    # Convert pandas Timestamp to Python date
                    if hasattr(date, 'date'):
                        date = date.date()

                    # Use UPSERT (MERGE) for better performance
                    merge_sql = f"""
                    MERGE INTO "{schema_name}"."{table_name}" AS target
                    USING (SELECT ? AS TICKER, ? AS DATE FROM DUMMY) AS source
                    ON target."TICKER" = source.TICKER AND target."DATE" = source.DATE
                    WHEN MATCHED THEN
                        UPDATE SET
                            "OPEN" = ?, "HIGH" = ?, "LOW" = ?, "CLOSE" = ?,
                            "VOLUME" = ?, "DAILY_RANGE" = ?, "DAILY_RETURN" = ?,
                            "TIMESTAMP" = ?
                    WHEN NOT MATCHED THEN
                        INSERT ("TICKER", "DATE", "OPEN", "HIGH", "LOW", "CLOSE",
                                "VOLUME", "DAILY_RANGE", "DAILY_RETURN", "TIMESTAMP")
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """

                    cursor.execute(merge_sql, (
                        ticker, date,  # USING clause
                        open_price, high_price, low_price, close_price,  # UPDATE clause
                        volume, daily_range, daily_return, timestamp,
                        ticker, date, open_price, high_price, low_price, close_price,  # INSERT clause
                        volume, daily_range, daily_return, timestamp
                    ))

                    # Check if insert or update occurred
                    if cursor.rowcount > 0:
                        inserted += 1

                except Exception as row_error:
                    failed += 1
                    error_msg = f"Row {index} [{ticker}|{date}]: {str(row_error)}"
                    self.logger.error(error_msg)
                    self.metrics.add_error(error_msg)

            self.hana_client.connection.commit()
            cursor.close()

            return (inserted, updated, failed)

        except Exception as e:
            self.logger.error(f"Batch insert error: {str(e)}")
            self.metrics.add_error(f"Batch insert failed: {str(e)}")
            return (0, 0, len(df_batch))

    def process_data_in_batches(self, df: pd.DataFrame, schema_name: str, table_name: str) -> Dict[str, int]:
        """
        Process DataFrame in batches for better performance

        Args:
            df: DataFrame to process
            schema_name: Schema name
            table_name: Table name

        Returns:
            Dictionary with processing results
        """
        total_rows = len(df)
        total_inserted = 0
        total_updated = 0
        total_failed = 0

        self.logger.info(f"Processing {total_rows} rows in batches of {self.batch_size}")

        # Process in batches
        for i in range(0, total_rows, self.batch_size):
            batch_num = (i // self.batch_size) + 1
            batch_df = df.iloc[i:i + self.batch_size]

            self.logger.info(f"Processing batch {batch_num} ({len(batch_df)} rows)...")

            inserted, updated, failed = self.insert_data_batch(batch_df, schema_name, table_name)

            total_inserted += inserted
            total_updated += updated
            total_failed += failed

            self.logger.info(f"Batch {batch_num} complete: {inserted} inserted, {updated} updated, {failed} failed")

            # Small delay between batches to avoid overwhelming the database
            if i + self.batch_size < total_rows:
                time.sleep(0.1)

        return {
            'inserted': total_inserted,
            'updated': total_updated,
            'failed': total_failed
        }

    def run(self, schema_name: str, table_name: str, incremental: bool = True) -> Dict[str, Any]:
        """
        Run the complete ETL pipeline

        Args:
            schema_name: HANA schema name
            table_name: HANA table name
            incremental: Whether to perform incremental load (default: True)

        Returns:
            Dictionary with pipeline execution results
        """
        self.logger.info("=" * 80)
        self.logger.info("STARTING ADVANCED ETL PIPELINE")
        self.logger.info("=" * 80)

        self.metrics.start()

        try:
            # Step 1: Fetch data from Kaggle
            self.logger.info("\n[STEP 1] Fetching data from Kaggle...")
            df = self.kaggle_client.fetch_stock_data()

            if df is None or df.empty:
                raise Exception("Failed to fetch data from Kaggle or data is empty")

            self.metrics.rows_fetched = len(df)
            self.logger.info(f"Fetched {len(df)} rows from Kaggle")

            # Step 2: Data Quality Validation
            self.logger.info("\n[STEP 2] Validating data quality...")
            issues = self.validator.validate_dataframe(df)

            if issues['duplicates'] or issues['invalid_dates'] or issues['outliers']:
                self.logger.warning("Data quality issues detected - cleaning data...")
                df = self.validator.clean_dataframe(df)

            self.metrics.rows_validated = len(df)

            # Step 3: Incremental Loading (if enabled)
            if incremental:
                self.logger.info("\n[STEP 3] Checking for incremental load...")
                last_date = self.get_last_loaded_date(schema_name, table_name)
                df = self.filter_incremental_data(df, last_date)

                if df.empty:
                    self.logger.info("No new data to load")
                    self.metrics.stop()
                    return self.metrics.to_dict()
            else:
                self.logger.info("\n[STEP 3] Performing full load (incremental disabled)")

            # Step 4: Batch Processing
            self.logger.info(f"\n[STEP 4] Processing {len(df)} rows in batches...")
            results = self.process_data_in_batches(df, schema_name, table_name)

            self.metrics.rows_inserted = results['inserted']
            self.metrics.rows_updated = results['updated']
            self.metrics.rows_failed = results['failed']

            # Step 5: Final Statistics
            self.logger.info("\n[STEP 5] Retrieving final statistics...")
            stats = self.hana_client.get_table_stats(schema_name, table_name)

            self.metrics.stop()
            self.metrics.log_summary(self.logger)

            self.logger.info("\n" + "=" * 80)
            self.logger.info("HANA TABLE STATISTICS")
            self.logger.info("=" * 80)
            self.logger.info(f"Total rows in table: {stats.get('total_rows', 'N/A')}")
            self.logger.info(f"Unique tickers: {stats.get('unique_tickers', 'N/A')}")
            self.logger.info(f"Date range: {stats.get('min_date', 'N/A')} to {stats.get('max_date', 'N/A')}")
            self.logger.info("=" * 80)

            return self.metrics.to_dict()

        except Exception as e:
            self.metrics.stop()
            self.metrics.add_error(f"Pipeline failed: {str(e)}")
            self.logger.error(f"ETL Pipeline failed: {str(e)}", exc_info=True)
            raise
