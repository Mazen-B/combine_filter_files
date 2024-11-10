import os
import tkinter as tk
from combine_files import combine_files
from filter_combined_file import filter_file
from allowed_col_names import ALLOWED_COLUMNS
from tkinter import filedialog, messagebox, ttk

# main Tkinter window
root = tk.Tk()
root.title("File Combiner and Filter")
root.geometry("650x650")
root.option_add("*Font", "Helvetica 10")

# apply a theme
style = ttk.Style(root)
style.theme_use("clam")
style.configure("TLabel", padding=5)
style.configure("TButton", font=("Helvetica", 10, "bold"))

# global variables to hold paths and filtering conditions
input_directory = tk.StringVar()
output_directory = tk.StringVar()
output_filename = tk.StringVar()
file_type = tk.StringVar(value="both")
apply_filter = tk.BooleanVar(value=False)
filter_conditions = []

def browse_input_directory():
    directory = filedialog.askdirectory()
    if directory:
        input_directory.set(directory)

def browse_output_directory():
    directory = filedialog.askdirectory()
    if directory:
        output_directory.set(directory)

def toggle_filter_section():
    if apply_filter.get():
        condition_frame.grid(row=1, column=0, columnspan=3, pady=10, padx=5, sticky="w")
        condition_list_frame.grid(row=2, column=0, columnspan=3, pady=10, padx=5, sticky="w")
    else:
        condition_frame.grid_forget()
        condition_list_frame.grid_forget()

CONDITION_TYPE_MAP = {
    "greater than": "greater_than",
    "less than": "less_than",
    "equals": "equals",
    "not equals": "not_equals"
}

def add_condition():
    column = column_entry.get()
    condition_type_display = condition_type_var.get()  # get display name
    value = condition_value_entry.get()

    # get internal condition type from the map
    condition_type = CONDITION_TYPE_MAP.get(condition_type_display)

    # check if column name is empty
    if not column:
        messagebox.showwarning("Empty Column Name", "Please add a column name.")
        return

    # check if column exists in allowed columns
    if column not in ALLOWED_COLUMNS:
        # ask the user to ignore or cancel
        response = messagebox.askyesno(
            "Column Not Found", 
            f"'{column}' is not found in the 'allowed columns names' list. Do you want to ignore this error and add it anyway?"
        )
        if not response:
            return

    # check if value contains a comma and prompt the user to use a period
    if "," in value:
        messagebox.showwarning("Invalid Number Format", "Please use a period (.) instead of a comma (,) for decimal values.")
        return

    # allow boolean values for equals and not_equals conditions
    if condition_type in ["equals", "not_equals"] and value.lower() in ["true", "false"]:
        numeric_value = value.lower() == "true"  # converts "true" to True and "false" to False
    else:
        # check if value can be converted to a numeric type (int or float)
        try:
            numeric_value = float(value) if "." in value else int(value)
        except ValueError:
            messagebox.showwarning("Invalid Input", f"The value '{value}' is not a valid number or boolean for the selected condition type.")
            return

    if column and condition_type:
        filter_conditions.append((column, condition_type, numeric_value))
        condition_list.insert(tk.END, f"{column} {condition_type_display} {numeric_value}")
        column_entry.delete(0, tk.END)
        condition_value_entry.delete(0, tk.END)

def remove_condition():
    selected_index = condition_list.curselection()
    if selected_index:
        condition_list.delete(selected_index)
        filter_conditions.pop(selected_index[0])
    else:
        messagebox.showwarning("No Selection", "Please select a condition to remove.")

def run_process():
    if not os.path.isdir(input_directory.get()):
        messagebox.showerror("Error", "Input directory does not exist.")
        return
    if not os.path.isdir(output_directory.get()):
        messagebox.showerror("Error", "Output directory does not exist.")
        return
    if not output_filename.get():
        messagebox.showerror("Error", "Output filename is not specified.")
        return
    
    output_file_path = os.path.join(output_directory.get(), output_filename.get())
    output_ext = os.path.splitext(output_file_path)[1]

    if file_type.get() == "csv" and output_ext != ".csv":
        messagebox.showerror("Error", "Output file extension does not match selected file type (CSV).")
        return
    elif file_type.get() == "excel" and output_ext != ".xlsx":
        messagebox.showerror("Error", "Output file extension does not match selected file type (Excel).")
        return

    try:
        combine_files(input_directory.get(), output_file_path, file_type.get())
        
        if apply_filter.get():
            conditions = {col: {"type": cond_type, "value": float(val) if isinstance(val, str) and val.isdigit() else val}
                          for col, cond_type, val in filter_conditions}
            filter_file(output_file_path, output_file_path, conditions)
            messagebox.showinfo("Success", "Files combined and filtered successfully.")
            root.destroy()
        else:
            messagebox.showinfo("Success", "Files combined successfully.")
            root.destroy()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# UI Elements for "Combine Files" Section
