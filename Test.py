import duckdb
import logging

logging.basicConfig(
    filename="referential_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# =========================================================
# TABLE NAMES
# =========================================================
PEOPLE_TABLE = "people"
BUSINESS_TABLE = "business"
COMPANY_TABLE = "company"

# =========================================================
# COLUMN CONFIGURATION
# =========================================================
PEOPLE_EIR_COL = "eir_code"
PEOPLE_POLE_COL = "pole"
PEOPLE_SOUS_POLE_COL = "sous_pole"
PEOPLE_DEPT_COL = "department"
PEOPLE_CODE_SERVICE_COL = "code_service"

BUSINESS_EIR_COL = "business_code"
BUSINESS_POLE_COL = "pole"
BUSINESS_SOUS_POLE_COL = "sous_pole"
BUSINESS_UID_COL = "uid"

COMPANY_CODE_SERVICE_COL = "code_service"
COMPANY_UID_COL = "uid"

BUSINESS_PREFIX = "business_"

try:
    con = duckdb.connect("referential_pipeline.duckdb")
    logging.info("Pipeline started")

    # =========================================================
    # 1️⃣ Deduplicate Business
    # =========================================================
    con.execute(f"""
        CREATE OR REPLACE TABLE business_dedup AS
        SELECT *
        FROM (
            SELECT *,
                   ROW_NUMBER() OVER (
                       PARTITION BY {BUSINESS_EIR_COL}
                       ORDER BY {BUSINESS_UID_COL}
                   ) rn
            FROM {BUSINESS_TABLE}
        )
        WHERE rn = 1;
    """)

    # =========================================================
    # 2️⃣ Deduplicate Company
    # =========================================================
    con.execute(f"""
        CREATE OR REPLACE TABLE company_dedup AS
        SELECT *
        FROM (
            SELECT *,
                   ROW_NUMBER() OVER (
                       PARTITION BY {COMPANY_CODE_SERVICE_COL}
                       ORDER BY {COMPANY_UID_COL}
                   ) rn
            FROM {COMPANY_TABLE}
        )
        WHERE rn = 1;
    """)

    logging.info("Deduplication complete")

    # =========================================================
    # 3️⃣ Dynamic Business Columns
    # =========================================================
    business_columns = con.execute(f"""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'business_dedup'
    """).fetchall()

    business_select_clause = ",\n".join([
        f"b.{col[0]} AS {BUSINESS_PREFIX}{col[0]}"
        for col in business_columns
    ])

    # =========================================================
    # 4️⃣ PRIORITY MATCHING + RANKING + CONFIDENCE
    # =========================================================
    con.execute(f"""
        CREATE OR REPLACE TABLE final_output AS
        SELECT
            p.*,
            {business_select_clause},

            -- Match Type
            CASE
                WHEN LOWER(p.{PEOPLE_DEPT_COL}) LIKE '%gts%'
                     AND p.{PEOPLE_POLE_COL} = b.{BUSINESS_POLE_COL}
                     AND p.{PEOPLE_EIR_COL} = b.{BUSINESS_EIR_COL}
                THEN 'STEP1_GTS_MATCH'

                WHEN LOWER(p.{PEOPLE_DEPT_COL}) NOT LIKE '%gts%'
                     AND p.{PEOPLE_POLE_COL} = b.{BUSINESS_POLE_COL}
                     AND p.{PEOPLE_SOUS_POLE_COL} = b.{BUSINESS_SOUS_POLE_COL}
                     AND p.{PEOPLE_EIR_COL} = b.{BUSINESS_EIR_COL}
                THEN 'STEP2_SOUS_POLE_MATCH'

                WHEN p.{PEOPLE_EIR_COL} = b.{BUSINESS_EIR_COL}
                THEN 'STEP3_DIRECT_MATCH'

                WHEN bf.{BUSINESS_EIR_COL} IS NOT NULL
                THEN 'STEP4_COMPANY_FALLBACK'

                ELSE 'NO_MATCH'
            END AS match_type,

            -- Match Rank (lower is better)
            CASE
                WHEN LOWER(p.{PEOPLE_DEPT_COL}) LIKE '%gts%'
                     AND p.{PEOPLE_POLE_COL} = b.{BUSINESS_POLE_COL}
                     AND p.{PEOPLE_EIR_COL} = b.{BUSINESS_EIR_COL}
                THEN 1

                WHEN LOWER(p.{PEOPLE_DEPT_COL}) NOT LIKE '%gts%'
                     AND p.{PEOPLE_POLE_COL} = b.{BUSINESS_POLE_COL}
                     AND p.{PEOPLE_SOUS_POLE_COL} = b.{BUSINESS_SOUS_POLE_COL}
                     AND p.{PEOPLE_EIR_COL} = b.{BUSINESS_EIR_COL}
                THEN 2

                WHEN p.{PEOPLE_EIR_COL} = b.{BUSINESS_EIR_COL}
                THEN 3

                WHEN bf.{BUSINESS_EIR_COL} IS NOT NULL
                THEN 4

                ELSE 99
            END AS match_rank,

            -- Confidence Score
            CASE
                WHEN LOWER(p.{PEOPLE_DEPT_COL}) LIKE '%gts%' THEN 100
                WHEN p.{PEOPLE_SOUS_POLE_COL} IS NOT NULL THEN 90
                WHEN p.{PEOPLE_EIR_COL} IS NOT NULL THEN 75
                WHEN bf.{BUSINESS_EIR_COL} IS NOT NULL THEN 60
                ELSE 0
            END AS confidence_score,

            -- Audit Flags
            (LOWER(p.{PEOPLE_DEPT_COL}) LIKE '%gts%') AS is_gts_department,
            (p.{PEOPLE_POLE_COL} IS NOT NULL) AS has_pole,
            (p.{PEOPLE_SOUS_POLE_COL} IS NOT NULL) AS has_sous_pole

        FROM {PEOPLE_TABLE} p

        LEFT JOIN business_dedup b
            ON p.{PEOPLE_EIR_COL} = b.{BUSINESS_EIR_COL}

        LEFT JOIN company_dedup c
            ON p.{PEOPLE_CODE_SERVICE_COL} = c.{COMPANY_CODE_SERVICE_COL}

        LEFT JOIN business_dedup bf
            ON c.{COMPANY_UID_COL} = bf.{BUSINESS_UID_COL};
    """)

    logging.info("Priority matching completed")

    # =========================================================
    # 5️⃣ Metrics Logging
    # =========================================================
    total = con.execute("SELECT COUNT(*) FROM final_output").fetchone()[0]
    unmatched = con.execute("""
        SELECT COUNT(*) FROM final_output
        WHERE match_type = 'NO_MATCH'
    """).fetchone()[0]

    logging.info(f"Total rows processed: {total}")
    logging.info(f"Unmatched rows: {unmatched}")

    # =========================================================
    # 6️⃣ Export Optimized Parquet
    # =========================================================
    con.execute("""
        COPY final_output
        TO 'final_output.parquet'
        (FORMAT PARQUET, COMPRESSION ZSTD);
    """)

    logging.info("Export completed successfully")

except Exception as e:
    logging.error(str(e))
    raise
