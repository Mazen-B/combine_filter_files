import os
import logging
import pandas as pd

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def validate_conditions(conditions, df_columns):
    """
  This function validates conditions for filtering to ensure they are properly formed.
  """
    special_keys = {"columns_to_keep", "columns_to_remove"}

    for key, condition in conditions.items():
        if key in special_keys:
            # validate that the condition is a list
            if not isinstance(condition, list):
                raise ValueError(f"'{key}' should be a list of columns.")
            
            # check if all columns in the list are valid
            invalid_columns = [col for col in condition if col not in df_columns]
            if invalid_columns:
                raise ValueError(f"The following columns in '{key}' are not valid: {', '.join(invalid_columns)}")
        else:
            if key not in df_columns:
                raise ValueError(f"Column '{key}' not found in the data. Please check the column names.")
            
            condition_type = condition.get("type")
            value = condition.get("value")

            # validate condition type
            if condition_type not in {"greater_than", "less_than", "equals", "not_equals"}:
                raise ValueError(f"Unsupported condition type '{condition_type}' for column '{key}'.")

            # validate value type for each condition type
            if condition_type in {"greater_than", "less_than"} and not isinstance(value, (int, float)):
                raise TypeError(f"Condition '{condition_type}' for column '{key}' requires a numeric value.")
            if condition_type in {"equals", "not_equals"} and not isinstance(value, (int, float)):
                raise TypeError(f"Condition '{condition_type}' for column '{key}' requires a numeric value.")

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
            raise ValueError("Unsupported file format. Please select a CSV or Excel file.")

        # ensure the output directory exists
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            logging.info(f"Created directory for output file at: {output_dir}")

        # validate conditions
        validate_conditions(conditions, df.columns)

        # apply filtering conditions
        for key, condition in conditions.items():
            if key in {"columns_to_keep", "columns_to_remove"}:
                continue  # skip special keys

            condition_type = condition.get("type")
            value = condition.get("value")

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

        # process columns to keep or remove
        columns_to_keep = conditions.get("columns_to_keep", None)
        columns_to_remove = conditions.get("columns_to_remove", None)

        if columns_to_keep and columns_to_remove:
            logging.warning("Both 'columns_to_keep' and 'columns_to_remove' are specified. 'columns_to_keep' will take precedence.")
            columns_to_remove = None

        if columns_to_keep:
            df = df[columns_to_keep]
            logging.info(f"Kept only specified columns: {', '.join(columns_to_keep)}.")
        elif columns_to_remove:
            df = df.drop(columns=columns_to_remove)
            logging.info(f"Removed specified columns: {', '.join(columns_to_remove)}.")

        # save the filtered data
        if output_file.endswith(".csv"):
            df.to_csv(output_file, index=False, float_format="%.15g")
            logging.info(f"Filtered data saved to '{output_file}' as CSV.")
        elif output_file.endswith(".xlsx"):
            df.to_excel(output_file, index=False)
            logging.info(f"Filtered data saved to '{output_file}' as Excel.")
        else:
            raise ValueError("Output file must be either .csv or .xlsx.")

    except FileNotFoundError:
        logging.error("The specified file was not found. Please check the file path.")
    except PermissionError:
        logging.error(f"Permission denied. Unable to write to '{output_file}'.")
    except pd.errors.EmptyDataError:
        logging.warning("The file is empty. No data to filter.")   
    except ValueError as ve:
        logging.error(f"Value error: {ve}")
    except TypeError as te:
        logging.error(f"Type error: {te}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
