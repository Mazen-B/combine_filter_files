import os
import sys
import unittest
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from combine_files import combine_files

class TestCombineFilesErrors(unittest.TestCase):
    def setUp(self):
        self.test_dir_1 = os.path.join("tests_IO", "diff_sized_files")
        self.test_dir_2 = os.path.join("tests_IO", "diff_col_names")
        self.test_dir_3 = os.path.join("tests_IO", "empty_cells")
        self.output_file_1 = os.path.join("tests_IO", "output_mismatch.csv")
        self.output_file_2 = os.path.join("tests_IO", "output_inconsistent_size.csv")
        self.output_file_3 = os.path.join("tests_IO", "output_inconsistent_name.csv")
        self.output_file_4 = os.path.join("tests_IO", "output_empty_cells.csv")

    def test_mismatched_file_type(self):
        """
      In this test, we check if an error is raised when file_type="excel" but output file is a CSV.
      """
        with self.assertLogs(level="ERROR") as log:
            combine_files(input_dir=self.test_dir_1, output_file=self.output_file_1, file_type="excel")
        
        # verify error log about file type mismatch
        self.assertIn("Output file extension does not match the specified file_type 'excel'.", log.output[0])

    def test_inconsistent_col_sizes(self):
        """
      In this test, we check if an error is raised when combining files with inconsistent column sizes.
      """
        # expect a warning about inconsistent columns
        with self.assertLogs(level="ERROR") as log:
            combine_files(input_dir=self.test_dir_1, output_file=self.output_file_2, file_type="csv")
        
        # verify error log about inconsistent columns
        self.assertIn("Files have inconsistent columns or data types. Aborting combination.", log.output[0])

    def test_inconsistent_col_name(self):
        """
      In this test, we check if an error is raised when combining files with inconsistent column names.
      """
        # expect a warning about inconsistent columns
        with self.assertLogs(level="ERROR") as log:
            combine_files(input_dir=self.test_dir_2, output_file=self.output_file_3, file_type="csv")
        
        # verify updated error log about inconsistent columns or data types
        self.assertIn("Files have inconsistent columns or data types. Aborting combination.", log.output[0])

    def test_combine_csv_files_only(self):
        """
      In this test, we check that empty cells in the CSV files are correctly added.
      """ 
        combine_files(input_dir=self.test_dir_3, output_file=self.output_file_4, file_type="csv")

        # read the combined output
        combined_df = pd.read_csv(self.output_file_4)

        # expected combined DataFrame
        expected_df = pd.DataFrame({
            "A": [1, 3, 5, 6, 15, 16],
            "B": [np.nan, 4, 7, 8, 17, np.nan],
            "C": [5, np.nan, 9, 10, 19, np.nan]
        })
        # check that the combined output matches the expected DataFrame
        pd.testing.assert_frame_equal(combined_df, expected_df)

if __name__ == "__main__":
    unittest.main()
