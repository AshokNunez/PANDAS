import duckdb
import logging
from pathlib import Path

# -------------------------------------------------
# 🔧 Config
# -------------------------------------------------

DB_FILE = "referential_pipeline.duckdb"
SOURCE_FOLDER = "data"   # folder containing all parquet files

logging.basicConfig(
    filename="referential_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

try:
    con = duckdb.connect(DB_FILE)
    logging.info("Pipeline started")

    folder = Path(SOURCE_FOLDER)

    # -------------------------------------------------
    # 1️⃣ Collect Files by Prefix
    # -------------------------------------------------

    people_files = []
    business_files = []
    company_files = []

    for file in folder.glob("*.parquet"):
        name = file.name.lower()

        if name.startswith("people"):
            people_files.append(str(file))

        elif name.startswith("isis"):
            business_files.append(str(file))

        elif name.startswith("sak"):
            company_files.append(str(file))

    logging.info(f"People files: {len(people_files)}")
    logging.info(f"Business files: {len(business_files)}")
    logging.info(f"Company files: {len(company_files)}")

    # -------------------------------------------------
    # 2️⃣ Create Tables in DuckDB
    # -------------------------------------------------

    if people_files:
        con.execute(f"""
            CREATE OR REPLACE TABLE people AS
            SELECT * FROM read_parquet({people_files});
        """)

    if business_files:
        con.execute(f"""
            CREATE OR REPLACE TABLE business AS
            SELECT * FROM read_parquet({business_files});
        """)

    if company_files:
        con.execute(f"""
            CREATE OR REPLACE TABLE company AS
            SELECT * FROM read_parquet({company_files});
        """)

    logging.info("Tables created successfully in DB")

except Exception as e:
    logging.error(str(e))
    raise
