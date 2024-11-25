class FilterHandler:
    """
  This is a helper class to handle filtering logic for multiple tabs.
  """
    def __init__(self, allowed_columns, condition_type_map):
        self.allowed_columns = allowed_columns
        self.condition_type_map = condition_type_map

    def add_condition(self, columns_entry, value_entry, condition_type_var, conditions_list, listbox):
        """
      This method adds a condition to the internal conditions list and updates the UI listbox.
      """
        condition_type_display = condition_type_var.get()
        condition_type = self.condition_type_map.get(condition_type_display)

        # get columns from the Entry field
        columns_text = columns_entry.get()
        if not columns_text:
            return "Please enter at least one column."
        columns = [col.strip() for col in columns_text.split(",") if col.strip()]

        # check if columns are in allowed columns
        unknown_columns = [col for col in columns if col not in self.allowed_columns]
        if unknown_columns:
            return f"The following columns are not allowed: {', '.join(unknown_columns)}."

        # handle conditions without values
        if condition_type in ["columns_to_keep", "columns_to_remove"]:
            conditions_list.append((condition_type, columns))
            listbox.insert("end", f"{condition_type_display}: {', '.join(columns)}")
            columns_entry.delete(0, "end")
            return None

        # handle conditions with values
        value = value_entry.get()
        if not value:
            return "Please enter a value for the condition."

        try:
            # validate the value type
            if condition_type in ["greater_than", "less_than"]:
                numeric_value = float(value)
            elif condition_type in ["equals", "not_equals"]:
                numeric_value = float(value) if value.lower() not in ["true", "false"] else value.lower() == "true"
            else:
                numeric_value = value
        except ValueError:
            return f"Invalid value '{value}' for condition '{condition_type_display}'."

        # add the conditions for each column
        for column in columns:
            conditions_list.append((column, condition_type, numeric_value))
            listbox.insert("end", f"{column} {condition_type_display} {numeric_value}")
        columns_entry.delete(0, "end")
        value_entry.delete(0, "end")
        return None

    def remove_condition(self, listbox, conditions_list):
        """
      This method removes the selected condition from the internal list and updates the UI.
      """
        selected_index = listbox.curselection()
        if not selected_index:
            return "No condition selected to remove."
        conditions_list.pop(selected_index[0])
        listbox.delete(selected_index)
        return None

    def toggle_filter_section(self, apply_filter_var, filter_conditions_frame):
        """
      This method toggles the visibility of the filter conditions section based on the state of the "Apply Filter" checkbox.
      """
        if apply_filter_var.get():
            filter_conditions_frame.grid()
        else:
            filter_conditions_frame.grid_remove()

    def on_condition_type_change(self, condition_type_var, value_entry, value_label):
        """
      This method shows or hides the Value entry field based on the selected condition type.
      """
        condition_type_display = condition_type_var.get()
        condition_type = self.condition_type_map.get(condition_type_display)

        if condition_type in ["columns_to_keep", "columns_to_remove"]:
            value_entry.grid_remove()
            value_label.grid_remove()
        else:
            value_label.grid()
            value_entry.grid()
