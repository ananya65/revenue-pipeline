import pandas as pd
from sqlalchemy import create_engine
from config.config import CURRENCY_MAPPING, FEE_PER_BOOKING, MIN_FEE, DB_URL
from utils.logger import setup_logger

# Set up logger for this module
logger = setup_logger(__name__)
engine = create_engine(DB_URL)

def transform_data(df: pd.DataFrame):
    logger.info(f"Starting transformation with {len(df)} rows.")

    try:
        df["check_out_date"] = pd.to_datetime(df["check_out_date"]).dt.normalize()
        df["currency"] = df["owner_company_country"].map(CURRENCY_MAPPING)
        df["fee_per_booking"] = df["owner_company_country"].map(FEE_PER_BOOKING)

        # Load exchange rates
        currency_df = pd.read_sql("SELECT * FROM currency_rates WHERE to_currency = 'GBP'", engine)
        logger.info(f"Loaded {len(currency_df)} currency rate rows from database.")

        currency_df = currency_df.rename(columns={"from_currency": "currency"})
        df = df.merge(
            currency_df,
            left_on=["currency", "check_out_date"],
            right_on=["currency", "rate_date"],
            how="left"
        )

        missing_rates = df["rate"].isna().sum()
        if missing_rates > 0:
            logger.warning(f"{missing_rates} rows are missing exchange rates.")

        df["revenue_gbp"] = df["fee_per_booking"] * df["rate"]
        df["month"] = df["check_out_date"].dt.to_period("M").astype(str)

        summary = df.groupby(
            ["owner_company", "owner_company_country", "currency", "month"]
        ).agg(
            bookings=("booking_id", "count"),
            revenue_local=("fee_per_booking", "sum"),
            revenue_gbp=("revenue_gbp", "sum")
        ).reset_index()

        logger.info(f"Grouped summary created with {len(summary)} rows.")

        def apply_min(row):
            try:
                min_local = MIN_FEE[row["owner_company_country"]]
                row["original_revenue_local"] = row["revenue_local"]
                if row["revenue_local"] < min_local:
                    rate = row["revenue_gbp"] / row["revenue_local"] if row["revenue_local"] > 0 else 0
                    row["revenue_local"] = min_local
                    row["revenue_gbp"] = min_local * rate
                    row["used_min_fee"] = True
                else:
                    row["used_min_fee"] = False
                return row
            except Exception as e:
                logger.exception(f"Failed applying minimum fee to row: {row}")
                raise

        summary = summary.apply(apply_min, axis=1)
        logger.info("Minimum fee enforcement completed.")

        return summary

    except Exception as e:
        logger.exception("Data transformation failed.")
        raise
