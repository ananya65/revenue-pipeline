import requests
import pandas as pd
from config.config import API_URL, PER_PAGE
from utils.logger import setup_logger

logger = setup_logger(__name__)

def fetch_all_bookings():
    page = 1
    all_results = []

    logger.info("Starting to fetch bookings from API.")
    
    while True:
        try:
            logger.debug(f"Fetching page {page} from API...")
            response = requests.get(API_URL, params={"page": page, "per_page": PER_PAGE})
            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])
            
            if not results:
                logger.info("No more results to fetch. Ending pagination.")
                break
            
            logger.info(f"Fetched {len(results)} records from page {page}.")
            all_results.extend(results)
            page += 1

        except requests.HTTPError as e:
            logger.exception(f"HTTP error on page {page}: {e}")
            raise
        except Exception as e:
            logger.exception(f"Unexpected error on page {page}: {e}")
            raise

    df = pd.DataFrame(all_results)
    logger.info(f"Finished fetching data. Total records fetched: {len(df)}")
    return df
