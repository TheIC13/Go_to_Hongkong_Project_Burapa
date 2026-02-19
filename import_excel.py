import pandas as pd
import os

def import_excel(file_path, sheet_name=0):

    try:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        if not file_path.lower().endswith(".xlsx"):
            raise ValueError("Only .xlsx files are supported in this example.")
        df = pd.read_excel(file_path, sheet_name=sheet_name, engine="openpyxl")
        print(f"Successfully imported '{file_path}' (Sheet: {sheet_name})")
        return df

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return None

if __name__ == "__main__":
    excel_file = "data.xlsx"
    data = import_excel(excel_file)

    if data is not None:
        print(data.head())