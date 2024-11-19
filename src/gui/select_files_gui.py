import os
import sys
import tkinter as tk
import ttkbootstrap as ttkb
from tkinter import filedialog, messagebox
from auto_complete import AutocompleteEntry
from needed_dict import ALLOWED_COLUMNS, CONDITION_TYPE_MAP

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from combine_files import combine_files
from filter_combined_file import filter_file

class FileOperationTool:
    def __init__(self, root):
        self.root = root
        self.root.title("File Operation Tool")
        self.root.geometry("750x550")
        self.style = ttkb.Style("cosmo")
        self.condition_type_var_combine = tk.StringVar(value="greater than")
        self.condition_type_var_filter = tk.StringVar(value="greater than")
        # build the UI
        self.create_widgets()

    def create_widgets(self):
        # create Notebook for tabs
        self.notebook = ttkb.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tabs
        self.combine_tab = ttkb.Frame(self.notebook)
        self.filter_tab = ttkb.Frame(self.notebook)
        self.notebook.add(self.combine_tab, text="Combine Multiple Files")
        self.notebook.add(self.filter_tab, text="Filter Existing File")

        # build each tab
        self.build_combine_tab()
        self.build_filter_tab()

    def build_combine_tab(self):
        # vars specific to the combine tab
        self.combine_input_directory = tk.StringVar()
        self.combine_output_directory = tk.StringVar()
        self.combine_output_filename = tk.StringVar()
        self.combine_file_type = tk.StringVar(value="both")
        self.combine_apply_filter = tk.BooleanVar(value=False)
        self.combine_filter_conditions = []

        # combine Tab Widgets
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

        ttkb.Checkbutton(self.combine_tab, text="Apply Filter", variable=self.combine_apply_filter, command=self.toggle_filter_section_combine).grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)

        # filter Conditions Section
        self.filter_conditions_frame_combine = self.create_filter_conditions_section(self.combine_tab, "combine")
        self.filter_conditions_frame_combine.grid(row=5, column=0, columnspan=3, sticky=tk.W, padx=5, pady=5)
        self.filter_conditions_frame_combine.grid_remove()

        # Run Button
        self.run_button = ttkb.Button(self.combine_tab, text="Run", command=self.run_combine)
        self.run_button.grid(row=6, column=0, columnspan=3, pady=20)

    def build_filter_tab(self):
        # vars specific to the filter tab
        self.filter_input_file = tk.StringVar()
        self.filter_output_directory = tk.StringVar()
        self.filter_output_filename = tk.StringVar()
        self.filter_apply_filter = tk.BooleanVar(value=False)
        self.filter_filter_conditions = []

        # filter Tab Widgets
        ttkb.Label(self.filter_tab, text="Input File:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttkb.Entry(self.filter_tab, textvariable=self.filter_input_file, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttkb.Button(self.filter_tab, text="Browse", command=lambda: self.browse_file(self.filter_input_file)).grid(row=0, column=2, padx=5, pady=5)

        ttkb.Label(self.filter_tab, text="Output Directory:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttkb.Entry(self.filter_tab, textvariable=self.filter_output_directory, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttkb.Button(self.filter_tab, text="Browse", command=lambda: self.browse_directory(self.filter_output_directory)).grid(row=1, column=2, padx=5, pady=5)

        ttkb.Label(self.filter_tab, text="Output Filename:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        ttkb.Entry(self.filter_tab, textvariable=self.filter_output_filename, width=50).grid(row=2, column=1, padx=5, pady=5)

        ttkb.Checkbutton(self.filter_tab, text="Apply Filter", variable=self.filter_apply_filter, command=self.toggle_filter_section_filter).grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)

        # filter Conditions Section
        self.filter_conditions_frame_filter = self.create_filter_conditions_section(self.filter_tab, "filter")
        self.filter_conditions_frame_filter.grid(row=4, column=0, columnspan=3, sticky=tk.W, padx=5, pady=5)
        self.filter_conditions_frame_filter.grid_remove()

        # Run Button
        self.run_button_filter = ttkb.Button(self.filter_tab, text="Run", command=self.run_filter)
        self.run_button_filter.grid(row=5, column=0, columnspan=3, pady=20)

    def create_filter_conditions_section(self, parent, tab_type):
        # Filter Conditions Section
        filter_conditions_frame = ttkb.Labelframe(parent, text="Filter Conditions")
        condition_frame = ttkb.Frame(filter_conditions_frame)
        condition_frame.pack(pady=5)

        # Column(s) Entry with Autocomplete
        ttkb.Label(condition_frame, text="Column(s)").grid(row=0, column=0, padx=5)
        autocomplete_list = ALLOWED_COLUMNS  # Dynamic or static list of allowed columns
        column_entry = AutocompleteEntry(autocomplete_list, condition_frame, width=40)
        column_entry.grid(row=1, column=0, columnspan=2, padx=5)
        
        # Save reference
        if tab_type == "filter":
            self.columns_entry_filter = column_entry
        else:
            self.columns_entry_combine = column_entry

        # Condition Type Combobox
        ttkb.Label(condition_frame, text="Condition Type").grid(row=0, column=2, padx=5)
        condition_type_menu = ttkb.Combobox(
            condition_frame,
            textvariable=(self.condition_type_var_filter if tab_type == "filter" else self.condition_type_var_combine),
            state="readonly",
            values=list(CONDITION_TYPE_MAP.keys()),
            width=15
        )
        condition_type_menu.grid(row=1, column=2, padx=5)

        # Value Entry
        ttkb.Label(condition_frame, text="Value").grid(row=0, column=3, padx=5)
        value_entry = ttkb.Entry(condition_frame, width=15)
        value_entry.grid(row=1, column=3, padx=5)
        
        # Save reference for conditional usage
        if tab_type == "filter":
            self.condition_value_entry_filter = value_entry
        else:
            self.condition_value_entry_combine = value_entry

        # Add Condition Button
        add_button_command = self.add_condition_filter if tab_type == "filter" else self.add_condition_combine
        ttkb.Button(condition_frame, text="Add Condition", command=add_button_command).grid(row=1, column=4, padx=5)

        # Condition Listbox for added conditions
        condition_list_frame = ttkb.Frame(filter_conditions_frame)
        condition_list_frame.pack(pady=10)
        ttkb.Label(condition_list_frame, text="Added Conditions:").grid(row=0, column=0, sticky="w")
        condition_list = tk.Listbox(condition_list_frame, height=5, width=70)
        condition_list.grid(row=1, column=0, padx=5, pady=5)

        # Save reference
        if tab_type == "filter":
            self.condition_list_filter = condition_list
        else:
            self.condition_list_combine = condition_list

        return filter_conditions_frame

    ###########################
    # Functions for Combine Tab
    ###########################
    def toggle_filter_section_combine(self):
        if self.combine_apply_filter.get():
            self.filter_conditions_frame_combine.grid()
        else:
            self.filter_conditions_frame_combine.grid_remove()

    def add_condition_combine(self):
        condition_type_display = self.condition_type_var_combine.get()
        condition_type = CONDITION_TYPE_MAP.get(condition_type_display)

        # Get columns from the Entry field
        columns_text = self.columns_entry_combine.get()
        if not columns_text:
            messagebox.showwarning("No Columns Entered", "Please enter at least one column.")
            return
        columns = [col.strip() for col in columns_text.split(",") if col.strip()]

        if condition_type in ["columns_to_keep", "columns_to_remove"]:
            self.combine_filter_conditions.append((condition_type, columns))
            self.condition_list_combine.insert(tk.END, f"{condition_type_display}: {", ".join(columns)}")
            # Clear the entry
            self.columns_entry_combine.delete(0, tk.END)
        else:
            value = self.condition_value_entry_combine.get()
            if not value:
                messagebox.showwarning("Empty Value", "Please enter a value.")
                return

            try:
                numeric_value = float(value) if "." in value else int(value)
            except ValueError:
                messagebox.showwarning("Invalid Input", f"The value '{value}' is not a valid number.")
                return

            for column in columns:
                self.combine_filter_conditions.append((column, condition_type, numeric_value))
                self.condition_list_combine.insert(tk.END, f"{column} {condition_type_display} {numeric_value}")
            # Clear the entries
            self.columns_entry_combine.delete(0, tk.END)
            self.condition_value_entry_combine.delete(0, tk.END)

    def remove_condition_combine(self):
        selected_index = self.condition_list_combine.curselection()
        if selected_index:
            self.condition_list_combine.delete(selected_index)
            self.combine_filter_conditions.pop(selected_index[0])
        else:
            messagebox.showwarning("No Selection", "Please select a condition to remove.")

    def run_combine(self):
        if not self.combine_input_directory.get() or not self.combine_output_directory.get() or not self.combine_output_filename.get():
            messagebox.showwarning("Missing Information", "Please fill out all required fields.")
            return

        output_file = os.path.join(self.combine_output_directory.get(), self.combine_output_filename.get())
        combine_files(
            input_dir=self.combine_input_directory.get(),
            output_file=output_file,
            file_type=self.combine_file_type.get(),
            conditions=self.convert_conditions_to_dict(self.combine_filter_conditions) if self.combine_apply_filter.get() else None
        )

        messagebox.showinfo("Success", "Files combined successfully!")

    ###########################
    # Functions for Filter Tab
    ###########################
    def toggle_filter_section_filter(self):
        if self.filter_apply_filter.get():
            self.filter_conditions_frame_filter.grid()
        else:
            self.filter_conditions_frame_filter.grid_remove()

    def add_condition_filter(self):
        condition_type_display = self.condition_type_var_filter.get()
        condition_type = CONDITION_TYPE_MAP.get(condition_type_display)

        # Get columns from the Entry field
        columns_text = self.columns_entry_filter.get()
        if not columns_text:
            messagebox.showwarning("No Columns Entered", "Please enter at least one column.")
            return
        columns = [col.strip() for col in columns_text.split(",") if col.strip()]

        if condition_type in ["columns_to_keep", "columns_to_remove"]:
            self.filter_filter_conditions.append((condition_type, columns))
            self.condition_list_filter.insert(tk.END, f"{condition_type_display}: {", ".join(columns)}")
            # Clear the entry
            self.columns_entry_filter.delete(0, tk.END)
        else:
            value = self.condition_value_entry_filter.get()
            if not value:
                messagebox.showwarning("Empty Value", "Please enter a value.")
                return

            try:
                numeric_value = float(value) if "." in value else int(value)
            except ValueError:
                messagebox.showwarning("Invalid Input", f"The value '{value}' is not a valid number.")
                return

            for column in columns:
                self.filter_filter_conditions.append((column, condition_type, numeric_value))
                self.condition_list_filter.insert(tk.END, f"{column} {condition_type_display} {numeric_value}")
            # Clear the entries
            self.columns_entry_filter.delete(0, tk.END)
            self.condition_value_entry_filter.delete(0, tk.END)

    def remove_condition_filter(self):
        selected_index = self.condition_list_filter.curselection()
        if selected_index:
            self.condition_list_filter.delete(selected_index)
            self.filter_filter_conditions.pop(selected_index[0])
        else:
            messagebox.showwarning("No Selection", "Please select a condition to remove.")

    def run_filter(self):
        if not self.filter_input_file.get() or not self.filter_output_directory.get() or not self.filter_output_filename.get():
            messagebox.showwarning("Missing Information", "Please fill out all required fields.")
            return

        output_file = os.path.join(self.filter_output_directory.get(), self.filter_output_filename.get())
        filter_file(
            file_path=self.filter_input_file.get(),
            output_file=output_file,
            conditions=self.convert_conditions_to_dict(self.filter_filter_conditions) if self.filter_apply_filter.get() else None
        )

        messagebox.showinfo("Success", "File filtered successfully!")

    # Utility functions
    def browse_directory(self, variable):
        directory = filedialog.askdirectory()
        if directory:
            variable.set(directory)

    def browse_file(self, variable):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx")])
        if file_path:
            variable.set(file_path)

    def convert_conditions_to_dict(self, condition_list):
        condition_dict = {}
        for item in condition_list:
            if isinstance(item[1], list):
                # This is a "columns_to_keep" or "columns_to_remove" condition
                condition_type = item[0]
                columns = item[1]
                condition_dict[condition_type] = columns
            else:
                # Existing conditions
                column, condition_type, value = item
                if column not in condition_dict:
                    condition_dict[column] = []
                condition_dict[column].append({"type": condition_type, "value": value})
        return condition_dict

    def on_condition_type_change(self, event, tab_type):
        selected_condition = event.widget.get()
        if tab_type == "filter":
            if selected_condition in ["Columns to Keep", "Columns to Remove"]:
                # Hide Value label and entry
                self.value_label_filter.grid_remove()
                self.condition_value_entry_filter.grid_remove()
            else:
                # Show Value label and entry
                self.value_label_filter.grid()
                self.condition_value_entry_filter.grid()
        elif tab_type == "combine":
            if selected_condition in ["Columns to Keep", "Columns to Remove"]:
                # Hide Value label and entry
                self.value_label_combine.grid_remove()
                self.condition_value_entry_combine.grid_remove()
            else:
                # Show Value label and entry
                self.value_label_combine.grid()
                self.condition_value_entry_combine.grid()

if __name__ == "__main__":
    root = tk.Tk()
    app = FileOperationTool(root)
    root.mainloop()
