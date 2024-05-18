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
05-14-2024  Use explicit keyword parameters for classes, instead of **kwargs.
            Add docstrings.
"""

import sys
import tkinter as tk
from tkinter import ttk

this = sys.modules[__name__]

this.value_list = None

class MyEntry(ttk.Entry):
    def __init__(self, parent, name='',
                               text=''
                ):
        super().__init__(parent,
                         exportselection=False)
        
        # self.name = kwargs['name']
        self.textvariable = tk.StringVar()
        # self.textvariable.set(kwargs['text'])
        self.name = name
        self.textvariable.set(text)

        # optional (works)
        # self.bind('<Return>', self.set_cat_val_list)
        self.bind('<Leave>', self.set_cat_val_list)

    def set_cat_val_list(self, ev):
        rawlist = self.get()
        list1 = list(rawlist.split(','))
        print(f'list1: {len(list1)}')
        this.value_list = [e.strip() for e in list1]
        
        print(f'value_list: {this.value_list}')



class FramedCombo(ttk.Frame):
    """
    class: FramedCombo
    parent: ttk.Frame

    child objects: ttk.Label, ttk.Combobox

    methods: create_widgets
    """
    def __init__(self, parent, cb_values=['1', '2', '3'],
                               var=None,
                               posn=None,
                               display_name='',
                               name=''
                 ):
        """
        class: FramedCombo

        Parameters:
        ----------
        cb_values : list
            values passed through to the Combobox
        var : str
            text variable name
        posn : list
            x,y position for packing child objects
        display_name : str
            value of the Label
        name : str
            name attribute of the Combobox
        """
        super().__init__(parent)

        self.cb_values = cb_values
        self.var = var
        self.posn = posn
        self.display_name = display_name
        self.name = name

        self.sep = ': '

        # self.label_name = self.display_name[0].upper() + self.display_name[1:] + self.sep
        self.label_name = self.display_name.title() + self.sep

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

    def props(self):
        return (self.__init__.__doc__)