# Revenue ETL Pipeline

This project implements an ETL pipeline to fetch booking data from an API, transform it using currency rates and fees, and load the summarized invoicing data into a PostgreSQL database.

---

## Prerequisites

- Docker & Docker Compose installed
- Poetry installed ([installation guide](https://python-poetry.org/docs/#installation))
- Python 3.12+

---
## Setup

### 1. Clone the repository

```bash
git clone https://github.com/ananya65/revenue-pipeline.git

## 2. Start PostgreSQL with Docker Compose

Run the following command to start the PostgreSQL database container in detached mode:

```bash
docker compose up -d
