import logging
from etl.fetch_api import fetch_all_bookings
from etl.transform import transform_data
from etl.load_currency import load_currency_rates
from etl.db import recreate_table
from utils.logger import setup_logger

logger = setup_logger(__name__)

def main():
    try:
        logger.info("Starting ETL pipeline")

        logger.info("Loading currency rates")
        load_currency_rates(r"data/currency_rates.csv")

        logger.info("Fetching booking data from API")
        bookings_df = fetch_all_bookings()
        logger.info(f"Fetched {len(bookings_df)} booking records")

        logger.info("Transforming data")
        summary_df = transform_data(bookings_df)

        logger.info("Loading summary data into database")
        recreate_table("invoicing", summary_df)

        logger.info("✔ Invoicing data successfully loaded to Postgres")
        
        print(summary_df.head(20))

    except Exception as e:
        logger.exception(f"Pipeline failed due to: {e}")
        raise

if __name__ == "__main__":
    main()
