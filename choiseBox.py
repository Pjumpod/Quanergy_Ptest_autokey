from tkinter import *
from tkinter import ttk

class choiseBox:
    def __init__(self,title,text,choices):
        self.t = Toplevel()
        self.t.title(title if title else "")
        self.selection = None
        Label(self.t, text=text if text else "").grid(row=0, column=0)
        self.c = ttk.Combobox(self.t, value=choices if choices else [], state="readonly")
        self.c.grid(row=0, column=1)
        self.c.bind("<<ComboboxSelected>>", self.combobox_select)

    def combobox_select(self,event):
        self.selection = self.c.get()
        # self.t.destroy()