combine_frame = ttk.LabelFrame(root, text="Combine Files")
combine_frame.pack(pady=10, fill=tk.X, padx=15)

ttk.Label(combine_frame, text="Input Directory:").grid(row=0, column=0, sticky=tk.W, padx=5)
ttk.Entry(combine_frame, textvariable=input_directory, width=45).grid(row=0, column=1, padx=5)
ttk.Button(combine_frame, text="Browse", command=browse_input_directory).grid(row=0, column=2, padx=5)

ttk.Label(combine_frame, text="Output Directory:").grid(row=1, column=0, sticky=tk.W, padx=5)
ttk.Entry(combine_frame, textvariable=output_directory, width=45).grid(row=1, column=1, padx=5)
ttk.Button(combine_frame, text="Browse", command=browse_output_directory).grid(row=1, column=2, padx=5)

ttk.Label(combine_frame, text="Output Filename:").grid(row=2, column=0, sticky=tk.W, padx=5)
ttk.Entry(combine_frame, textvariable=output_filename, width=45).grid(row=2, column=1, padx=5)

# Label for file type selection
ttk.Label(combine_frame, text="File Type to Combine:").grid(row=3, column=0, sticky=tk.W, padx=5)

file_type_frame = tk.Frame(combine_frame)
file_type_frame.grid(row=3, column=1, sticky=tk.W, padx=5)

file_type_csv = tk.Radiobutton(file_type_frame, text="CSV", variable=file_type, value="csv")
file_type_csv.pack(side=tk.LEFT, padx=(0, 10))
file_type_excel = tk.Radiobutton(file_type_frame, text="Excel", variable=file_type, value="excel")
file_type_excel.pack(side=tk.LEFT, padx=(0, 10))
file_type_both = tk.Radiobutton(file_type_frame, text="Both", variable=file_type, value="both")
file_type_both.pack(side=tk.LEFT)

file_type_frame.configure(background="#f0f0f0")

# UI Elements for "Filter the Combined File" Section
filter_frame = ttk.LabelFrame(root, text="Filter the Combined File")
filter_frame.pack(pady=10, fill=tk.X, padx=15)

ttk.Checkbutton(filter_frame, text="Apply Filter", variable=apply_filter, command=toggle_filter_section).grid(row=0, column=0, sticky=tk.W, padx=5)

# frame for adding filter conditions
condition_frame = tk.Frame(filter_frame)
tk.Label(condition_frame, text="Column").grid(row=0, column=0, padx=5)
tk.Label(condition_frame, text="Condition Type").grid(row=0, column=1, padx=5)
tk.Label(condition_frame, text="Value").grid(row=0, column=2, padx=5)

column_entry = ttk.Entry(condition_frame, width=20)
column_entry.grid(row=1, column=0, padx=5)

condition_type_var = tk.StringVar(value="greater than")
condition_type_menu = ttk.Combobox(condition_frame, textvariable=condition_type_var, state="readonly",
                                   values=list(CONDITION_TYPE_MAP.keys()), width=15)
condition_type_menu.grid(row=1, column=1, padx=5)

condition_value_entry = ttk.Entry(condition_frame, width=20)
condition_value_entry.grid(row=1, column=2, padx=5)

ttk.Button(condition_frame, text="Add Condition", command=add_condition).grid(row=1, column=3, padx=5)

# listbox to display conditions
condition_list_frame = tk.Frame(filter_frame)
tk.Label(condition_list_frame, text="Filter Conditions:").grid(row=0, column=0, sticky="w")
condition_list = tk.Listbox(condition_list_frame, height=5, width=80)
condition_list.grid(row=1, column=0, padx=5, pady=5)
condition_list.bind("<Button-3>", lambda e: condition_list_menu.post(e.x_root, e.y_root))

condition_list_menu = tk.Menu(root, tearoff=0)
condition_list_menu.add_command(label="Remove Condition", command=remove_condition)

toggle_filter_section()

# run button
run_button = ttk.Button(root, text="Run", command=run_process, style="Accent.TButton")
style.configure("Accent.TButton", font=("Helvetica", 12, "bold"), foreground="white", background="#1f77b4")
run_button.pack(pady=20)

root.mainloop()
