import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.load import load_to_postgres, load_to_csv, load_to_google_sheets, load

class TestLoad(unittest.TestCase):

    def setUp(self):
        # Sample DataFrame to test
        self.df = pd.DataFrame({
            'Title': ['Product 1', 'Product 2'],
            'Price': [10, 20],
            'Image URL': ['url1', 'url2'],
            'Rating': [5, 4],
            'Colors': ['Red', 'Blue'],
            'Size': ['M', 'L'],
            'Gender': ['Male', 'Female'],
            'Timestamp': ['2023-05-02', '2023-05-02']
        })
        self.db_url = "postgresql://user:password@localhost/dbname"
        self.csv_file_path = "data.csv"
        self.spreadsheet_name = "TestSpreadsheet"

    @patch('utils.load.load_to_postgres')
    def test_load_to_postgres(self, mock_postgres):
        mock_postgres.return_value = True
        result = load_to_postgres(self.df, self.db_url)
        self.assertTrue(result)
        mock_postgres.assert_called_once_with(self.df, self.db_url)

    @patch('utils.load.load_to_csv')
    def test_load_to_csv(self, mock_csv):
        mock_csv.return_value = True
        result = load_to_csv(self.df, self.csv_file_path)
        self.assertTrue(result)
        mock_csv.assert_called_once_with(self.df, self.csv_file_path)

    @patch('utils.load.load_to_google_sheets')
    def test_load_to_google_sheets(self, mock_google_sheets):
        mock_google_sheets.return_value = True
        result = load_to_google_sheets(self.df, self.spreadsheet_name)
        self.assertTrue(result)
        mock_google_sheets.assert_called_once_with(self.df, self.spreadsheet_name)

    @patch('utils.load.load_to_postgres')
    @patch('utils.load.load_to_csv')
    @patch('utils.load.load_to_google_sheets')

    def test_load(self, mock_google_sheets, mock_csv, mock_postgres):
        mock_postgres.return_value = True
        mock_csv.return_value = True
        mock_google_sheets.return_value = True

        result = load(self.df, self.db_url, self.csv_file_path, self.spreadsheet_name)
        
        self.assertEqual(result['postgres'], True)
        self.assertEqual(result['csv'], True)
        self.assertEqual(result['google_sheets'], True)

if __name__ == '__main__':
    unittest.main()
