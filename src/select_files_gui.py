import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from combine_files import combine_files
from filter_output_file import filter_file

# main Tkinter window
root = tk.Tk()
root.title("File Combiner and Filter")
root.geometry("600x650")
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

def add_condition():
    column = column_entry.get()
    condition_type = condition_type_var.get()
    value = condition_value_entry.get()
    if column and condition_type and value:
        filter_conditions.append((column, condition_type, value))
        condition_list.insert(tk.END, f"{column} {condition_type} {value}")
        column_entry.delete(0, tk.END)
        condition_value_entry.delete(0, tk.END)

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
        messagebox.showinfo("Success", "Files combined successfully.")

        if apply_filter.get():
            conditions = {col: {"type": cond_type, "value": float(val) if val.isdigit() else val}
                          for col, cond_type, val in filter_conditions}
            filter_file(output_file_path, output_file_path, conditions)
            messagebox.showinfo("Success", "Files filtered successfully.")

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

ttk.Label(combine_frame, text="File Type:").grid(row=3, column=0, sticky=tk.W, padx=5)
file_type_option_menu = ttk.Combobox(combine_frame, textvariable=file_type, state="readonly",
                                     values=["csv", "excel", "both"], width=10)
file_type_option_menu.grid(row=3, column=1, padx=5)

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

condition_type_var = tk.StringVar(value="greater_than")
condition_type_menu = ttk.Combobox(condition_frame, textvariable=condition_type_var, state="readonly",
                                   values=["greater_than", "less_than", "equals", "not_equals"], width=15)
condition_type_menu.grid(row=1, column=1, padx=5)

condition_value_entry = ttk.Entry(condition_frame, width=20)
condition_value_entry.grid(row=1, column=2, padx=5)

ttk.Button(condition_frame, text="Add Condition", command=add_condition).grid(row=1, column=3, padx=5)

condition_type_var = tk.StringVar(value="greater_than")
condition_type_menu = ttk.Combobox(condition_frame, textvariable=condition_type_var, state="readonly",
                                   values=["greater_than", "less_than", "equals", "not_equals"], width=15)
condition_type_menu.grid(row=1, column=1, padx=5)

condition_value_entry = ttk.Entry(condition_frame, width=20)
condition_value_entry.grid(row=1, column=2, padx=5)

ttk.Button(condition_frame, text="Add Condition", command=add_condition).grid(row=1, column=3, padx=5)

# listbox to display conditions, also using grid
condition_list_frame = tk.Frame(filter_frame)
tk.Label(condition_list_frame, text="Filter Conditions:").grid(row=0, column=0, sticky="w")
condition_list = tk.Listbox(condition_list_frame, height=5, width=80)
condition_list.grid(row=1, column=0, padx=5, pady=5)

toggle_filter_section()

# run button with enhanced style
run_button = ttk.Button(root, text="Run", command=run_process, style="Accent.TButton")
style.configure("Accent.TButton", font=("Helvetica", 12, "bold"), foreground="white", background="#1f77b4")
run_button.pack(pady=20)

root.mainloop()
