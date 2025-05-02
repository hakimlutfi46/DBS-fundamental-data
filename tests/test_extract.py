import unittest
from unittest.mock import patch, MagicMock
from utils.extract import extract

class TestExtract(unittest.TestCase):

    @patch('utils.extract.extract_data')
    def test_extract_data(self, mock_extract):
        # Assuming your extract function returns some data
        mock_extract.return_value = ['item1', 'item2', 'item3']
        
        result = extract("https://example.com")
        self.assertEqual(result, ['item1', 'item2', 'item3'])
        mock_extract.assert_called_once_with("https://example.com")

if __name__ == '__main__':
    unittest.main()
