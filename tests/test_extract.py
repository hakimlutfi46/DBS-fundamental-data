import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock
from utils.extract import extract
import pandas as pd

class TestExtract(unittest.TestCase):

    @patch('utils.extract.requests.get')
    def test_extract_data_success(self, mock_get):
        # Mock HTML content
        mock_html = """
        <div class="collection-card">
            <div class="product-title">Mock Product</div>
            <div class="price">$10</div>
            <img src="mock_image.jpg"/>
            <p>Rating: 4.5</p>
            <p>Colors Red</p>
            <p>Size: M</p>
            <p>Gender: Male</p>
        </div>
        """

        # Mock response object
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = mock_html
        mock_get.return_value = mock_response

        df = extract(max_pages=1)

        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]['Title'], "Mock Product")
        self.assertEqual(df.iloc[0]['Price'], "$10")
        self.assertEqual(df.iloc[0]['Image URL'], "mock_image.jpg")
        self.assertEqual(df.iloc[0]['Rating'], "4.5")
        self.assertEqual(df.iloc[0]['Colors'], "Red")
        self.assertEqual(df.iloc[0]['Size'], "M")
        self.assertEqual(df.iloc[0]['Gender'], "Male")
        self.assertTrue(isinstance(df.iloc[0]['Timestamp'], pd.Timestamp))

    @patch('utils.extract.requests.get')
    def test_extract_404(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        df = extract(max_pages=1)
        self.assertTrue(df.empty)

if __name__ == '__main__':
    unittest.main()
