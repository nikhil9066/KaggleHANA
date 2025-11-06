"""
SAP HANA database client for storing S&P 500 stock data
"""

import datetime
import logging

# Import SAP HANA Python client
try:
    from hdbcli import dbapi
    HDBCLI_AVAILABLE = True
except ImportError:
    HDBCLI_AVAILABLE = False
    logging.warning("hdbcli package not installed. SAP HANA integration will not work.")
    logging.warning("Install using: pip install hdbcli")

class HanaClient:
    """Client for interacting with SAP HANA database."""

    def __init__(self, config):
        """
        Initialize the SAP HANA client with configuration.

        Args:
            config (dict): Configuration parameters
        """
        self.logger = logging.getLogger(__name__)

        if not HDBCLI_AVAILABLE:
            self.logger.error("hdbcli package not installed. Cannot use SAP HANA integration.")
            raise ImportError("hdbcli package not installed")

        # Set HANA connection parameters
        self.address = config['hana']['address']
        self.port = config['hana']['port']
        self.user = config['hana']['user']
        self.password = config['hana']['password']
        self.schema = config['hana']['schema']

        # Connection will be set later
        self.connection = None

        # Define table schema for S&P 500 stock data
        self.table_schema = """
            CREATE TABLE "{schema}"."{table}" (
                "ID" INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                "TICKER" NVARCHAR(20),
                "DATE" DATE,
                "OPEN" DECIMAL(18,6),
                "HIGH" DECIMAL(18,6),
                "LOW" DECIMAL(18,6),
                "CLOSE" DECIMAL(18,6),
                "VOLUME" BIGINT,
                "DAILY_RANGE" DECIMAL(18,6),
                "DAILY_RETURN" DECIMAL(18,6),
                "TIMESTAMP" TIMESTAMP,
                UNIQUE ("TICKER", "DATE")
            )
        """

    def connect(self):
        """
        Establish a connection to SAP HANA database.

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.connection = dbapi.connect(
                address=self.address,
                port=int(self.port),
                user=self.user,
                password=self.password
            )

            self.logger.info("Successfully connected to SAP HANA at %s:%s",
                         self.address, self.port)
            return True

        except Exception as e:
            self.logger.error("Failed to connect to SAP HANA: %s", str(e))
            return False

    def close(self):
        """Close the connection to SAP HANA database."""
        if self.connection:
            self.connection.close()
            self.logger.info("Closed connection to SAP HANA")
            self.connection = None

    def create_schema_if_not_exists(self, schema_name):
        """
        Create a schema in SAP HANA if it doesn't exist.

        Args:
            schema_name (str): The schema name to create

        Returns:
            bool: True if successful, False otherwise
        """
        if not self.connection:
            self.logger.error("No connection to SAP HANA. Cannot create schema.")
            return False

        try:
            cursor = self.connection.cursor()

            # Check if schema exists
            cursor.execute(f"""
            SELECT COUNT(*) FROM SYS.SCHEMAS WHERE SCHEMA_NAME = '{schema_name}'
            """)

            schema_exists = cursor.fetchone()[0] > 0

            if not schema_exists:
                cursor.execute(f"""
                CREATE SCHEMA "{schema_name}"
                """)
                self.logger.info(f'Successfully created schema "{schema_name}" in SAP HANA')
            else:
                self.logger.info(f'Schema "{schema_name}" already exists in SAP HANA')

            cursor.close()
            return True

        except Exception as e:
            self.logger.error(f"Error creating schema: {str(e)}")
            return False

    def create_table(self, schema_name, table_name):
        """
        Create a table in SAP HANA for storing S&P 500 stock data.

        Args:
            schema_name (str): The schema name in SAP HANA
            table_name (str): The table name to create

        Returns:
            bool: True if successful, False otherwise
        """
        if not self.connection:
            self.logger.error("No connection to SAP HANA. Cannot create table.")
            return False

        try:
            cursor = self.connection.cursor()

            # First check if table exists
            cursor.execute(f"""
            SELECT COUNT(*) FROM SYS.TABLES
            WHERE SCHEMA_NAME = '{schema_name}' AND TABLE_NAME = '{table_name}'
            """)

            table_exists = cursor.fetchone()[0] > 0

            if not table_exists:
                create_table_sql = self.table_schema.format(
                    schema=schema_name, table=table_name)

                cursor.execute(create_table_sql)
                self.logger.info(f'Successfully created table "{schema_name}"."{table_name}" in SAP HANA')
            else:
                self.logger.info(f'Table "{schema_name}"."{table_name}" already exists in SAP HANA')

            cursor.close()
            return True

        except Exception as e:
            self.logger.error(f"Error creating HANA table: {str(e)}")
            return False

    def insert_data(self, df, schema_name, table_name):
        """
        Insert stock data from DataFrame to SAP HANA table.

        Args:
            df (DataFrame): The pandas DataFrame containing stock data
            schema_name (str): The schema name in SAP HANA
            table_name (str): The table name to insert into

        Returns:
            int: The number of rows inserted
        """
        if not self.connection:
            self.logger.error("No connection to SAP HANA. Cannot insert data.")
            return 0

        try:
            cursor = self.connection.cursor()
            rows_inserted = 0
            rows_updated = 0
            timestamp = datetime.datetime.now()

            # Process the DataFrame
            for index, row in df.iterrows():
                try:
                    # Extract stock data
                    ticker = str(row.get('Ticker', ''))
                    date = row.get('Date')
                    open_price = float(row.get('Open', 0)) if row.get('Open') is not None else None
                    high_price = float(row.get('High', 0)) if row.get('High') is not None else None
                    low_price = float(row.get('Low', 0)) if row.get('Low') is not None else None
                    close_price = float(row.get('Close', 0)) if row.get('Close') is not None else None
                    volume = int(row.get('Volume', 0)) if row.get('Volume') is not None else None
                    daily_range = float(row.get('Daily_Range', 0)) if row.get('Daily_Range') is not None else None
                    daily_return = float(row.get('Daily_Return', 0)) if row.get('Daily_Return') is not None else None

                    # Convert pandas Timestamp to Python date
                    if hasattr(date, 'date'):
                        date = date.date()

                    # Check if record already exists
                    check_sql = f"""
                    SELECT COUNT(*) FROM "{schema_name}"."{table_name}"
                    WHERE "TICKER" = ? AND "DATE" = ?
                    """
                    cursor.execute(check_sql, (ticker, date))
                    exists = cursor.fetchone()[0] > 0

                    if exists:
                        # Update existing record
                        update_sql = f"""
                        UPDATE "{schema_name}"."{table_name}"
                        SET "OPEN" = ?, "HIGH" = ?, "LOW" = ?, "CLOSE" = ?,
                            "VOLUME" = ?, "DAILY_RANGE" = ?, "DAILY_RETURN" = ?,
                            "TIMESTAMP" = ?
                        WHERE "TICKER" = ? AND "DATE" = ?
                        """
                        cursor.execute(update_sql, (
                            open_price, high_price, low_price, close_price,
                            volume, daily_range, daily_return, timestamp,
                            ticker, date
                        ))
                        rows_updated += 1
                    else:
                        # Insert new record
                        insert_sql = f"""
                        INSERT INTO "{schema_name}"."{table_name}" (
                            "TICKER", "DATE", "OPEN", "HIGH", "LOW", "CLOSE",
                            "VOLUME", "DAILY_RANGE", "DAILY_RETURN", "TIMESTAMP"
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """
                        cursor.execute(insert_sql, (
                            ticker, date, open_price, high_price, low_price, close_price,
                            volume, daily_range, daily_return, timestamp
                        ))
                        rows_inserted += 1

                except Exception as row_error:
                    self.logger.warning(f"Error processing row {index}: {str(row_error)}")
                    continue

            self.connection.commit()
            cursor.close()

            self.logger.info(f'Successfully inserted {rows_inserted} rows and updated {rows_updated} rows in "{schema_name}"."{table_name}"')
            return rows_inserted + rows_updated

        except Exception as e:
            self.logger.error(f"Error inserting data to HANA: {str(e)}")
            return 0

    def get_table_stats(self, schema_name, table_name):
        """
        Get statistics about the data in the table.

        Args:
            schema_name (str): The schema name in SAP HANA
            table_name (str): The table name

        Returns:
            dict: Statistics about the table
        """
        if not self.connection:
            self.logger.error("No connection to SAP HANA.")
            return {}

        try:
            cursor = self.connection.cursor()

            # Get total row count
            cursor.execute(f"""
            SELECT COUNT(*) FROM "{schema_name}"."{table_name}"
            """)
            total_rows = cursor.fetchone()[0]

            # Get unique tickers count
            cursor.execute(f"""
            SELECT COUNT(DISTINCT "TICKER") FROM "{schema_name}"."{table_name}"
            """)
            unique_tickers = cursor.fetchone()[0]

            # Get date range
            cursor.execute(f"""
            SELECT MIN("DATE"), MAX("DATE") FROM "{schema_name}"."{table_name}"
            """)
            date_range = cursor.fetchone()

            cursor.close()

            stats = {
                'total_rows': total_rows,
                'unique_tickers': unique_tickers,
                'min_date': str(date_range[0]) if date_range[0] else None,
                'max_date': str(date_range[1]) if date_range[1] else None
            }

            self.logger.info(f"Table stats: {stats}")
            return stats

        except Exception as e:
            self.logger.error(f"Error getting table stats: {str(e)}")
            return {}

    def query_data(self, schema_name, table_name, limit=100):
        """
        Query data from the table.

        Args:
            schema_name (str): The schema name in SAP HANA
            table_name (str): The table name
            limit (int): Maximum number of rows to return

        Returns:
            list: List of dictionaries containing the data
        """
        if not self.connection:
            self.logger.error("No connection to SAP HANA.")
            return []

        try:
            cursor = self.connection.cursor()

            query = f"""
            SELECT "TICKER", "DATE", "OPEN", "HIGH", "LOW", "CLOSE",
                   "VOLUME", "DAILY_RANGE", "DAILY_RETURN"
            FROM "{schema_name}"."{table_name}"
            ORDER BY "DATE" DESC, "TICKER"
            LIMIT {limit}
            """

            cursor.execute(query)

            columns = [desc[0] for desc in cursor.description]
            results = []

            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))

            cursor.close()

            return results

        except Exception as e:
            self.logger.error(f"Error querying data: {str(e)}")
            return []
