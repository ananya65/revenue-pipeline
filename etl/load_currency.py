import pandas as pd
from sqlalchemy import text
from etl.db import engine
from utils.logger import setup_logger

logger = setup_logger(__name__)

def load_currency_rates(csv_path: str, table_name="currency_rates"):
    try:
        logger.info(f"Loading currency rates from {csv_path}")
        df = pd.read_csv(csv_path)
        df["rate_date"] = pd.to_datetime(df["rate_date"])
        logger.info(f"Read {len(df)} rows from currency CSV")

        with engine.connect() as conn:
            logger.info(f"Dropping existing table `{table_name}` if it exists")
            conn.execute(text(f"DROP TABLE IF EXISTS {table_name}"))

        logger.info(f"Writing to table `{table_name}` in database")
        df.to_sql(table_name, engine, index=False, if_exists="replace")

        logger.info(f"✔ Currency rates loaded successfully to `{table_name}`")

    except Exception as e:
        logger.exception(f" Failed to load currency rates: {e}")
        raise
