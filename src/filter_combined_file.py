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

        # check if all the needed columns are in the df
        special_keys = {"columns_to_keep", "columns_to_remove"}
        missing_columns = []

        for key, value in conditions.items():
            if key in special_keys:
                for column in value:
                    if column not in df.columns:
                        missing_columns.append(column)
            else:
                if key not in df.columns:
                    missing_columns.append(key)
        if missing_columns:
            missing_columns_str = ", ".join(missing_columns)
            logging.error(f"The following columns are missing from the data: {missing_columns_str}. Exiting the function.")
            return

        # apply filtering conditions
        for key, condition in conditions.items():
            if key in special_keys:
                continue  # skip "columns_to_keep" and "columns_to_remove"

            condition_type = condition.get("type")
            value = condition.get("value")

            # check if the value is numeric/bool before applying conditions
            if not isinstance(value, (int, float, bool)):
                logging.warning(f"The value for column '{key}' in condition '{condition_type}' is not numeric: {value}. Skipping.")
                continue

            if condition_type == "greater_than":
                df = df[df[key] > value]
                logging.info(f"Applied 'greater_than' condition on column '{key}' with value {value}.")
            elif condition_type == "less_than":
                df = df[df[key] < value]
                logging.info(f"Applied 'less_than' condition on column '{key}' with value {value}.")
            elif condition_type == "equals":
                df = df[df[key] == value]
                logging.info(f"Applied 'equals' condition on column '{key}' with value {value}.")
            elif condition_type == "not_equals":
                df = df[df[key] != value]
                logging.info(f"Applied 'not_equals' condition on column '{key}' with value {value}.")
            else:
                logging.warning(f"Unsupported condition type '{condition_type}' for column '{key}'. Skipping.")

        # process columns to keep or remove
        columns_to_keep = conditions.get("columns_to_keep", None)
        columns_to_remove = conditions.get("columns_to_remove", None)

        if columns_to_keep is not None and columns_to_remove is not None:
            logging.warning("Both 'columns_to_keep' and 'columns_to_remove' are specified. 'columns_to_keep' will take precedence.")
            columns_to_remove = None

        if columns_to_keep is not None:
            df = df[columns_to_keep]
            logging.info(f"Kept only specified columns: {', '.join(columns_to_keep)}.")
        elif columns_to_remove is not None:
            df = df.drop(columns=columns_to_remove)
            logging.info(f"Removed specified columns: {', '.join(columns_to_remove)}.")

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
