import os
import sys
import unittest
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from filter_combined_file import filter_file

class TestFilterFile(unittest.TestCase):
    def setUp(self):
        self.test_file = os.path.join("tests_IO", "input_test_filtering.csv")
        self.output_file_1 = os.path.join("tests_IO", "filtered_output_error_1.csv")
        self.output_file_2 = os.path.join("tests_IO", "filtered_output_error_2.csv")

    def test_missing_column_error(self):
        """
      In this test, we check for missing column error handling.
      """
        conditions = {"D": {"type": "equals", "value": 10}}  # col "D" does not exist
        with self.assertLogs(level="ERROR") as log:
            filter_file(file_path=self.test_file, output_file=self.output_file_1, conditions=conditions)
        self.assertIn("The following columns are missing from the data: D.", log.output[0])

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

if __name__ == "__main__":
    unittest.main()
