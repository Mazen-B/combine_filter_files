import os
import logging
import pandas as pd

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


def combine_files(input_dir, output_file, file_type="both"):
    """
  This function combines files in a directory based on specified file type.
  """    
    try:
        # ensure the input and output dir exist
        if not os.path.isdir(input_dir):
            logging.error("Specified directory does not exist. Please check the path.")
            return
        
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            logging.info(f"Created directory for output file at: {output_dir}")
    
        # determine which files to include based on the file_type parameter
        if file_type == "csv":
            files = [f for f in os.listdir(input_dir) if f.endswith(".csv")]
            if not output_file.endswith(".csv"):
                logging.error("Output file extension does not match the specified file_type 'csv'.")
                return
        elif file_type == "excel":
            files = [f for f in os.listdir(input_dir) if f.endswith(".xlsx")]
            if not output_file.endswith(".xlsx"):
                logging.error("Output file extension does not match the specified file_type 'excel'.")
                return
        elif file_type == "both":
            files = [f for f in os.listdir(input_dir) if f.endswith(".csv") or f.endswith(".xlsx")]
        else:
            logging.error("Invalid file_type specified. Choose 'csv', 'excel', or 'both'.")
            return
        
        if not files:
            logging.warning(f"No {file_type.upper()} files found in the directory.")
            return
        
        df_list = []
        columns_set = None
        
        # process each file
        for file in files:
            file_path = os.path.join(input_dir, file)
            try:
                if file.endswith(".csv"):
                    df = pd.read_csv(file_path)
                elif file.endswith(".xlsx"):
                    df = pd.read_excel(file_path)
                else:
                    logging.warning(f"Skipping unsupported file format for {file}.")
                    continue
                
                # validate columns consistency
                if columns_set is None:
                    columns_set = set(df.columns)
                elif set(df.columns) != columns_set:
                    logging.warning(f"Inconsistent columns in {file}. Skipping this file.")
                    continue

                df_list.append(df)
                logging.info(f"File {file} successfully read and appended.")
            except pd.errors.EmptyDataError:
                logging.warning(f"File {file} is empty. Skipping.")
            except pd.errors.ParserError:
                logging.error(f"File {file} could not be parsed. Skipping.")
            except Exception as e:
                logging.error(f"An error occurred while processing {file}: {e}")
        
        if not df_list:
            logging.warning("No valid files to combine after processing.")
            return

        # combine all dataframes
        combined_df = pd.concat(df_list, ignore_index=True)
        logging.info("DataFrames combined successfully.")
        
        # save to output
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
    
    except FileNotFoundError:
        logging.error("Directory not found. Please check the path and try again.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")


################################################################
################################################################

input_dir = os.path.join("..", "random_csv_xlsx_files")
output_file = os.path.join("..", "output_combined", "test_both.csv")

# csv, excel, or both
combine_files(input_dir, output_file, file_type="both")

################################################################
################################################################