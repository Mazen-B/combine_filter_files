import os
import sys
import unittest
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.combine_files import combine_files

class TestCombineFiles(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.join("tests_IO", "same_sized_files")
        self.output_file_1 = os.path.join("tests_IO", "combined_only_csvs.csv")
        self.output_file_2 = os.path.join("tests_IO", "combined_only_excel.xlsx")
        self.output_file_3 = os.path.join("tests_IO", "combined_both.csv")

    def test_combine_csv_files_only(self):
        """
      In this test, we check that only CSV files are correctly combined when file_type="csv".
      """ 
        combine_files(input_dir=self.test_dir, output_file=self.output_file_1, file_type="csv")

        # read the combined output
        combined_df = pd.read_csv(self.output_file_1)

        # expected combined DataFrame
        expected_df = pd.DataFrame({"A": [1, 2, 5, 6], "B": [3, 4, 7, 8]})

        # check that the combined output matches the expected DataFrame
        pd.testing.assert_frame_equal(combined_df, expected_df)

    def test_combine_xlsx_files_only(self):
        """
      In this test, we check that only excel files are correctly combined when file_type="excel".
      """
        combine_files(input_dir=self.test_dir, output_file=self.output_file_2, file_type="excel")

        # read the combined output
        combined_df = pd.read_excel(self.output_file_2)

        # expected combined DataFrame
        expected_df = pd.DataFrame({"A": [9, 10, 13, 14], "B": [11, 12, 15, 16]})

        # check that the combined output matches the expected DataFrame
        pd.testing.assert_frame_equal(combined_df, expected_df)

    def test_combine_both_csv_and_xlsx_files(self):
        """
      In this test, we check that both CSV and Excel files are combined correctly when file_type="both".
      """
        combine_files(input_dir=self.test_dir, output_file=self.output_file_3, file_type="both")

        # read the combined output
        combined_df = pd.read_csv(self.output_file_3)

        # expected combined DataFrame (CSV + Excel data, one csv file then one excel file order)
        expected_df = pd.DataFrame({
            "A": [1, 2, 9, 10, 5, 6, 13, 14],
            "B": [3, 4, 11, 12, 7, 8, 15, 16]
        })

        # check that the combined output matches the expected DataFrame
        pd.testing.assert_frame_equal(combined_df, expected_df)

if __name__ == "__main__":
    unittest.main()

