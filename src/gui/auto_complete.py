import tkinter as tk
import ttkbootstrap as ttkb
from tkinter import StringVar

class AutocompleteEntry(ttkb.Entry):
    """
    This is a helper class to handle the autocompletion logic for the Column(s) field.
    """
    def __init__(self, autocomplete_list, *args, **kwargs):
        self.root = kwargs.pop("root", None)
        super().__init__(*args, **kwargs)
        if self.root is None:
            self.root = self.winfo_toplevel()
        self.autocomplete_list = sorted(autocomplete_list, key=str.lower)
        self.var = self["textvariable"]
        if not self.var:
            self.var = self["textvariable"] = StringVar()

        self.var.trace("w", self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Return>", self.selection)
        self.bind("<Up>", self.move_up)
        self.bind("<Down>", self.move_down)

        self.dropdown_visible = False

    def changed(self, *args):
        """
      This method is called whenever the user types in the text field. It opens and populates the dropdown (Listbox) with matches if any exist.
      """
        words = self.var.get().split(",")
        word = words[-1].strip()

        if word == "":
            self.close_dropdown()
        else:
            matches = [w for w in self.autocomplete_list if w.lower().startswith(word.lower())]
            if matches:
                if not self.dropdown_visible:
                    self.show_dropdown(matches)
                else:
                    self.update_dropdown(matches)
            else:
                self.close_dropdown()

    def show_dropdown(self, matches):
        """
      This method shows the dropdown Listbox with the matches.
      """
        self.root.update_idletasks()

        self.dropdown_window = tk.Toplevel(self.root)
        self.dropdown_window.wm_overrideredirect(True)
        self.dropdown_window.attributes("-topmost", True)

        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()
        self.dropdown_window.wm_geometry("+%d+%d" % (x, y))

        self.lb = tk.Listbox(self.dropdown_window)
        self.lb.pack()
        self.lb.bind("<Double-Button-1>", self.selection)
        self.lb.bind("<Right>", self.selection)
        self.lb.bind("<Return>", self.selection)
        self.lb.bind("<Up>", self.move_up)
        self.lb.bind("<Down>", self.move_down)

        for w in matches:
            self.lb.insert(tk.END, w)
        self.lb.config(height=min(len(matches), 10))

        self.dropdown_visible = True

    def update_dropdown(self, matches):
        """
      This method updates the contents of the dropdown Listbox.
      """
        self.lb.delete(0, tk.END)
        for w in matches:
            self.lb.insert(tk.END, w)
        self.lb.config(height=min(len(matches), 10))

    def close_dropdown(self):
        """
      This method closes the dropdown Listbox.
      """
        if self.dropdown_visible:
            self.dropdown_window.destroy()
            self.dropdown_visible = False

    def selection(self, event=None):
        """
      This method is called when the user selects an item from the dropdown (via <Right>, <Return> keys, or double-click).
      """
        if self.dropdown_visible:
            words = self.var.get().split(",")
            words[-1] = self.lb.get(tk.ACTIVE)
            self.var.set(", ".join(words))
            self.close_dropdown()
            self.icursor(tk.END)
            return "break"

    def move_up(self, event):
        """
      This method allows navigation upward in the dropdown using the <Up> arrow key.
      """
        if self.dropdown_visible:
            if self.lb.curselection() == ():
                index = "0"
            else:
                index = self.lb.curselection()[0]
            if index != "0":
                self.lb.selection_clear(first=index)
                index = str(int(index) - 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)
            return "break"

    def move_down(self, event):
        """
      This method allows navigation downward in the dropdown using the <Down> arrow key.
      """
        if self.dropdown_visible:
            if self.lb.curselection() == ():
                index = "-1"
            else:
                index = self.lb.curselection()[0]
            if index != tk.END:
                self.lb.selection_clear(first=index)
                index = str(int(index) + 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)
            return "break"
