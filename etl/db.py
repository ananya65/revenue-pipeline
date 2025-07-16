import pandas as pd
from sqlalchemy import create_engine, text
from config.config import DB_URL
from utils.logger import setup_logger

logger = setup_logger(__name__)
engine = create_engine(DB_URL)

def recreate_table(table_name: str, df: pd.DataFrame):
    try:
        with engine.begin() as conn:
            logger.info(f"Dropping table if it exists: '{table_name}'")
            conn.execute(text(f"DROP TABLE IF EXISTS {table_name};"))

            logger.info(f"Creating empty table structure for '{table_name}'")
            df.head(0).to_sql(table_name, con=conn, index=False)

            logger.info(f"Inserting {len(df)} records into '{table_name}'")
            df.to_sql(table_name, con=conn, index=False, if_exists="append")

            logger.info(f"Table '{table_name}' recreated successfully.")

    except Exception as e:
        logger.exception(f"Failed to recreate table '{table_name}': {e}")
