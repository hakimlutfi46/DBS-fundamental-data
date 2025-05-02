import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock, mock_open
import pandas as pd
from sqlalchemy import exc
from utils.load import (
    load_to_postgres,
    load_to_csv,
    load_to_google_sheets,
    load
)

class TestLoadFunctions(unittest.TestCase):
    def setUp(self):
        self.sample_df = pd.DataFrame({
            'id': [1, 2],
            'name': ['A', 'B'],
            'date': pd.to_datetime(['2023-01-01', '2023-01-02'])
        })
        self.empty_df = pd.DataFrame()
        self.db_url = "postgresql://user:pass@localhost/db"
        self.csv_path = "test.csv"
        self.sheet_id = "test_sheet_id"

    # Test load_to_postgres
    @patch('utils.load.create_engine')
    def test_load_to_postgres_success(self, mock_engine):
        mock_conn = MagicMock()
        mock_engine.return_value.begin.return_value.__enter__.return_value = mock_conn
        self.assertTrue(load_to_postgres(self.sample_df, self.db_url))

    @patch('utils.load.create_engine')
    def test_load_to_postgres_db_error(self, mock_engine):
        mock_engine.return_value.begin.side_effect = exc.SQLAlchemyError("DB error")
        self.assertFalse(load_to_postgres(self.sample_df, self.db_url))

    def test_load_to_postgres_empty_df(self):
        self.assertFalse(load_to_postgres(self.empty_df, self.db_url))

    # Test load_to_csv
    @patch('builtins.open', new_callable=mock_open)
    @patch('pandas.DataFrame.to_csv')
    def test_load_to_csv_success(self, mock_to_csv, mock_file):
        self.assertTrue(load_to_csv(self.sample_df, self.csv_path))

    @patch('pandas.DataFrame.to_csv', side_effect=PermissionError("No write permission"))
    def test_load_to_csv_io_error(self, mock_to_csv):
        self.assertFalse(load_to_csv(self.sample_df, self.csv_path))

    def test_load_to_csv_empty_df(self):
        self.assertFalse(load_to_csv(self.empty_df, self.csv_path))

    # Test load_to_google_sheets
    @patch('utils.load.gspread.authorize')
    @patch('utils.load.ServiceAccountCredentials.from_json_keyfile_name')
    def test_load_to_google_sheets_success(self, mock_creds, mock_auth):
        mock_client = MagicMock()
        mock_auth.return_value = mock_client
        mock_sheet = MagicMock()
        mock_client.open_by_key.return_value.get_worksheet.return_value = mock_sheet
        self.assertTrue(load_to_google_sheets(self.sample_df, self.sheet_id))

    @patch('utils.load.ServiceAccountCredentials.from_json_keyfile_name', 
           side_effect=FileNotFoundError("No creds file"))
    def test_load_to_google_sheets_cred_error(self, mock_creds):
        self.assertFalse(load_to_google_sheets(self.sample_df, self.sheet_id))

    @patch('utils.load.gspread.authorize')
    @patch('utils.load.ServiceAccountCredentials.from_json_keyfile_name')
    def test_load_to_google_sheets_api_error(self, mock_creds, mock_auth):
        mock_auth.return_value.open_by_key.side_effect = Exception("API error")
        self.assertFalse(load_to_google_sheets(self.sample_df, self.sheet_id))

    def test_load_to_google_sheets_empty_df(self):
        self.assertFalse(load_to_google_sheets(self.empty_df, self.sheet_id))

    # Test load function
    @patch('utils.load.load_to_postgres', return_value=True)
    @patch('utils.load.load_to_csv', return_value=True)
    @patch('utils.load.load_to_google_sheets', return_value=True)
    def test_load_success(self, mock_gsheets, mock_csv, mock_pg):
        result = load(self.sample_df, self.db_url, self.csv_path, self.sheet_id)
        self.assertTrue(all(result.values()))

    @patch('utils.load.load_to_postgres', return_value=False)
    @patch('utils.load.load_to_csv', return_value=True)
    @patch('utils.load.load_to_google_sheets', return_value=False)
    def test_load_partial_failure(self, mock_gsheets, mock_csv, mock_pg):
        result = load(self.sample_df, self.db_url, self.csv_path, self.sheet_id)
        self.assertEqual(result, {
            "postgres": False,
            "csv": True,
            "google_sheets": False
        })

    def test_load_invalid_input(self):
        result = load("not a dataframe", self.db_url, self.csv_path, self.sheet_id)
        self.assertFalse(any(result.values()))

if __name__ == '__main__':
    unittest.main()