import duckdb

# ==========================
# CONFIGURATION VARIABLES
# ==========================

PEOPLE_PARQUET = "parquet_folder/people_*.parquet"
BUSINESS_PARQUET = "parquet_folder/business_*.parquet"
OUTPUT_PARQUET = "output_folder/people_referential.parquet"

# Column Names (Change if needed)
PEOPLE_UID = "uid"
PEOPLE_BUSINESS_CODE = "business_code"
PEOPLE_EIR = "eir_code"
PEOPLE_POLE = "pole"
PEOPLE_SOUS_POLE = "sous_pole"
PEOPLE_DEPARTMENT = "department"

BUSINESS_CODE = "business_code"
BUSINESS_EIR = "eir_code"
BUSINESS_POLE = "pole"
BUSINESS_SOUS_POLE = "sous_pole"
BUSINESS_DEPARTMENT = "department"

# ==========================
# CONNECT
# ==========================

con = duckdb.connect()

# ==========================
# CREATE BASE TABLES
# ==========================

con.execute(f"""
CREATE OR REPLACE TABLE people AS
SELECT 
    *,
    TRIM(UPPER(CAST({PEOPLE_BUSINESS_CODE} AS VARCHAR))) AS business_code_clean,
    TRIM(UPPER(CAST({PEOPLE_EIR} AS VARCHAR))) AS eir_clean,
    TRIM(UPPER(CAST({PEOPLE_POLE} AS VARCHAR))) AS pole_clean,
    TRIM(UPPER(CAST({PEOPLE_SOUS_POLE} AS VARCHAR))) AS sous_pole_clean,
    TRIM(UPPER(CAST({PEOPLE_DEPARTMENT} AS VARCHAR))) AS dept_clean
FROM read_parquet('{PEOPLE_PARQUET}')
""")

con.execute(f"""
CREATE OR REPLACE TABLE business AS
SELECT 
    *,
    TRIM(UPPER(CAST({BUSINESS_CODE} AS VARCHAR))) AS business_code_clean,
    TRIM(UPPER(CAST({BUSINESS_EIR} AS VARCHAR))) AS eir_clean,
    TRIM(UPPER(CAST({BUSINESS_POLE} AS VARCHAR))) AS pole_clean,
    TRIM(UPPER(CAST({BUSINESS_SOUS_POLE} AS VARCHAR))) AS sous_pole_clean,
    TRIM(UPPER(CAST({BUSINESS_DEPARTMENT} AS VARCHAR))) AS dept_clean
FROM read_parquet('{BUSINESS_PARQUET}')
""")

# ==========================
# STEP 1 (PRIORITY MATCH)
# eir + pole + department contains 'GTS'
# ==========================

con.execute("""
CREATE OR REPLACE TABLE step1_match AS
SELECT *
FROM (
    SELECT 
        p.*,
        b.*,
        ROW_NUMBER() OVER (PARTITION BY p.uid ORDER BY b.business_code_clean) rn
    FROM people p
    LEFT JOIN business b
      ON p.eir_clean = b.eir_clean
     AND p.pole_clean = b.pole_clean
     AND b.dept_clean LIKE '%GTS%'
) t
WHERE rn = 1
""")

# ==========================
# STEP 2 (SECOND PRIORITY)
# eir + pole + sous_pole
# ==========================

con.execute("""
CREATE OR REPLACE TABLE step2_match AS
SELECT *
FROM (
    SELECT 
        p.*,
        b.*,
        ROW_NUMBER() OVER (PARTITION BY p.uid ORDER BY b.business_code_clean) rn
    FROM people p
    LEFT JOIN business b
      ON p.eir_clean = b.eir_clean
     AND p.pole_clean = b.pole_clean
     AND p.sous_pole_clean = b.sous_pole_clean
    WHERE p.uid NOT IN (SELECT uid FROM step1_match)
) t
WHERE rn = 1
""")

# ==========================
# STEP 3 (NORMAL BUSINESS_CODE MATCH)
# ==========================

con.execute("""
CREATE OR REPLACE TABLE normal_match AS
SELECT *
FROM (
    SELECT 
        p.*,
        b.*,
        ROW_NUMBER() OVER (PARTITION BY p.uid ORDER BY b.business_code_clean) rn
    FROM people p
    LEFT JOIN business b
      ON p.business_code_clean = b.business_code_clean
    WHERE p.uid NOT IN (
        SELECT uid FROM step1_match
        UNION
        SELECT uid FROM step2_match
    )
) t
WHERE rn = 1
""")

# ==========================
# FINAL UNION
# ==========================

con.execute("""
CREATE OR REPLACE TABLE people_referential AS
SELECT * FROM step1_match
UNION ALL
SELECT * FROM step2_match
UNION ALL
SELECT * FROM normal_match
""")

# ==========================
# REMOVE DUPLICATE PEOPLE (SAFETY)
# ==========================

con.execute("""
CREATE OR REPLACE TABLE people_referential AS
SELECT *
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY uid ORDER BY business_code_clean) rn
    FROM people_referential
) t
WHERE rn = 1
""")

# ==========================
# EXPORT TO PARQUET
# ==========================

con.execute(f"""
COPY people_referential TO '{OUTPUT_PARQUET}' (FORMAT PARQUET);
""")

con.close()

print("✅ Referential Mapping Completed Successfully")
