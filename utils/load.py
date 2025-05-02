from typing import Dict
import pandas as pd
import traceback
from sqlalchemy import create_engine
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def load_to_postgres(df: pd.DataFrame, db_url: str) -> bool:
    """
    Load data to PostgreSQL database.

    Args:
        df (pd.DataFrame): Data to be loaded.
        db_url (str): Database URL.

    Returns:
        bool: Success status.
    """
    try:
        # Create database engine and load data into 'products' table
        engine = create_engine(db_url)
        df.to_sql("products", engine, index=False, if_exists="replace")
        return True
    except Exception as e:
        print(f"Error loading to PostgreSQL: {e}")
        return False

def load_to_csv(df: pd.DataFrame, csv_file_path: str) -> bool:
    """
    Save data to CSV.

    Args:
        df (pd.DataFrame): Data to be saved.
        csv_file_path (str): Path where CSV will be saved.

    Returns:
        bool: Success status.
    """
    try:
        # Save the DataFrame to a CSV file
        df.to_csv(csv_file_path, index=False)
        return True
    except Exception as e:
        print(f"Error loading to CSV: {e}")
        return False

def load_to_google_sheets(df: pd.DataFrame, spreadsheet_name: str) -> bool:
    """
    Load data to Google Sheets.

    Args:
        df (pd.DataFrame): Data to be loaded.
        spreadsheet_name (str): Name of the Google Sheets file.

    Returns:
        bool: Success status.
    """
    try:
        # Konversi semua kolom dengan tipe Timestamp ke format string (ISO 8601)
        for col in df.select_dtypes(include=['datetime64[ns]']).columns:
            df[col] = df[col].apply(lambda x: x.isoformat() if isinstance(x, pd.Timestamp) else x)

        creds_json = "google-sheets-api.json"
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scope)
        client = gspread.authorize(creds)

        spreadsheet = client.open_by_key('1pvsfeNJHMKS-xevuULc2wOAhUICzBNt6hRGG7BlMdZE')
        sheet = spreadsheet.get_worksheet(0)

        # Clear existing data
        sheet.clear()

        # Tambahkan header + data
        data = [df.columns.tolist()] + df.values.tolist()
        sheet.append_rows(data, value_input_option="USER_ENTERED")

        return True
    except Exception as e:
        print(f"Error loading to Google Sheets: {e}")
        traceback.print_exc()
        return False

    

def load(df: pd.DataFrame, db_url: str, csv_file_path: str, spreadsheet_name: str) -> Dict[str, bool]:
    """
    Load cleaned data to various storage destinations.

    Args:
        df (pd.DataFrame): Cleaned data to be loaded.
        db_url (str): Database URL.
        csv_file_path (str): Path to the CSV file.
        spreadsheet_name (str): Name of the Google Sheets file.

    Returns:
        Dict[str, bool]: Dictionary indicating success status for each destination.
    """
    result = {}

    # Load data to PostgreSQL
    result["postgres"] = load_to_postgres(df, db_url)
    
    # Load data to CSV
    result["csv"] = load_to_csv(df, csv_file_path)
    
    # Load data to Google Sheets
    result["google_sheets"] = load_to_google_sheets(df, spreadsheet_name)

    return result
