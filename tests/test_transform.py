import unittest
import pandas as pd
import numpy as np
from utils.transform import clean_rating, transform

class TestTransform(unittest.TestCase):

    def setUp(self):
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

    def test_transform(self):
        transformed_df = transform(self.df)
        
        # Add checks to verify the transformation
        self.assertTrue('TransformedColumn' in transformed_df.columns)
        self.assertEqual(transformed_df.shape, (2, 9))  # Example: 2 rows and 9 columns after transformation

    def test_clean_rating_valid(self):
        # Test a valid rating value
        rating = "4.5"
        cleaned_rating = clean_rating(rating)
        self.assertEqual(cleaned_rating, 4.5)

    def test_clean_rating_invalid(self):
        # Test an invalid rating value
        rating = "invalid"
        cleaned_rating = clean_rating(rating)
        self.assertTrue(np.isnan(cleaned_rating))

    def test_clean_rating_edge_case(self):
        # Test a rating with a value that has no digits
        rating = "N/A"
        cleaned_rating = clean_rating(rating)
        self.assertTrue(np.isnan(cleaned_rating))

    def test_clean_rating_empty(self):
        # Test an empty string or None
        rating = ""
        cleaned_rating = clean_rating(rating)
        self.assertTrue(np.isnan(cleaned_rating))

if __name__ == '__main__':
    unittest.main()
