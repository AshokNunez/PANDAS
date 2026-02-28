import duckdb
import logging

logging.basicConfig(
    filename="referential_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

PEOPLE_TABLE = "people"
BUSINESS_TABLE = "business"
COMPANY_TABLE = "company"

PEOPLE_BUSINESS_CODE_COL = "business_code"
BUSINESS_BUSINESS_CODE_COL = "business_code"

PEOPLE_CODE_SERVICE_COL = "code_service"
COMPANY_CODE_SERVICE_COL = "code_service"

COMPANY_UID_COL = "uid"
BUSINESS_UID_COL = "uid"

BUSINESS_PREFIX = "business_"

try:
    con = duckdb.connect("referential_pipeline.duckdb")
    logging.info("Pipeline started")

    # -------------------------------------------------
    # 1️⃣ Strict Deduplicate Business (1 row per key)
    # -------------------------------------------------

    con.execute(f"""
        CREATE OR REPLACE TABLE business_dedup AS
        SELECT *
        FROM (
            SELECT *,
                   ROW_NUMBER() OVER (
                       PARTITION BY {BUSINESS_BUSINESS_CODE_COL}
                       ORDER BY {BUSINESS_UID_COL}
                   ) AS rn
            FROM {BUSINESS_TABLE}
        )
        WHERE rn = 1;
    """)

    # -------------------------------------------------
    # 2️⃣ Strict Deduplicate Company
    # -------------------------------------------------

    con.execute(f"""
        CREATE OR REPLACE TABLE company_dedup AS
        SELECT *
        FROM (
            SELECT *,
                   ROW_NUMBER() OVER (
                       PARTITION BY {COMPANY_CODE_SERVICE_COL}
                       ORDER BY {COMPANY_UID_COL}
                   ) AS rn
            FROM {COMPANY_TABLE}
        )
        WHERE rn = 1;
    """)

    logging.info("Deduplication complete")

    # -------------------------------------------------
    # 3️⃣ Dynamic Business Columns
    # -------------------------------------------------

    business_columns = con.execute(f"""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = '{BUSINESS_TABLE}'
    """).fetchall()

    business_select_clause = ",\n".join([
        f"b.{col[0]} AS {BUSINESS_PREFIX}{col[0]}"
        for col in business_columns
    ])

    # -------------------------------------------------
    # 4️⃣ Deterministic Single Join (No Row Multiplication)
    # -------------------------------------------------

    con.execute(f"""
        CREATE OR REPLACE TABLE final_output AS
        SELECT
            p.*,
            {business_select_clause},
            CASE
                WHEN b.{BUSINESS_BUSINESS_CODE_COL} IS NOT NULL THEN 'DIRECT'
                WHEN bf.{BUSINESS_BUSINESS_CODE_COL} IS NOT NULL THEN 'FALLBACK'
                ELSE 'NO_MATCH'
            END AS match_type
        FROM {PEOPLE_TABLE} p

        -- Direct match
        LEFT JOIN business_dedup b
            ON p.{PEOPLE_BUSINESS_CODE_COL} = b.{BUSINESS_BUSINESS_CODE_COL}

        -- Fallback via company -> business
        LEFT JOIN company_dedup c
            ON p.{PEOPLE_CODE_SERVICE_COL} = c.{COMPANY_CODE_SERVICE_COL}

        LEFT JOIN business_dedup bf
            ON c.{COMPANY_UID_COL} = bf.{BUSINESS_UID_COL};
    """)

    logging.info("Final table created without row multiplication")

    # -------------------------------------------------
    # 5️⃣ Optional: Remove Ambiguous Cases
    # -------------------------------------------------
    # If both direct and fallback exist → keep direct only
    con.execute("""
        DELETE FROM final_output
        WHERE match_type = 'FALLBACK'
        AND business_business_code IS NOT NULL;
    """)

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
