import duckdb
import logging

logging.basicConfig(
    filename="referential_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------------------------------------
# 🔑 Dynamic Column Configuration
# -------------------------------------------------

PEOPLE_TABLE = "people"
BUSINESS_TABLE = "business"
COMPANY_TABLE = "company"

PEOPLE_BUSINESS_CODE_COL = "business_code"
BUSINESS_BUSINESS_CODE_COL = "business_code"

PEOPLE_CODE_SERVICE_COL = "code_service"
COMPANY_CODE_SERVICE_COL = "code_service"
COMPANY_UID_COL = "uid"
BUSINESS_UID_COL = "uid"

BUSINESS_PREFIX = "business_"   # naming convention

try:
    con = duckdb.connect("referential_pipeline.duckdb")
    logging.info("Pipeline started")

    # -------------------------------------------------
    # 1️⃣ Normalize Keys (Trim + Lower)
    # -------------------------------------------------

    con.execute(f"""
        CREATE OR REPLACE TABLE people_clean AS
        SELECT *,
               NULLIF(LOWER(TRIM({PEOPLE_BUSINESS_CODE_COL})), '') AS clean_business_code,
               NULLIF(LOWER(TRIM({PEOPLE_CODE_SERVICE_COL})), '') AS clean_code_service
        FROM {PEOPLE_TABLE};
    """)

    con.execute(f"""
        CREATE OR REPLACE TABLE business_clean AS
        SELECT *,
               NULLIF(LOWER(TRIM({BUSINESS_BUSINESS_CODE_COL})), '') AS clean_business_code,
               NULLIF(LOWER(TRIM({BUSINESS_UID_COL})), '') AS clean_uid
        FROM {BUSINESS_TABLE};
    """)

    con.execute(f"""
        CREATE OR REPLACE TABLE company_clean AS
        SELECT *,
               NULLIF(LOWER(TRIM({COMPANY_CODE_SERVICE_COL})), '') AS clean_code_service,
               NULLIF(LOWER(TRIM({COMPANY_UID_COL})), '') AS clean_uid
        FROM {COMPANY_TABLE};
    """)

    logging.info("Key normalization completed")

    # -------------------------------------------------
    # 2️⃣ Get Business Columns Dynamically
    # -------------------------------------------------

    business_columns = con.execute(f"""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = '{BUSINESS_TABLE}'
        AND column_name NOT IN ('clean_business_code','clean_uid')
    """).fetchall()

    business_select_clause = ",\n".join([
        f"b.{col[0]} AS {BUSINESS_PREFIX}{col[0]}"
        for col in business_columns
    ])

    # -------------------------------------------------
    # 3️⃣ Direct Match
    # -------------------------------------------------

    con.execute(f"""
        CREATE OR REPLACE TABLE direct_match AS
        SELECT
            p.*,
            {business_select_clause},
            'DIRECT_BUSINESS_CODE' AS match_type
        FROM people_clean p
        LEFT JOIN business_clean b
            ON p.clean_business_code = b.clean_business_code;
    """)

    logging.info("Direct matching completed")

    # -------------------------------------------------
    # 4️⃣ Fallback Only for Non-Matched
    # -------------------------------------------------

    con.execute("""
        CREATE OR REPLACE TABLE no_direct AS
        SELECT p.*
        FROM people_clean p
        LEFT JOIN business_clean b
            ON p.clean_business_code = b.clean_business_code
        WHERE b.clean_business_code IS NULL;
    """)

    con.execute(f"""
        CREATE OR REPLACE TABLE fallback_match AS
        SELECT
            p.*,
            {business_select_clause},
            'FALLBACK_CODE_SERVICE' AS match_type
        FROM no_direct p
        LEFT JOIN company_clean c
            ON p.clean_code_service = c.clean_code_service
        LEFT JOIN business_clean b
            ON c.clean_uid = b.clean_uid;
    """)

    logging.info("Fallback matching completed")

    # -------------------------------------------------
    # 5️⃣ Combine
    # -------------------------------------------------

    con.execute("""
        CREATE OR REPLACE TABLE final_output AS
        SELECT * FROM direct_match
        UNION ALL
        SELECT * FROM fallback_match;
    """)

    logging.info("Final table created")

    # -------------------------------------------------
    # 6️⃣ Export
    # -------------------------------------------------

    con.execute("""
        COPY final_output TO 'final_output.parquet' (FORMAT PARQUET);
    """)

    logging.info("Export completed successfully")

except Exception as e:
    logging.error(str(e))
    raise
How its reading parquet files
