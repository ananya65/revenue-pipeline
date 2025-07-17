# Revenue ETL Pipeline

This project implements an ETL pipeline to fetch booking data from an API, transform it using currency rates and fees, and load the summarized invoicing data into a PostgreSQL database.

---

## Prerequisites

- Docker & Docker Compose installed
- Poetry installed ([installation guide](https://python-poetry.org/docs/#installation))
- Python 3.12+

---
## Setup and Usage

### 1. Clone the repository

```bash
git clone https://github.com/ananya65/revenue-pipeline.git
```
### 2. Start PostgreSQL with Docker Compose

Run the following command to start the PostgreSQL database container in detached mode:

```bash
docker compose up -d
```

### 3. Install dependencies and activate virtual environment

Install dependencies and activate virtual environment

```bash
poetry shell
poetry install
```


### 3. Configure environment variables

Create a .env file in the project root with the following variables:
```bash
API_URL=http://localhost:5000/api/bookings
PER_PAGE=20

DB_USER=truvi_user
DB_PASS=truvi_pass
DB_HOST=localhost
DB_PORT=5432
DB_NAME=truvi_db

CURRENCY_MAPPING={"UK":"GBP","USA":"USD","France":"EUR"}
FEE_PER_BOOKING={"UK":10,"USA":14,"France":12}
MIN_FEE={"UK":100,"USA":140,"France":120}
```

