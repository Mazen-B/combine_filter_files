import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb
from tkinter import filedialog, messagebox
from combine_files import combine_files
from filter_combined_file import filter_file
from allowed_col_names import ALLOWED_COLUMNS

class FileOperationTool:
    CONDITION_TYPE_MAP = {
        "greater than": "greater_than",
        "less than": "less_than",
        "equals": "equals",
        "not equals": "not_equals"
    }

    def __init__(self, root):
        self.root = root
        self.root.title("File Operation Tool")
        self.root.geometry("700x700")
        self.style = ttkb.Style("cosmo")

        # needed vars
        self.input_directory = tk.StringVar()
        self.output_directory = tk.StringVar()
        self.output_filename = tk.StringVar()
        self.file_type = tk.StringVar(value="both")
        self.apply_filter = tk.BooleanVar(value=False)
        self.filter_conditions = []

        # build the UI
        self.create_widgets()

    def create_widgets(self):
        # create Notebook for tabs
        self.notebook = ttkb.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tabs
        self.combine_tab = ttkb.Frame(self.notebook)
        self.filter_tab = ttkb.Frame(self.notebook)
        self.notebook.add(self.combine_tab, text="Combine/Filter Multiple Files")
        self.notebook.add(self.filter_tab, text="Filter Existing File")

        # build each tab
        self.build_combine_tab()
        self.build_filter_tab()

    def build_combine_tab(self):
        # combine Tab Widgets
        ttkb.Label(self.combine_tab, text="Input Directory:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttkb.Entry(self.combine_tab, textvariable=self.input_directory, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttkb.Button(self.combine_tab, text="Browse", command=lambda: self.browse_directory(self.input_directory)).grid(row=0, column=2, padx=5, pady=5)

        ttkb.Label(self.combine_tab, text="Output Directory:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttkb.Entry(self.combine_tab, textvariable=self.output_directory, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttkb.Button(self.combine_tab, text="Browse", command=lambda: self.browse_directory(self.output_directory)).grid(row=1, column=2, padx=5, pady=5)

        ttkb.Label(self.combine_tab, text="Output Filename:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        ttkb.Entry(self.combine_tab, textvariable=self.output_filename, width=50).grid(row=2, column=1, padx=5, pady=5)

        ttkb.Label(self.combine_tab, text="File Type to Combine:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        file_type_frame = ttkb.Frame(self.combine_tab)
        file_type_frame.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        ttkb.Radiobutton(file_type_frame, text="CSV", variable=self.file_type, value="csv").pack(side=tk.LEFT)
        ttkb.Radiobutton(file_type_frame, text="Excel", variable=self.file_type, value="excel").pack(side=tk.LEFT)
        ttkb.Radiobutton(file_type_frame, text="Both", variable=self.file_type, value="both").pack(side=tk.LEFT)

        ttkb.Checkbutton(self.combine_tab, text="Apply Filter", variable=self.apply_filter, command=self.toggle_filter_section).grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)

        # filter Conditions Section
        self.filter_conditions_frame = self.create_filter_conditions_section(self.combine_tab)
        self.filter_conditions_frame.grid(row=5, column=0, columnspan=3, sticky=tk.W, padx=5, pady=5)
        self.filter_conditions_frame.grid_remove()

        # Run Button
        self.run_button = ttkb.Button(self.combine_tab, text="Run", command=self.run_combine)
        self.run_button.grid(row=6, column=0, columnspan=3, pady=20)

    def build_filter_tab(self):
        # filter Tab Widgets
        ttkb.Label(self.filter_tab, text="Input File:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttkb.Entry(self.filter_tab, textvariable=self.input_directory, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttkb.Button(self.filter_tab, text="Browse", command=lambda: self.browse_file(self.input_directory)).grid(row=0, column=2, padx=5, pady=5)

        ttkb.Label(self.filter_tab, text="Output Directory:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttkb.Entry(self.filter_tab, textvariable=self.output_directory, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttkb.Button(self.filter_tab, text="Browse", command=lambda: self.browse_directory(self.output_directory)).grid(row=1, column=2, padx=5, pady=5)

        ttkb.Label(self.filter_tab, text="Output Filename:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        ttkb.Entry(self.filter_tab, textvariable=self.output_filename, width=50).grid(row=2, column=1, padx=5, pady=5)

        ttkb.Checkbutton(self.filter_tab, text="Apply Filter", variable=self.apply_filter, command=self.toggle_filter_section).grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)

        # filter Conditions Section
        self.filter_conditions_frame_filter = self.create_filter_conditions_section(self.filter_tab)
        self.filter_conditions_frame_filter.grid(row=4, column=0, columnspan=3, sticky=tk.W, padx=5, pady=5)
        self.filter_conditions_frame_filter.grid_remove()

        # Run Button
        self.run_button_filter = ttkb.Button(self.filter_tab, text="Run", command=self.run_filter)
        self.run_button_filter.grid(row=5, column=0, columnspan=3, pady=20)

    def create_filter_conditions_section(self, parent):
        # filter Conditions Section
        filter_conditions_frame = ttkb.Labelframe(parent, text="Filter Conditions")
        condition_frame = ttkb.Frame(filter_conditions_frame)
        condition_frame.pack(pady=5)

        ttkb.Label(condition_frame, text="Column").grid(row=0, column=0, padx=5)
        ttkb.Label(condition_frame, text="Condition Type").grid(row=0, column=1, padx=5)
        ttkb.Label(condition_frame, text="Value").grid(row=0, column=2, padx=5)

        self.column_entry = ttkb.Entry(condition_frame, width=20)
        self.column_entry.grid(row=1, column=0, padx=5)

        self.condition_type_var = tk.StringVar(value="greater than")
        condition_type_menu = ttkb.Combobox(condition_frame, textvariable=self.condition_type_var, state="readonly",
                                            values=list(self.CONDITION_TYPE_MAP.keys()), width=15)
        condition_type_menu.grid(row=1, column=1, padx=5)

        self.condition_value_entry = ttkb.Entry(condition_frame, width=20)
        self.condition_value_entry.grid(row=1, column=2, padx=5)

        ttkb.Button(condition_frame, text="Add Condition", command=self.add_condition).grid(row=1, column=3, padx=5)

        # condition List
        condition_list_frame = ttkb.Frame(filter_conditions_frame)
        condition_list_frame.pack()
        ttkb.Label(condition_list_frame, text="Filter Conditions:").grid(row=0, column=0, sticky="w")
        self.condition_list = tk.Listbox(condition_list_frame, height=5, width=80)
        self.condition_list.grid(row=1, column=0, padx=5, pady=5)

        # context Menu for the Condition List
        condition_list_menu = tk.Menu(self.root, tearoff=0)
        condition_list_menu.add_command(label="Remove Condition", command=self.remove_condition)
        self.condition_list.bind("<Button-3>", lambda e: condition_list_menu.post(e.x_root, e.y_root))

        return filter_conditions_frame

    def toggle_filter_section(self):
        if self.apply_filter.get():
            if self.notebook.index(self.notebook.select()) == 0:
                self.filter_conditions_frame.grid()
            else:
                self.filter_conditions_frame_filter.grid()
        else:
            self.filter_conditions_frame.grid_remove()
            self.filter_conditions_frame_filter.grid_remove()

    def add_condition(self):
        column = self.column_entry.get()
        condition_type_display = self.condition_type_var.get()
        value = self.condition_value_entry.get()
        condition_type = self.CONDITION_TYPE_MAP.get(condition_type_display)

        if not column:
            messagebox.showwarning("Empty Column Name", "Please add a column name.")
            return

        if column not in ALLOWED_COLUMNS:
            response = messagebox.askyesno(
                "Column Not Found",
                f"'{column}' is not found in the allowed columns list. Do you want to add it anyway?"
            )
            if not response:
                return

        try:
            numeric_value = float(value) if "." in value else int(value)
        except ValueError:
            messagebox.showwarning("Invalid Input", f"The value '{value}' is not a valid number.")
            return

        self.filter_conditions.append((column, condition_type, numeric_value))
        self.condition_list.insert(tk.END, f"{column} {condition_type_display} {numeric_value}")
        self.column_entry.delete(0, tk.END)
        self.condition_value_entry.delete(0, tk.END)

    def remove_condition(self):
        selected_index = self.condition_list.curselection()
        if selected_index:
            self.condition_list.delete(selected_index)
            self.filter_conditions.pop(selected_index[0])
        else:
            messagebox.showwarning("No Selection", "Please select a condition to remove.")

    def browse_directory(self, variable):
        directory = filedialog.askdirectory()
        if directory:
            variable.set(directory)

    def browse_file(self, variable):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx")])
        if file_path:
            variable.set(file_path)

    def run_combine(self):
        if not self.input_directory.get() or not self.output_directory.get() or not self.output_filename.get():
            messagebox.showwarning("Missing Information", "Please fill out all required fields.")
            return

        combine_files(self.input_directory.get(), self.output_directory.get(), self.output_filename.get(), self.file_type.get(), self.filter_conditions)

        messagebox.showinfo("Success", "Files combined successfully!")

    def run_filter(self):
        if not self.input_directory.get() or not self.output_directory.get() or not self.output_filename.get():
            messagebox.showwarning("Missing Information", "Please fill out all required fields.")
            return

        filter_file(self.input_directory.get(), self.output_directory.get(), self.output_filename.get(), self.filter_conditions)

        messagebox.showinfo("Success", "File filtered successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileOperationTool(root)
    root.mainloop()
