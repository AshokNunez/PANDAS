from pathlib import Path
import pandas as pd
import logging
import numpy as np

# -------------------------------
# Configuration
# -------------------------------
input_folder = Path("your_input_folder_here")
output_folder = Path("your_output_folder_here")
output_folder.mkdir(parents=True, exist_ok=True)

log_file = output_folder / "string_conversion.log"

# Columns to convert to string
COLUMNS_TO_CONVERT = [
    "business_code",
    "uid",
    "company"
]

# -------------------------------
# Logging Setup
# -------------------------------
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("=== Vectorized String Conversion Started ===")


# -------------------------------
# Vectorized Conversion Function
# -------------------------------
def convert_column_vectorized(series: pd.Series) -> pd.Series:
    """
    Vectorized conversion:
    - Converts to string
    - Removes trailing .0
    - Strips spaces
    - Preserves NaN
    """
    # Preserve null mask
    null_mask = series.isna()

    # Convert to string
    series = series.astype(str)

    # Remove trailing .0 (for floats converted to string)
    series = series.str.replace(r"\.0$", "", regex=True)

    # Strip spaces
    series = series.str.strip()

    # Restore NaN
    series[null_mask] = np.nan

    return series


# -------------------------------
# Process Files
# -------------------------------
for file in input_folder.iterdir():

    if file.suffix.lower() not in [".xlsx", ".csv"]:
        continue

    try:
        logging.info(f"Processing file: {file.name}")
        print(f"Processing {file.name}")

        # Read file
        if file.suffix.lower() == ".xlsx":
            df = pd.read_excel(file)
        else:
            df = pd.read_csv(file)

        # Convert only existing columns
        existing_cols = [c for c in COLUMNS_TO_CONVERT if c in df.columns]
        missing_cols = list(set(COLUMNS_TO_CONVERT) - set(existing_cols))

        if missing_cols:
            logging.warning(f"Missing columns skipped: {missing_cols}")

        for col in existing_cols:
            df[col] = convert_column_vectorized(df[col])
            logging.info(f"Converted column: {col}")

        # Save as parquet in output folder
        output_file = output_folder / f"{file.stem}.parquet"
        df.to_parquet(output_file, index=False)

        logging.info(f"Saved parquet: {output_file.name}")

    except Exception as e:
        logging.error(f"Error processing {file.name} - {str(e)}")

logging.info("=== Processing Completed Successfully ===")
print("Vectorized string conversion completed.")
