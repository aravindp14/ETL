import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from sqlalchemy import create_engine, text
import logging
import sys


# ============================================================
# 1. LOGGING CONFIGURATION (Production Standard)
# ============================================================

logging.basicConfig(
    filename="etl_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log(msg):
    logging.info(msg)
    print(msg)   # also print to console for notebook visibility


# ============================================================
# 2. DATABASE ENGINE (SQLAlchemy Production Standard)
# ============================================================

def get_engine():
    return create_engine(
        "mysql+pymysql://root:Benz007@localhost/commodity_price",
        pool_pre_ping=True,          # avoids stale connections
        pool_recycle=1800,           # avoids MySQL timeout
        echo=False                   # disable noisy SQL logs
    )


# ============================================================
# 3. EXTRACTION (Robust, Clean, Safe)
# ============================================================

def extract(url, location):
    """
    Extract steel price data from ScrapMonster.
    Returns a clean DataFrame.
    """

    log(f"Extracting data from {location}...")

    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("tbody")
    if table is None:
        raise ValueError(f"No table found for URL: {url}")

    rows = table.find_all("tr")
    records = []

    currency_map = {"$US": "USD", "$": "USD", "US$": "USD"}
    unit_map = {"MT": "metric_ton", "Kg": "kilogram", "LB": "pound"}

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 5:
            continue

        metal_type = cols[0].get_text(strip=True)
        price = float(cols[1].get_text(strip=True))

        raw = cols[3].get_text(strip=True)
        curr_raw, unit_raw = raw.split("/")

        currency = currency_map.get(curr_raw)
        unit = unit_map.get(unit_raw)

        reported_date = datetime.strptime(cols[4].get_text(strip=True), "%B %d, %Y")

        records.append({
            "metal_type": metal_type,
            "price": price,
            "unit": unit,
            "currency": currency,
            "location": location,
            "scraped_date": datetime.now(),
            "reported_date": reported_date
        })

    df = pd.DataFrame(records)
    log(f"Extracted {len(df)} rows from {location}")
    return df


# ============================================================
# 4. TRANSFORMATION (Simple but future‑proof)
# ============================================================

def transform(df):
    """
    Placeholder for future transformations.
    Currently returns df unchanged.
    """
    log("Transforming data...")
    return df


# ============================================================
# 5. LOAD TO CSV (Production Safe)
# ============================================================

def load_to_csv(df, location, csv_path):
    filename = f"{location}_{csv_path}"
    df.to_csv(filename, index=False)
    log(f"Saved CSV: {filename}")


# ============================================================
# 6. LOAD TO DATABASE (UPSERT + SQLAlchemy Safe)
# ============================================================

def load_to_db(df, engine):
    """
    UPSERT into MySQL using SQLAlchemy text() with named parameters.
    """

    log("Loading data into database...")

    insert_stmt = text("""
        INSERT INTO steel_price (
            metal_type, price, unit, currency, location, scraped_date, reported_date
        ) VALUES (
            :metal_type, :price, :unit, :currency, :location, :scraped_date, :reported_date
        )
        ON DUPLICATE KEY UPDATE
            price = VALUES(price),
            unit = VALUES(unit),
            currency = VALUES(currency),
            scraped_date = VALUES(scraped_date);
    """)

    with engine.begin() as conn:
        conn.execute(insert_stmt, df.to_dict(orient="records"))

    log("Database load complete.")


# ============================================================
# 7. MAIN ETL LOOP (Production‑Grade)
# ============================================================

def run_etl():

    engine = get_engine()

    urls = [
        "https://www.scrapmonster.com/steel-prices/united-states",
        "https://www.scrapmonster.com/steel-prices/china",
        "https://www.scrapmonster.com/steel-prices/europe",
        "https://www.scrapmonster.com/steel-prices/world-export-market"
    ]

    locations = ["USA", "China", "Europe", "World"]
    csv_path = "steel_price.csv"

    for url, location in zip(urls, locations):

        log(f"Starting ETL for {location}")

        df = extract(url, location)
        df = transform(df)
        load_to_csv(df, location, csv_path)
        load_to_db(df, engine)

        log(f"ETL completed for {location}\n")


# ============================================================
# 8. RUN ETL
# ============================================================

if __name__ == "__main__":
    try:
        run_etl()
        log("ETL Pipeline Completed Successfully.")
    except Exception as e:
        logging.error(f"ETL Failed: {str(e)}")
        print(f"ETL Failed: {str(e)}")
        sys.exit(1)
