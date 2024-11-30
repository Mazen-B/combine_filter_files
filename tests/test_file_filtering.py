import os
import sys
import unittest
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.filter_combined_file import filter_file

class TestFilterFile(unittest.TestCase):
    def setUp(self):
        self.test_file = os.path.join("tests_IO", "input_test_filtering.csv")
        self.output_file_1 = os.path.join("tests_IO", "filtered_output_1.csv")
        self.output_file_2 = os.path.join("tests_IO", "filtered_output_2.csv")
        self.output_file_3 = os.path.join("tests_IO", "filtered_output_3.csv")
        self.output_file_4 = os.path.join("tests_IO", "filtered_output_4.csv")
        self.output_file_5 = os.path.join("tests_IO", "filtered_output_5.csv")
        self.output_file_6 = os.path.join("tests_IO", "filtered_output_6.csv")

    def test_greater_than_filter(self):
        """
      In this test, we check the filtering with a "greater_than" condition.
      """
        conditions = {"A": {"type": "greater_than", "value": 10}}
        filter_file(file_path=self.test_file, output_file=self.output_file_1, conditions=conditions)
        filtered_df = pd.read_csv(self.output_file_1)

        expected_df = pd.DataFrame({"A": [15, 20], "B": [16, 21], "C": [17, 22]})
        pd.testing.assert_frame_equal(filtered_df, expected_df)

    def test_less_than_filter(self):
        """
      In this test, we check the filtering with a "less_than" condition.
      """
        conditions = {"B": {"type": "less_than", "value": 10}}
        filter_file(file_path=self.test_file, output_file=self.output_file_2, conditions=conditions)
        filtered_df = pd.read_csv(self.output_file_2)

        expected_df = pd.DataFrame({"A": [1, 5], "B": [2, 6], "C": [3, 7]})
        pd.testing.assert_frame_equal(filtered_df, expected_df)

    def test_equals_filter(self):
        """
      In this test, we check the filtering with an "equals" condition.
      """
        conditions = {"C": {"type": "equals", "value": 12}}
        filter_file(file_path=self.test_file, output_file=self.output_file_3, conditions=conditions)
        filtered_df = pd.read_csv(self.output_file_3)

        expected_df = pd.DataFrame({"A": [10], "B": [11], "C": [12]})
        pd.testing.assert_frame_equal(filtered_df, expected_df)

    def test_not_equals_filter(self):
        """
      In this test, we check the filtering with a "not_equals" condition.
      """
        conditions = {"A": {"type": "not_equals", "value": 5}}
        filter_file(file_path=self.test_file, output_file=self.output_file_4, conditions=conditions)
        filtered_df = pd.read_csv(self.output_file_4)

        expected_df = pd.DataFrame({"A": [1, 10, 15, 20], "B": [2, 11, 16, 21], "C": [3, 12, 17, 22]})
        pd.testing.assert_frame_equal(filtered_df, expected_df)

    def test_columns_to_keep(self):
        """
      In this test, we check the filtering with a "columns_to_keep" condition.
      """
        conditions = {"columns_to_keep": ["A"]}
        filter_file(file_path=self.test_file, output_file=self.output_file_5, conditions=conditions)
        filtered_df = pd.read_csv(self.output_file_5)

        expected_df = pd.DataFrame({"A": [1, 5, 10, 15, 20]})
        pd.testing.assert_frame_equal(filtered_df, expected_df)

    def test_columns_to_remove(self):
        """
      In this test, we check the filtering with a "columns_to_remove" condition.
      """
        conditions = {"columns_to_remove": ["B"]}
        filter_file(file_path=self.test_file, output_file=self.output_file_6, conditions=conditions)
        filtered_df = pd.read_csv(self.output_file_6)

        expected_df = pd.DataFrame({"A": [1, 5, 10, 15, 20], "C": [3, 7, 12, 17, 22]})
        pd.testing.assert_frame_equal(filtered_df, expected_df)

if __name__ == "__main__":
    unittest.main()
