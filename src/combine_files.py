import os
import logging
import pandas as pd

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


def validate_directory(input_dir, output_file):
    """
  This function ensures that the input directory exists and create output directory if needed.
  """
    if not os.path.isdir(input_dir):
        logging.error("Specified directory does not exist. Please check the path.")
        return False

    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        logging.info(f"Created directory for output file at: {output_dir}")

    return True

def get_files(input_dir, file_type, output_file):
    """
  This function gets files of specified type from input directory and validate output file extension.
  """
    if file_type == "csv":
        files = [f for f in os.listdir(input_dir) if f.endswith(".csv")]
        if not output_file.endswith(".csv"):
            logging.error("Output file extension does not match the specified file_type 'csv'.")
            return None
    elif file_type == "excel":
        files = [f for f in os.listdir(input_dir) if f.endswith(".xlsx")]
        if not output_file.endswith(".xlsx"):
            logging.error("Output file extension does not match the specified file_type 'excel'.")
            return None
    elif file_type == "both":
        files = [f for f in os.listdir(input_dir) if f.endswith(".csv") or f.endswith(".xlsx")]
    else:
        logging.error("Invalid file_type specified. Choose 'csv', 'excel', or 'both'.")
        return None

    if not files:
        logging.warning(f"No {file_type.upper()} files found in the directory.")
        return None

    return files

def check_column_consistency(df, columns_list):
    """
  This function checks if the DataFrame's columns are consistent with the initial columns in both names and order.
  """
    if columns_list is None:
        return list(df.columns)
    elif list(df.columns) != columns_list:
        logging.error("Not all files have the same columns or column order. Aborting combination.")
        return None
    return columns_list

def read_file(file_path):
    """
  This function reads a file into a DataFrame, handling CSV and Excel formats and logging any errors.
  """
    try:
        if file_path.endswith(".csv"):
            return pd.read_csv(file_path)
        elif file_path.endswith(".xlsx"):
            return pd.read_excel(file_path)
        else:
            logging.warning(f"Skipping unsupported file format for {file_path}.")
            return None
    except pd.errors.EmptyDataError:
        logging.warning(f"File {file_path} is empty. Skipping.")
    except pd.errors.ParserError:
        logging.error(f"File {file_path} could not be parsed. Skipping.")
    except Exception as e:
        logging.error(f"An error occurred while processing {file_path}: {e}")
    return None

def combine_and_save(df_list, output_file):
    """
  This function combines DataFrames and save to the specified output file.
  """
    if not df_list:
        logging.warning("No valid files to combine after processing.")
        return

    combined_df = pd.concat(df_list, ignore_index=True)
    logging.info("DataFrames combined successfully.")

    try:
        if output_file.endswith(".csv"):
            combined_df.to_csv(output_file, index=False, float_format="%.15g")
        elif output_file.endswith(".xlsx"):
            combined_df.to_excel(output_file, index=False)
        else:
            logging.error("Output file must be either .csv or .xlsx")
            return

        logging.info(f"Files combined and saved successfully into {output_file}.")
    except PermissionError:
        logging.error(f"Permission denied. Unable to write to {output_file}.")
    except Exception as e:
        logging.error(f"An unexpected error occurred while writing the file: {e}")


def combine_files(input_dir, output_file, file_type="both"):
    """
  This is the main function to combine files based on file type and save to output file.
  """
    if not validate_directory(input_dir, output_file):
        return

    files = get_files(input_dir, file_type, output_file)
    if files is None:
        return

    df_list = []
    columns_list = None

    for file in files:
        file_path = os.path.join(input_dir, file)
        df = read_file(file_path)

        if df is not None:
            columns_list = check_column_consistency(df, columns_list)
            if columns_list is None:
                return  # Abort if columns are inconsistent
            df_list.append(df)
            logging.info(f"File {file} successfully read and appended.")

    combine_and_save(df_list, output_file)
