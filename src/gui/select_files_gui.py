import os
import sys
import tkinter as tk
import ttkbootstrap as ttkb
from filter_handler import FilterHandler
from tkinter import filedialog, messagebox
from auto_complete import AutocompleteEntry
from needed_dict import ALLOWED_COLUMNS, CONDITION_TYPE_MAP

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from logging_config import clear_log_buffer, get_log_messages
from filter_combined_file import filter_file
from combine_files import combine_files

class FileOperationTool:
    def __init__(self, root):
        self.root = root
        self.root.title("File Operation Tool")
        self.root.geometry("750x600")
        self.style = ttkb.Style("cosmo")
        self.condition_type_var_combine = tk.StringVar(value="greater than")
        self.condition_type_var_filter = tk.StringVar(value="greater than")
        self.filter_handler = FilterHandler(ALLOWED_COLUMNS, CONDITION_TYPE_MAP)

        self.create_widgets()

    def create_widgets(self):
        """
      This method creates the main UI components of the application, including tabs for combining files and filtering files.
      """
        self.notebook = ttkb.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tabs
        self.combine_tab = ttkb.Frame(self.notebook)
        self.filter_tab = ttkb.Frame(self.notebook)
        self.notebook.add(self.combine_tab, text="Combine Multiple Files")
        self.notebook.add(self.filter_tab, text="Filter Existing File")

        self.build_combine_tab()
        self.build_one_file_tab()

    ######################################
    # "Combine Multiple Files" tab's logic
    ######################################
    def build_combine_tab(self):
        """
      This method builds the "Combine Multiple Files" tab, allowing users to specify input/output directories, output filename, file types, and optional filter conditions.
      """
        self.combine_input_directory = tk.StringVar()
        self.combine_output_directory = tk.StringVar()
        self.combine_output_filename = tk.StringVar()
        self.combine_file_type = tk.StringVar(value="both")
        self.combine_apply_filter = tk.BooleanVar(value=False)
        self.combine_filter_conditions = []

        ttkb.Label(self.combine_tab, text="Input Directory:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttkb.Entry(self.combine_tab, textvariable=self.combine_input_directory, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttkb.Button(self.combine_tab, text="Browse", command=lambda: self.browse_directory(self.combine_input_directory)).grid(row=0, column=2, padx=5, pady=5)

        ttkb.Label(self.combine_tab, text="Output Directory:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttkb.Entry(self.combine_tab, textvariable=self.combine_output_directory, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttkb.Button(self.combine_tab, text="Browse", command=lambda: self.browse_directory(self.combine_output_directory)).grid(row=1, column=2, padx=5, pady=5)

        ttkb.Label(self.combine_tab, text="Output Filename:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        ttkb.Entry(self.combine_tab, textvariable=self.combine_output_filename, width=50).grid(row=2, column=1, padx=5, pady=5)

        ttkb.Label(self.combine_tab, text="File Type to Combine:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        file_type_frame = ttkb.Frame(self.combine_tab)
        file_type_frame.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        ttkb.Radiobutton(file_type_frame, text="CSV", variable=self.combine_file_type, value="csv").pack(side=tk.LEFT, padx=10)
        ttkb.Radiobutton(file_type_frame, text="Excel", variable=self.combine_file_type, value="excel").pack(side=tk.LEFT, padx=10)
        ttkb.Radiobutton(file_type_frame, text="Both", variable=self.combine_file_type, value="both").pack(side=tk.LEFT, padx=10)

        ttkb.Checkbutton(
            self.combine_tab, text="Apply Filter",
            variable=self.combine_apply_filter,
            command=lambda: self.filter_handler.toggle_filter_section(self.combine_apply_filter, self.filter_conditions_frame_combine)
        ).grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)

        self.filter_conditions_frame_combine = self.create_filter_conditions_section(self.combine_tab, "combine")
        self.filter_conditions_frame_combine.grid(row=5, column=0, columnspan=3, sticky=tk.W, padx=5, pady=5)
        self.filter_conditions_frame_combine.grid_remove()

        ttkb.Button(self.combine_tab, text="Run", command=self.run_combine).grid(row=6, column=0, columnspan=3, pady=20)

    def run_combine(self):
        """
      This method actually calls the combine_files function (if needed the filter_file function)
      """
        if not self.combine_input_directory.get() or not self.combine_output_directory.get() or not self.combine_output_filename.get():
            messagebox.showwarning("Missing Information", "Please fill out all required fields.")
            return

        clear_log_buffer()

        output_file = os.path.join(self.combine_output_directory.get(), self.combine_output_filename.get())
        try:
            combine_files(
                input_dir=self.combine_input_directory.get(),
                output_file=output_file,
                file_type=self.combine_file_type.get()
            )

            if self.combine_apply_filter.get():
                conditions = self.convert_conditions_to_dict(self.combine_filter_conditions)
                filter_file(output_file, output_file, conditions)

            # check for logged warnings or errors
            log_messages = get_log_messages()
            if "ERROR" in log_messages or "WARNING" in log_messages:
                messagebox.showwarning("Warning", log_messages)
            else:
                messagebox.showinfo("Success", "Files combined successfully!")
                self.root.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            log_messages = get_log_messages()
            print(log_messages)

    ####################################
    # "Filter Existing File" tab's logic
    ####################################
    def build_one_file_tab(self):
        """
      This method builds the "Filter Existing File" tab, allowing users to specify input/output directories, output filename, and optional filter conditions.
      """
        self.filter_input_file = tk.StringVar()
        self.filter_output_directory = tk.StringVar()
        self.filter_output_filename = tk.StringVar()
        self.filter_apply_filter = tk.BooleanVar(value=False)
        self.filter_filter_conditions = []

        ttkb.Label(self.filter_tab, text="Input File:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttkb.Entry(self.filter_tab, textvariable=self.filter_input_file, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttkb.Button(self.filter_tab, text="Browse", command=lambda: self.browse_file(self.filter_input_file)).grid(row=0, column=2, padx=5, pady=5)

        ttkb.Label(self.filter_tab, text="Output Directory:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttkb.Entry(self.filter_tab, textvariable=self.filter_output_directory, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttkb.Button(self.filter_tab, text="Browse", command=lambda: self.browse_directory(self.filter_output_directory)).grid(row=1, column=2, padx=5, pady=5)

        ttkb.Label(self.filter_tab, text="Output Filename:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        ttkb.Entry(self.filter_tab, textvariable=self.filter_output_filename, width=50).grid(row=2, column=1, padx=5, pady=5)

        ttkb.Checkbutton(
            self.filter_tab, text="Apply Filter",
            variable=self.filter_apply_filter,
            command=lambda: self.filter_handler.toggle_filter_section(self.filter_apply_filter, self.filter_conditions_frame_filter)
        ).grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)

        self.filter_conditions_frame_filter = self.create_filter_conditions_section(self.filter_tab, "filter")
        self.filter_conditions_frame_filter.grid(row=4, column=0, columnspan=3, sticky=tk.W, padx=5, pady=5)
        self.filter_conditions_frame_filter.grid_remove()

        ttkb.Button(self.filter_tab, text="Run", command=self.run_filter).grid(row=5, column=0, columnspan=3, pady=20)

    def run_filter(self):
        """
      This method creates a filter conditions section in the specified tab.
      """
        if not self.filter_input_file.get() or not self.filter_output_directory.get() or not self.filter_output_filename.get():
            messagebox.showwarning("Missing Information", "Please fill out all required fields.")
            return

        clear_log_buffer()

        output_file = os.path.join(self.filter_output_directory.get(), self.filter_output_filename.get())
        try:
            conditions = self.convert_conditions_to_dict(self.filter_filter_conditions) if self.filter_apply_filter.get() else {}
            filter_file(self.filter_input_file.get(), output_file, conditions)

            log_messages = get_log_messages()
            if "ERROR" in log_messages or "WARNING" in log_messages:
                messagebox.showwarning("Warning", log_messages)
            else:
                if messagebox.showinfo("Success", "File filtered successfully!") == "ok":
                    self.root.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

            log_messages = get_log_messages()
            print(log_messages)

    ###########################
    # condition section's logic
    ###########################
    def create_filter_conditions_section(self, parent, tab_type):
        """
      This method creates a filter conditions section in the specified tab.
      """
        filter_conditions_frame = ttkb.Labelframe(parent, text="Filter Conditions")
        condition_frame = ttkb.Frame(filter_conditions_frame)
        condition_frame.pack(pady=5)

        ttkb.Label(condition_frame, text="Column(s):").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        autocomplete_list = ALLOWED_COLUMNS
        column_entry = AutocompleteEntry(autocomplete_list, condition_frame, width=25, root=self.root)
        column_entry.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        ttkb.Label(condition_frame, text="Condition Type:").grid(row=0, column=1, padx=5, pady=2, sticky="w")
        condition_type_var = self.condition_type_var_filter if tab_type == "filter" else self.condition_type_var_combine
        condition_type_menu = ttkb.Combobox(
            condition_frame,
            textvariable=condition_type_var,
            state="readonly",
            values=list(CONDITION_TYPE_MAP.keys()),
            width=20
        )
        condition_type_menu.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        condition_type_menu.bind("<<ComboboxSelected>>", lambda event, tab=tab_type: self.filter_handler.on_condition_type_change(
            condition_type_var, value_entry, value_label
        ))

        value_label = ttkb.Label(condition_frame, text="Value:")
        value_label.grid(row=0, column=2, padx=5, pady=2, sticky="w")
        value_entry = ttkb.Entry(condition_frame, width=15)
        value_entry.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        if tab_type == "filter":
            self.columns_entry_filter = column_entry
            self.condition_type_menu_filter = condition_type_menu
            self.condition_value_entry_filter = value_entry
            self.condition_value_label_filter = value_label
        else:
            self.columns_entry_combine = column_entry
            self.condition_type_menu_combine = condition_type_menu
            self.condition_value_entry_combine = value_entry
            self.condition_value_label_combine = value_label

        ttkb.Button(
            condition_frame, text="Add Condition",
            command=lambda: self.add_condition(tab_type)
        ).grid(row=1, column=3, padx=5, sticky="w")

        condition_list_frame = ttkb.Frame(filter_conditions_frame)
        condition_list_frame.pack(pady=10)
        ttkb.Label(condition_list_frame, text="Added Conditions:").grid(row=0, column=0, sticky="w")
        condition_list = tk.Listbox(condition_list_frame, height=5, width=70)
        condition_list.grid(row=1, column=0, padx=5, pady=5)

        if tab_type == "filter":
            self.condition_list_filter = condition_list
            self.remove_button_filter = ttkb.Button(
                condition_list_frame, text="Remove Selected Condition",
                command=lambda: self.remove_condition(tab_type)
            )
            self.remove_button_filter.grid(row=2, column=0, padx=5, pady=5, sticky="w")
            self.remove_button_filter["state"] = "disabled"
        else:
            self.condition_list_combine = condition_list
            self.remove_button_combine = ttkb.Button(
                condition_list_frame, text="Remove Selected Condition",
                command=lambda: self.remove_condition(tab_type)
            )
            self.remove_button_combine.grid(row=2, column=0, padx=5, pady=5, sticky="w")
            self.remove_button_combine["state"] = "disabled"

        return filter_conditions_frame
    
    def convert_conditions_to_dict(self, condition_list):
        """
      This method conversts the conditions added by the user to a dict.
      """
        condition_dict = {}
        for item in condition_list:
            if isinstance(item[1], list):
                condition_dict[item[0]] = item[1]
            else:
                column, condition_type, value = item
                condition_dict[column] = {"type": condition_type, "value": value}
        return condition_dict

    def add_condition(self, tab_type):
        """
      This method adds the condition in the "Added Conditions" box.
      """
        if tab_type == "combine":
            error = self.filter_handler.add_condition(
                self.columns_entry_combine,
                self.condition_value_entry_combine,
                self.condition_type_var_combine,
                self.combine_filter_conditions,
                self.condition_list_combine
            )
            # Enable or disable the remove button
            self.remove_button_combine["state"] = "normal" if self.combine_filter_conditions else "disabled"
        else:
            error = self.filter_handler.add_condition(
                self.columns_entry_filter,
                self.condition_value_entry_filter,
                self.condition_type_var_filter,
                self.filter_filter_conditions,
                self.condition_list_filter
            )
            # Enable or disable the remove button
            self.remove_button_filter["state"] = "normal" if self.filter_filter_conditions else "disabled"
        if error:
            messagebox.showwarning("Error", error)

    def remove_condition(self, tab_type):
        """
      This method has the remov the condition in the "Added Conditions" box.
      """
        if tab_type == "combine":
            error = self.filter_handler.remove_condition(self.condition_list_combine, self.combine_filter_conditions)
            self.remove_button_combine["state"] = "normal" if self.combine_filter_conditions else "disabled"
        else:
            error = self.filter_handler.remove_condition(self.condition_list_filter, self.filter_filter_conditions)
            self.remove_button_filter["state"] = "normal" if self.filter_filter_conditions else "disabled"
        if error:
            messagebox.showwarning("Error", error)

    ###########################
    # general utilies functions
    ###########################
    def browse_directory(self, variable):
        directory = filedialog.askdirectory()
        if directory:
            variable.set(directory)

    def browse_file(self, variable):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx")])
        if file_path:
            variable.set(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileOperationTool(root)
    root.mainloop()
