"""
Kaggle API client for S&P 500 data
"""

import logging
import os
import pandas as pd
import zipfile
from pathlib import Path

class KaggleApiClient:
    """Client for interacting with Kaggle API to fetch S&P 500 stock data."""

    def __init__(self, config):
        """
        Initialize the Kaggle API Client with configuration.

        Args:
            config (dict): Configuration parameters
        """
        self.logger = logging.getLogger(__name__)

        # Set Kaggle API configuration
        self.kaggle_username = config['kaggle']['username']
        self.kaggle_key = config['kaggle']['key']
        self.dataset_name = config['kaggle']['dataset_name']

        # Set file paths
        self.download_dir = config['paths']['downloads_dir']
        self.data_dir = config['paths']['data_dir']

        # Ensure directories exist
        Path(self.download_dir).mkdir(parents=True, exist_ok=True)
        Path(self.data_dir).mkdir(parents=True, exist_ok=True)

        # Initialize Kaggle API
        self._initialize_kaggle_api()

    def _initialize_kaggle_api(self):
        """Initialize the Kaggle API with credentials."""
        try:
            # Set Kaggle credentials as environment variables
            os.environ['KAGGLE_USERNAME'] = self.kaggle_username
            os.environ['KAGGLE_KEY'] = self.kaggle_key

            # Import kaggle API
            from kaggle.api.kaggle_api_extended import KaggleApi

            self.api = KaggleApi()
            self.api.authenticate()

            self.logger.info("Successfully authenticated with Kaggle API")

        except Exception as e:
            self.logger.error(f"Failed to initialize Kaggle API: {str(e)}")
            raise

    def download_dataset(self):
        """
        Download the S&P 500 dataset from Kaggle.

        Returns:
            str: Path to the downloaded dataset
        """
        try:
            self.logger.info(f"Downloading dataset: {self.dataset_name}")

            # Download the dataset
            self.api.dataset_download_files(
                self.dataset_name,
                path=self.download_dir,
                unzip=True
            )

            self.logger.info(f"Successfully downloaded dataset to {self.download_dir}")

            # Find the downloaded CSV file
            csv_files = list(Path(self.download_dir).glob("*.csv"))

            if not csv_files:
                self.logger.error("No CSV files found in download directory")
                return None

            # Return the first CSV file found
            dataset_path = str(csv_files[0])
            self.logger.info(f"Found dataset file: {dataset_path}")

            return dataset_path

        except Exception as e:
            self.logger.error(f"Error downloading dataset: {str(e)}")
            raise

    def load_and_clean_data(self, dataset_path=None):
        """
        Load and clean the S&P 500 data.

        Args:
            dataset_path (str, optional): Path to the dataset file

        Returns:
            DataFrame: Cleaned pandas DataFrame with stock data
        """
        try:
            # If no path provided, download the dataset
            if dataset_path is None:
                dataset_path = self.download_dataset()

            if dataset_path is None:
                self.logger.error("No dataset path available")
                return None

            self.logger.info(f"Loading data from: {dataset_path}")

            # Load the CSV file
            df = pd.read_csv(dataset_path)

            self.logger.info(f"Loaded {len(df)} rows with columns: {df.columns.tolist()}")

            # Clean the data
            df = self._clean_dataframe(df)

            self.logger.info(f"After cleaning: {len(df)} rows")

            return df

        except Exception as e:
            self.logger.error(f"Error loading and cleaning data: {str(e)}")
            raise

    def _clean_dataframe(self, df):
        """
        Clean and transform the DataFrame.

        Args:
            df (DataFrame): Raw DataFrame

        Returns:
            DataFrame: Cleaned DataFrame
        """
        try:
            # Standardize column names (handle different dataset formats)
            # Common column name variations
            column_mapping = {
                'date': 'Date',
                'Date': 'Date',
                'open': 'Open',
                'Open': 'Open',
                'high': 'High',
                'High': 'High',
                'low': 'Low',
                'Low': 'Low',
                'close': 'Close',
                'Close': 'Close',
                'volume': 'Volume',
                'Volume': 'Volume',
                'name': 'Ticker',
                'Name': 'Ticker',
                'symbol': 'Ticker',
                'Symbol': 'Ticker',
                'ticker': 'Ticker',
                'Ticker': 'Ticker'
            }

            # Rename columns based on mapping
            for old_col, new_col in column_mapping.items():
                if old_col in df.columns:
                    df.rename(columns={old_col: new_col}, inplace=True)

            # Ensure required columns exist
            required_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']

            for col in required_columns:
                if col not in df.columns:
                    self.logger.warning(f"Required column '{col}' not found in dataset")

            # Add Ticker column if it doesn't exist
            if 'Ticker' not in df.columns:
                # Try to extract ticker from filename or use a default
                self.logger.warning("Ticker column not found, using 'UNKNOWN'")
                df['Ticker'] = 'UNKNOWN'

            # Convert Date column to datetime
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

            # Convert numeric columns to proper types
            numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            # Remove rows with missing critical data
            df = df.dropna(subset=['Date', 'Close'])

            # Sort by date and ticker
            sort_columns = []
            if 'Ticker' in df.columns:
                sort_columns.append('Ticker')
            if 'Date' in df.columns:
                sort_columns.append('Date')

            if sort_columns:
                df = df.sort_values(by=sort_columns)

            # Calculate additional metrics
            if all(col in df.columns for col in ['High', 'Low', 'Close']):
                df['Daily_Range'] = df['High'] - df['Low']
                df['Daily_Return'] = df.groupby('Ticker')['Close'].pct_change()

            # Reset index
            df = df.reset_index(drop=True)

            self.logger.info("Data cleaning completed successfully")

            return df

        except Exception as e:
            self.logger.error(f"Error cleaning DataFrame: {str(e)}")
            raise

    def fetch_stock_data(self):
        """
        Main method to fetch and process S&P 500 stock data.

        Returns:
            DataFrame: Processed stock data ready for HANA insertion
        """
        try:
            # Download and load data
            df = self.load_and_clean_data()

            if df is None or df.empty:
                self.logger.error("Failed to fetch data or data is empty")
                return None

            self.logger.info(f"Successfully fetched {len(df)} rows of stock data")

            # Display sample of data
            self.logger.info(f"Data preview:\n{df.head()}")
            self.logger.info(f"Data columns: {df.columns.tolist()}")
            self.logger.info(f"Data types:\n{df.dtypes}")

            return df

        except Exception as e:
            self.logger.error(f"Error fetching stock data: {str(e)}")
            raise

    def get_latest_data_by_ticker(self, df, top_n=100):
        """
        Get the most recent data for each ticker.

        Args:
            df (DataFrame): Full stock data DataFrame
            top_n (int): Number of most recent records per ticker

        Returns:
            DataFrame: Latest data for each ticker
        """
        try:
            if 'Ticker' not in df.columns or 'Date' not in df.columns:
                self.logger.warning("Cannot filter by ticker - required columns missing")
                return df

            # Get the most recent date for each ticker
            latest_data = df.sort_values('Date').groupby('Ticker').tail(top_n)

            self.logger.info(f"Filtered to {len(latest_data)} most recent records")

            return latest_data

        except Exception as e:
            self.logger.error(f"Error filtering latest data: {str(e)}")
            return df

    def get_date_range_data(self, df, start_date=None, end_date=None):
        """
        Filter data by date range.

        Args:
            df (DataFrame): Full stock data DataFrame
            start_date (str): Start date in 'YYYY-MM-DD' format
            end_date (str): End date in 'YYYY-MM-DD' format

        Returns:
            DataFrame: Filtered data within date range
        """
        try:
            if 'Date' not in df.columns:
                self.logger.warning("Date column not found")
                return df

            filtered_df = df.copy()

            if start_date:
                start_date = pd.to_datetime(start_date)
                filtered_df = filtered_df[filtered_df['Date'] >= start_date]
                self.logger.info(f"Filtered data from {start_date}")

            if end_date:
                end_date = pd.to_datetime(end_date)
                filtered_df = filtered_df[filtered_df['Date'] <= end_date]
                self.logger.info(f"Filtered data until {end_date}")

            self.logger.info(f"Date range filter resulted in {len(filtered_df)} rows")

            return filtered_df

        except Exception as e:
            self.logger.error(f"Error filtering by date range: {str(e)}")
            return df
