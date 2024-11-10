import os
import logging
import pandas as pd

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def filter_file(file_path, output_file, conditions):
    """
  This function filters data in a CSV or Excel file based on specified conditions.
  """
    try:
        # load the file based on its extension
        if file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
            logging.info(f"Excel file '{file_path}' loaded successfully.")
        elif file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
            logging.info(f"CSV file '{file_path}' loaded successfully.")
        else:
            logging.error("Unsupported file format. Please select a CSV or Excel file.")
            return

        # ensure the output directory exists
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            logging.info(f"Created directory for output file at: {output_dir}")

        # convert DataFrame columns to lowercase for case-insensitive matching
        df.columns = [col.lower() for col in df.columns]
        
        # check if all specified columns are in the DataFrame
        missing_columns = [column for column in conditions if column.lower() not in df.columns]
        if missing_columns:
            missing_columns_str = ", ".join(missing_columns)
            logging.error(f"The following columns are missing from the data: {missing_columns_str}. Exiting the function.")
            return
        
        # apply filtering conditions
        for column, condition in conditions.items():
            column_lower = column.lower()
            
            condition_type = condition.get("type")
            value = condition.get("value")

            # check if the value is an int or float before applying conditions
            if not isinstance(value, (int, float)):
                logging.warning(f"The value for column '{column}' in condition '{condition_type}' is not numeric: {value}. Skipping.")
                continue

            if condition_type == "greater_than":
                df = df[df[column_lower] > value]
                logging.info(f"Applied 'greater_than' condition on column '{column}' with value {value}.")
            elif condition_type == "less_than":
                df = df[df[column_lower] < value]
                logging.info(f"Applied 'less_than' condition on column '{column}' with value {value}.")
            elif condition_type == "equals":
                df = df[df[column_lower] == value]
                logging.info(f"Applied 'equals' condition on column '{column}' with value {value}.")
            elif condition_type == "not_equals":
                df = df[df[column_lower] != value]
                logging.info(f"Applied 'not_equals' condition on column '{column}' with value {value}.")
            else:
                logging.warning(f"Unsupported condition type '{condition_type}' for column '{column}'. Skipping.")

        # save the filtered data
        try:
            if output_file.endswith(".csv"):
                df.to_csv(output_file, index=False, float_format="%.15g")
                logging.info(f"Filtered data saved to '{output_file}' as CSV.")
            elif output_file.endswith(".xlsx"):
                df.to_excel(output_file, index=False)
                logging.info(f"Filtered data saved to '{output_file}' as Excel.")
            else:
                logging.error("Output file must be either .csv or .xlsx")
        except PermissionError:
            logging.error(f"Permission denied. Unable to write to '{output_file}'.")
        except Exception as e:
            logging.error(f"An unexpected error occurred while saving the file: {e}")

    except FileNotFoundError:
        logging.error("The specified file was not found. Please check the file path.")
    except pd.errors.EmptyDataError:
        logging.warning("The file is empty. No data to filter.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
