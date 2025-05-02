import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import pandas as pd
import numpy as np
from utils.transform import transform, clean_rating

class TestTransform(unittest.TestCase):

    def setUp(self):
        self.raw_data = pd.DataFrame({
            "Title": ["T-shirt", "Unknown", "Shirt"],
            "Rating": ["4.5", "Invalid", "Not Available"],
            "Price": ["$10.00", "Unavailable", "$20.00"],
            "Colors": ["Colors 3", "Colors 2", "Colors 1"],
            "Size": ["Medium", "Large", "Unknown"],
            "Gender": ["Male", "Female", "Unisex"],
            "Timestamp": ["2023-01-01", "Invalid Date", "2023-05-02"]
        })

    def test_clean_rating(self):
        self.assertEqual(clean_rating("4.5"), 4.5)
        self.assertEqual(clean_rating("Rating: 3.2"), 3.2)
        self.assertTrue(np.isnan(clean_rating("Invalid")))
        self.assertTrue(np.isnan(clean_rating(None)))

    def test_transform_valid_input(self):
        transformed = transform(self.raw_data)
        # Only 1 valid row should remain after dropna
        self.assertEqual(len(transformed), 1)
        row = transformed.iloc[0]
        self.assertEqual(row['Title'], 't-shirt')
        self.assertAlmostEqual(row['Rating'], 4.5)
        self.assertAlmostEqual(row['Price'], 160000.0)
        self.assertEqual(row['Colors'], 3)
        self.assertEqual(row['Size'], 'M')
        self.assertEqual(row['Gender'], 'Men')
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(transformed['Timestamp']))

    def test_transform_missing_columns(self):
        # Remove one required column
        df_missing = self.raw_data.drop(columns=['Rating'])
        with self.assertRaises(KeyError):
            transform(df_missing)

    def test_transform_non_dataframe_input(self):
        with self.assertRaises(ValueError):
            transform("not a dataframe")

    def test_transform_none_input(self):
        result = transform(None)
        self.assertTrue(result.empty)

if __name__ == '__main__':
    unittest.main()
