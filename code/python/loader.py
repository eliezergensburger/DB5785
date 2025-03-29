import psycopg2
import pandas as pd
from io import StringIO
import time
import logging
from typing import Tuple, Optional
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PostgresLoader:
    def __init__(self):
        # Docker-friendly configuration (can be overridden with environment variables)
        self.DB_HOST = os.getenv("DB_HOST", "localhost")
        self.DB_PORT = os.getenv("DB_PORT", "5432")
        self.DB_NAME = os.getenv("DB_NAME", "postgres")
        self.DB_USER = os.getenv("DB_USER", "postgres")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
        self.TABLE_NAME = os.getenv("TABLE_NAME", "employees")
        self.DATASET_URL = os.getenv("DATASET_URL", "https://people.sc.fsu.edu/~jburkardt/data/csv/hw_200.csv")

    def _get_connection(self) -> psycopg2.extensions.connection:
        """Establish database connection with retry logic"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                conn = psycopg2.connect(
                    dbname=self.DB_NAME,
                    user=self.DB_USER,
                    password=self.DB_PASSWORD,
                    host=self.DB_HOST,
                    port=self.DB_PORT,
                    connect_timeout=5
                )
                conn.autocommit = False  # We'll manage transactions explicitly
                return conn
            except psycopg2.OperationalError as e:
                if attempt == max_retries - 1:
                    raise
                wait_time = (attempt + 1) * 2
                logger.warning(f"Connection failed (attempt {attempt + 1}), retrying in {wait_time}s...")
                time.sleep(wait_time)

    def download_dataset(self) -> pd.DataFrame:
        """Download and preprocess dataset"""
        try:
            df = pd.read_csv(
                self.DATASET_URL,
                header=None,
                names=["Index", "Height", "Weight"],
                dtype={"Height": float, "Weight": float}
            )
            df.drop(columns=["Index"], inplace=True)
            logger.info(f"Downloaded dataset with {len(df)} rows")
            return df
        except Exception as e:
            logger.error(f"Failed to download dataset: {e}")
            raise

    def _create_table(self, cursor: psycopg2.extensions.cursor) -> None:
        """Create table with optimized schema"""
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
            id SERIAL PRIMARY KEY,
            height FLOAT NOT NULL,
            weight FLOAT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS idx_{self.TABLE_NAME}_height ON {self.TABLE_NAME}(height);
        CREATE INDEX IF NOT EXISTS idx_{self.TABLE_NAME}_weight ON {self.TABLE_NAME}(weight);
        """
        cursor.execute(create_table_query)

    def _bulk_insert(self, cursor: psycopg2.extensions.cursor, df: pd.DataFrame) -> Tuple[bool, Optional[str]]:
        """Perform bulk insert with COPY FROM"""
        try:
            # Prepare data in memory
            output = StringIO()
            df.to_csv(output, index=False, header=False, sep='\t')
            output.seek(0)
            
            # Use COPY with explicit columns
            cursor.copy_from(
                file=output,
                table=self.TABLE_NAME,
                sep='\t',
                null='',  # Handle NULL values
                columns=('height', 'weight')
            )
            return True, None
        except Exception as e:
            return False, str(e)

    def load_data(self) -> bool:
        """Main data loading workflow"""
        start_time = time.time()
        conn = None
        try:
            # Step 1: Download data
            df = self.download_dataset()
            
            # Step 2: Connect to database
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Step 3: Prepare database
            self._create_table(cursor)
            
            # Step 4: Load data with transaction
            success, error = self._bulk_insert(cursor, df)
            if not success:
                conn.rollback()
                logger.error(f"Bulk insert failed: {error}")
                return False
            
            conn.commit()
            elapsed = time.time() - start_time
            logger.info(f"Successfully loaded {len(df)} rows in {elapsed:.2f} seconds")
            return True
            
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Data loading failed: {e}")
            return False
        finally:
            if conn:
                cursor.close()
                conn.close()

# Docker-compatible execution
if __name__ == "__main__":
    loader = PostgresLoader()
    
    # For Docker health checks
    if os.getenv("HEALTH_CHECK", "false").lower() == "true":
        try:
            conn = loader._get_connection()
            conn.close()
            print("Database connection healthy")
            exit(0)
        except Exception as e:
            print(f"Database connection failed: {e}")
            exit(1)
    
    # Normal execution
    success = loader.load_data()
    exit(0 if success else 1)
