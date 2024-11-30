import os
import sys
import unittest
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.filter_combined_file import filter_file, validate_conditions

class TestFilterFile(unittest.TestCase):
    def setUp(self):
        self.test_file = os.path.join("tests_IO", "input_test_filtering.csv")
        self.output_file_1 = os.path.join("tests_IO", "filtered_output_error_1.csv")
        self.output_file_2 = os.path.join("tests_IO", "filtered_output_error_2.csv")
        self.df_columns = pd.read_csv(self.test_file).columns.tolist()
    def test_missing_column_error(self):
        """
      In this test, we check for missing column error handling.
      """
        conditions = {"D": {"type": "equals", "value": 10}}  # col "D" does not exist
        with self.assertLogs(level="ERROR") as log:
            filter_file(file_path=self.test_file, output_file=self.output_file_1, conditions=conditions)
        self.assertIn("Value error: Column 'D' not found in the data. Please check the column names.", log.output[0])

    def test_unsupported_file_format(self):
        """
      In this test, we check for unsupported file format error.
      """
        unsupported_file = os.path.join("tests_IO", "unsupported.txt")
        with open(unsupported_file, "w") as f:
            f.write("Some text data")

        conditions = {"A": {"type": "greater_than", "value": 5}}
        with self.assertLogs(level="ERROR") as log:
            filter_file(file_path=unsupported_file, output_file=self.output_file_2, conditions=conditions)
        self.assertIn("Unsupported file format. Please select a CSV or Excel file.", log.output[0])

    def test_invalid_condition_type(self):
        """
      In this test, we check that an invalid condition type raises an error.
      """
        conditions = {"A": {"type": "invalid_type", "value": 5}}
        with self.assertRaises(ValueError) as context:
            validate_conditions(conditions, self.df_columns)
        self.assertIn("Unsupported condition type 'invalid_type' for column 'A'.", str(context.exception))

    def test_invalid_value_type(self):
        """
      In this test, we check that an invalid value type raises an error.
      """
        conditions = {"A": {"type": "greater_than", "value": "invalid_value"}}
        with self.assertRaises(TypeError) as context:
            validate_conditions(conditions, self.df_columns)
        self.assertIn("Condition 'greater_than' for column 'A' requires a numeric value.", str(context.exception))

if __name__ == "__main__":
    unittest.main()
