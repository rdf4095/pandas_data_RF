"""
module: plotting_ui.py

purpose: provide widget UI and variables for a data review and
         plotting application.

author: Russell Folks

history:
-------
02-24-2024  creation
"""

import sys
from tkinter import ttk

this = sys.modules[__name__]

this.use_category = False
this.category = None
this.category_values = None

class MyEntry(ttk.Entry):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs,
                         exportselection=False,
                         name='cat_list_entry')
        self.bind('<Return>', self.set_cat_val_list)

    def set_cat_val_list(self, ev):
        rawlist = self.get()
        # print(f'from my, rawlist: {rawlist}')

        this.category_values = list(rawlist.split(', '))



class FramedCombo(ttk.Frame):
    def __init__(self, parent, cb_values=None, boxname='', var=None, **kwargs):
        super().__init__(parent, **kwargs,
                         border=4)
        self.cb_values = cb_values

        lab = ttk.Label(self,
                        text='Y data: ')
        
        print('in FramedCombo:')
        print(f'   cb_values: {cb_values}')
        print(f'   var: {var.get()}')

        cb = ttk.Combobox(self,
                          height=3,
                          width=10,
                          exportselection=False,
                          state='readonly',
                          name=boxname,
                          values=self.cb_values,
                          textvariable=var
                          )
        cb.current(0)

        lab.pack(side='left', fill='x')
        cb.pack(side='left', fill='x')


    