import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch
import pandas as pd
import warnings
from utils.load import load_to_postgres, load_to_csv, load_to_google_sheets, load

class TestLoad(unittest.TestCase):

    def setUp(self):
        # Sample DataFrame to test
        self.df = pd.DataFrame({
            'Title': ['Product 1', 'Product 2'],
            'Price': [10.0, 20.0],
            'Image URL': ['url1', 'url2'],
            'Rating': [5.0, 4.5],
            'Colors': ['Red', 'Blue'],
            'Size': ['M', 'L'],
            'Gender': ['Male', 'Female'],
            'Timestamp': pd.to_datetime(['2023-05-02', '2023-05-02'])
        })
        self.db_url = "postgresql://user:password@localhost/dbname"
        self.csv_file_path = "test_data.csv"
        self.spreadsheet_name = "TestSpreadsheet"

    @patch('utils.load.create_engine')
    def test_load_to_postgres(self, mock_create_engine):
        mock_engine = mock_create_engine.return_value
        # Mock method to_sql
        mock_conn = mock_engine.connect.return_value
        result = load_to_postgres(self.df, self.db_url)
        self.assertTrue(result)
            
    @patch('pandas.DataFrame.to_csv')
    def test_load_to_csv(self, mock_to_csv):
        mock_to_csv.return_value = None
        result = load_to_csv(self.df, self.csv_file_path)
        self.assertTrue(result)
        mock_to_csv.assert_called_once()

    @patch('utils.load.gspread.authorize')
    @patch('utils.load.ServiceAccountCredentials.from_json_keyfile_name')
    def test_load_to_google_sheets(self, mock_creds, mock_authorize):
        mock_client = mock_authorize.return_value
        mock_sheet = mock_client.open_by_key.return_value.get_worksheet.return_value

        mock_sheet.clear.return_value = None
        mock_sheet.append_rows.return_value = None

        result = load_to_google_sheets(self.df, self.spreadsheet_name)
        self.assertTrue(result)

    @patch('utils.load.load_to_postgres')
    @patch('utils.load.load_to_csv')
    @patch('utils.load.load_to_google_sheets')
    def test_load(self, mock_google_sheets, mock_csv, mock_postgres):
        mock_postgres.return_value = True
        mock_csv.return_value = True
        mock_google_sheets.return_value = True

        result = load(self.df, self.db_url, self.csv_file_path, self.spreadsheet_name)

        self.assertTrue(result['postgres'])
        self.assertTrue(result['csv'])
        self.assertTrue(result['google_sheets'])

        mock_postgres.assert_called_once()
        mock_csv.assert_called_once()
        mock_google_sheets.assert_called_once()

if __name__ == '__main__':
    unittest.main()
