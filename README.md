# File Processing and Filtering Tool

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Graphical User Interface (GUI)](#graphical-user-interface-gui)
  - [Key Features](#key-features)
  - [Usage (GUI Mode)](#usage-gui-mode)
- [Contribution](#contribution)
- [TODO List](#todo-list)

## Overview

This project provides a comprehensive toolset for combining, filtering, and managing structured data files (CSV and Excel). It includes robust functionality for handling various scenarios and a user-friendly graphical interface.

## Features

- **File Combination**:
  - Combine multiple CSV, Excel or both files into a single output file.
  - Handle differences in file structures, such as varying column names and sizes.

- **Data Filtering**:
  - Apply conditions to filter rows and columns.
  - Supported filter types:
    - Greater than (`>`)
    - Less than (`<`)
    - Equals (`=`)
    - Not equals (`!=`)
    - Columns to keep (all other columns will be removed)
    - Columns to remove

- **GUI Support**:
  - User-friendly interface for file selection and filtering.
  - Auto-completion and validation for input fields.

- **Error Handling**:
  - Validates input files, filter conditions, and column names.
  - Provides meaningful error messages for unsupported formats or invalid operations.

- **Testing**:
  - Comprehensive test suite to ensure the reliability of file combination and filtering features.

## Project Structure

```
│
├── src/
│   ├── combine_files.py               # Handles file combination
│   ├── filter_combined_file.py        # Handles data filtering
│   ├── logging_config.py              # Configures logging (used in the GUI)
│   └── gui/
│       ├── auto_complete.py           # GUI auto-completion support
│       ├── filter_handler.py          # GUI filter logic
│       ├── needed_dict.py             # Allowed columns and condition types
│       ├── select_files_gui.py        # Main GUI application
├── tests/
│   ├── test_combine_files.py          # Tests for file combination
│   ├── test_file_filtering.py         # Tests for filtering
│   ├── test_error_cases_combine.py    # Tests to verify error handling for file combination
│   ├── test_error_cases_filtering.py  # Tests to verify error handling for filtering
│   └── tests_IO/                      # Sample input/output test files
├── run.bat                            # Batch script to launch the GUI application
├── setup.bat                          # Batch script to install dependencies
├── requirements.txt                   # Python dependencies for the project
└── README.md                          # Project documentation
```

## Graphical User Interface (GUI)

The project includes a graphical user interface (GUI) for enhancing user interaction and accessibility. The GUI is designed to streamline the process of combining and filtering files.

### Key Features
- **Tabbed Interface**:
  - **Combine Multiple Files**: Allows users to combine multiple CSV and/or Excel files into a single output file with optional filtering.
  - **Filter Existing File**: Provides functionality to apply advanced filtering conditions to a single file.

- **Customizable Filtering**:
  - Add multiple filter conditions using an intuitive interface.
  - Supports condition types such as "greater than," "less than," "equals," "not equals," and column-based operations like "columns to keep" or "columns to remove."

- **User-Friendly Widgets**:
  - File and directory selection dialogs for easy navigation.
  - Auto-complete functionality for selecting columns.
  - Drop-down menus for selecting condition types.

- **Real-Time Feedback**:
  - Displays warnings or errors if required fields are missing or conditions are invalid.
  - Provides success messages upon successful operations.

- **Note on Auto-Complete Functionality**:
  - The auto-complete feature in the GUI uses a predefined list of column names specified in the `needed_dict.py` file located inside `src/gui`. This list (`ALLOWED_COLUMNS`) is used to suggest column names when adding filter conditions.
  - Feel free to modify this dictionary with column names that you commonly use in your datasets. Customizing this list will ensure that the auto-complete suggestions match your specific requirements.

### Usage (GUI Mode)
---
1. Using Command-Line Mode
  - run **`pip install -r requirements.txt`** once to set up all necessary dependencies.
  - run **`python src/gui/select_files_gui.py`** to run the gui
2. Using batch scripts (Windows):
- Run **`setup_python.bat`** once to set up all necessary dependencies.
- From then on, simply run **`run.bat`** wto run the gui.