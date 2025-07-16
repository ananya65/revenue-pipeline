import os
import json
from dotenv import load_dotenv


load_dotenv()

API_URL = os.getenv("API_URL")
PER_PAGE = int(os.getenv("PER_PAGE", 20))


DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
POSTGRES = {
    "user": DB_USER,
    "password": DB_PASS,
    "host": DB_HOST,
    "port": DB_PORT,
    "dbname": DB_NAME
}


CURRENCY_MAPPING = json.loads(os.getenv("CURRENCY_MAPPING"))
FEE_PER_BOOKING = json.loads(os.getenv("FEE_PER_BOOKING"))
MIN_FEE = json.loads(os.getenv("MIN_FEE"))
