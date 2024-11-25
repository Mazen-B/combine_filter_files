import tkinter as tk
import ttkbootstrap as ttkb
from tkinter import StringVar

class AutocompleteEntry(ttkb.Entry):
    """
  This is a helper class to handle the autocompletion logic for the Column(s) field.
  """
    def __init__(self, autocomplete_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.autocomplete_list = sorted(autocomplete_list, key=str.lower)
        self.var = self["textvariable"]
        if self.var == "":
            self.var = self["textvariable"] = StringVar()

        self.var.trace("w", lambda *args: self.changed())
        self.bind("<Right>", self.selection)
        self.bind("<Return>", self.selection)
        self.bind("<Up>", self.move_up)
        self.bind("<Down>", self.move_down)

        self.lb_up = False

    def changed(self):
        """
      This method is called whenever the user types in the text field. It opens and populates the dropdown (Listbox) with matches if any exist
      """
        words = self.var.get().split(",")
        word = words[-1].strip()
        if word == "":
            if self.lb_up:
                self.lb.destroy()
                self.lb_up = False
        else:
            matches = [w for w in self.autocomplete_list if w.lower().startswith(word.lower())]
            if matches:
                if not self.lb_up:
                    self.lb = tk.Listbox()
                    self.lb.bind("<Double-Button-1>", self.selection)
                    self.lb.bind("<Right>", self.selection)
                    self.lb.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
                    self.lb_up = True

                self.lb.delete(0, tk.END)
                for w in matches:
                    self.lb.insert(tk.END, w)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False

    def selection(self, event):
        """
      This method is called when the user selects an item from the dropdown (via <Right>, <Return> keys, or double-click).
      """
        if self.lb_up:
            words = self.var.get().split(",")
            words[-1] = self.lb.get(tk.ACTIVE)
            self.var.set(", ".join(words))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(tk.END)

    def move_up(self, event):
        """
      This method allows navigation upward in the dropdown using the <Up> arrow key.
      """
        if self.lb_up:
            if self.lb.curselection() == ():
                index = "0"
            else:
                index = self.lb.curselection()[0]
            if index != "0":
                self.lb.selection_clear(first=index)
                index = str(int(index) - 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def move_down(self, event):
        """
      This method allows navigation downward in the dropdown using the <Down> arrow key.
      """
        if self.lb_up:
            if self.lb.curselection() == ():
                index = "-1"
            else:
                index = self.lb.curselection()[0]
            if index != tk.END:
                self.lb.selection_clear(first=index)
                index = str(int(index) + 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)
