from pathlib import Path
import pandas as pd


class ExcelToParquetConverter:

    def __init__(self, input_folder, output_folder, fill_value="No-info"):
        self.input_folder = Path(input_folder)
        self.output_folder = Path(output_folder)
        self.fill_value = fill_value

        # Create output folder if it does not exist
        self.output_folder.mkdir(parents=True, exist_ok=True)

    def read_excel(self, file_path):
        """Read Excel file"""
        return pd.read_excel(file_path)

    def clean_data(self, df):
        """Fill missing values"""
        return df.fillna(self.fill_value)

    def save_parquet(self, df, output_file):
        """Save dataframe to parquet"""
        df.to_parquet(output_file, index=False)

    def process_file(self, file_path):
        """Process a single file"""
        try:
            df = self.read_excel(file_path)
            df = self.clean_data(df)

            output_file = self.output_folder / f"{file_path.stem}.parquet"
            self.save_parquet(df, output_file)

            print(f"Converted: {file_path.name} -> {output_file.name}")

        except Exception as e:
            print(f"Error processing {file_path.name}: {e}")

    def run(self):
        """Process all Excel files"""
        excel_files = list(self.input_folder.glob("*.xlsx"))

        for file in excel_files:
            self.process_file(file)


# ==========================
# Run the converter
# ==========================
if __name__ == "__main__":

    input_folder = "path_to_excel_folder"
    output_folder = "path_to_parquet_folder"

    converter = ExcelToParquetConverter(input_folder, output_folder)
    converter.run()
