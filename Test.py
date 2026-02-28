from pathlib import Path
import pandas as pd
import logging

# -------------------------------
# Configuration
# -------------------------------
folder = Path("your_folder_path_here")
log_file = folder / "conversion.log"

# -------------------------------
# Logging Setup
# -------------------------------
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("=== Conversion Started ===")

# -------------------------------
# Function to handle missing values
# -------------------------------
def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    
    # Fill numeric columns with 0
    numeric_cols = df.select_dtypes(include=["number"]).columns
    df[numeric_cols] = df[numeric_cols].fillna(0)

    # Fill string/object columns with 'Unknown'
    object_cols = df.select_dtypes(include=["object"]).columns
    df[object_cols] = df[object_cols].fillna("Unknown")

    return df


# -------------------------------
# File Processing
# -------------------------------
for file in folder.iterdir():

    if file.suffix.lower() in [".xlsx", ".csv"]:

        try:
            logging.info(f"Processing file: {file.name}")
            print(f"Processing {file.name}")

            # Read file
            if file.suffix.lower() == ".xlsx":
                df = pd.read_excel(file)
            else:
                df = pd.read_csv(file)

            # Log missing values before handling
            missing_count = df.isna().sum().sum()
            logging.info(f"Missing values found: {missing_count}")

            # Handle missing values
            df = handle_missing_values(df)

            # Convert to parquet
            parquet_path = file.with_suffix(".parquet")
            df.to_parquet(parquet_path, index=False)

            logging.info(f"Successfully converted: {parquet_path.name}")

        except Exception as e:
            logging.error(f"Error processing {file.name} - {str(e)}")

logging.info("=== Conversion Completed ===")
