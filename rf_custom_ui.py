"""
module: rf_custom_ui.py

purpose: provide widget UI and variables for a data review and
         plotting application.

author: Russell Folks

history:
-------
02-24-2024  creation
03-03-2024  Add create_widgets() to FramedCombo class. Pass in label value.
03-04-2024  Use **kwargs for FramedCombo class.
03-05-2024  Append separator character(s) to Label.
04-16-2024  Remove unused variables. Rename 'category_values' to 'value_list'
            to make this module more generic.
"""
"""
TODO:
- for FramedCombo, make 'name' parameter optional
- for MyEntry, make 'name' parameter optional?
"""

import sys
import tkinter as tk
from tkinter import ttk

this = sys.modules[__name__]

this.value_list = None

class MyEntry(ttk.Entry):
    def __init__(self, parent, **kwargs):
        # super().__init__(parent, **kwargs,
        #                  exportselection=False,
        #                  name='cat_list_entry')
        super().__init__(parent,
                         exportselection=False)
        
        self.name = kwargs['name']
        self.textvariable = tk.StringVar()
        self.textvariable.set(kwargs['text'])
        # self.bind('<Return>', self.set_cat_val_list)
        self.bind('<Leave>', self.set_cat_val_list)

    def set_cat_val_list(self, ev):
        rawlist = self.get()
        list1 = list(rawlist.split(','))
        this.value_list = [e.strip() for e in list1]
        
        print(f'value_list: {this.value_list}')
        print(f'MyEntry name: {self.name}')
        print(f'textvariable: {self.textvariable.get()}')



class FramedCombo(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent)

        # self.parent = parent
        self.cb_values = kwargs['cb_values']
        self.var = kwargs['var']
        self.posn = kwargs['posn']
        self.name = kwargs['name']
        self.sep = ': '

        self.label_name = self.name[0].upper() + self.name[1:] + self.sep

        self.create_widgets()

    def create_widgets(self):
        self.lab = ttk.Label(self,
                        text=self.label_name)
        
        self.cb = ttk.Combobox(self,
                          height=3,
                          width=10,
                          exportselection=False,
                          state='readonly',
                          name=self.name,
                          values=self.cb_values,
                          textvariable=self.var
                          )
        self.cb.current(0)

        self.lab.pack(side='left', fill='x')
        self.cb.pack(side='left', fill='x')

        self.grid(row=self.posn[0], column=self.posn[1], padx=10)