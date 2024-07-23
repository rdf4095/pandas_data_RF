"""
module: multi_select.py

purpose: provide expandable widget UI for selecting options.

author: Russell Folks

history:
-------
07-21-2024  creation
07-22-2024  Rename functions using "selection" instead of "criterion".
            Access calling module's objects using sys.modules. This is better
            than using local vars because each var used is prefixed with "sys",
            indicating that it is not defined locally.
"""
"""
TODO:
"""
import tkinter as tk
from tkinter import ttk
import sys

# test access to caller's variables that are needed in this module.
this = sys.modules['__main__']

def create_selection_row(windows: dict) -> object:
    """Add a new row of widgets for making a selection-from-list."""
    """
    module variables:
        filter_spec_fr
    """
    # print(f'in multi_select/create_slection_row, data_columns is:\n{this.data_columns}')
    nextrowframe = ttk.Frame(this.filter_spec_fr, border=2)

    var = tk.StringVar()
    filt_cb = ttk.Combobox(nextrowframe, height=3, width=7,
                           exportselection=False,
                           state="readonly",
                           textvariable=var,
                           values=this.data_columns)

    criterion = tk.StringVar()    
    entry = ttk.Entry(nextrowframe, width=7, textvariable=criterion)

    button_subt = ttk.Button(nextrowframe,
                             text='-',
                             width=1,
                             command=lambda rf=nextrowframe,
                                            w=windows: remove_selection_row(rf, w))
                            #  command=lambda: remove_criterion_row(nextrowframe, windows))

    button_add = ttk.Button(nextrowframe,
                            text='+',
                            width=1,
                            command=lambda w=windows: add_selection_row(w))
                            # command=lambda: add_criterion_row(windows))
    
    filt_cb.grid(row=0, column=0)
    entry.grid(row=0, column=1)
    button_subt.grid(row=0, column=2)
    button_add.grid(row=0, column=3)

    # what is this?
    # button_add.configure

    return nextrowframe


def add_selection_row(windows: dict) -> None:
    """Add a row of widgets to define a selection-from-list.
    
    The 'criteria' button must be used to filter with the new criterion.
    module variables:
        filt_rows
        data_columns
    """
    rows_gridded = [r for r in this.filt_rows if len(r.grid_info().items()) > 0]
    num_gridded = len(rows_gridded)

    if num_gridded == len(this.data_columns):
        return

    newrow = create_selection_row(windows)
    this.filt_rows.append(newrow)
    newrow.grid(row=num_gridded, column=0, sticky='nw')

    for row in rows_gridded:
        row.winfo_children()[3].grid_remove()

    if this.do_debug:
        print(f'in function: {sys._getframe().f_code.co_name}')
        print(f'...called by: {sys._getframe().f_back.f_code.co_name}')
        print(f'adding row')
        print(f'   {num_gridded} rows on grid:')
        for r in rows_gridded:
            print(f'   {r}')

        print(f'   ...new row {newrow} at row: {num_gridded}')
        print()


def remove_selection_row(rowframe: object, windows: dict) -> None:
    """Remove a row of widgets specifying a selection-from-list.
    
    Data is automatically re-filtered by the remaining criteria.
    module variables:
        filt_rows
        data_1: passed to my_fxn
    """
    rows_gridded = [r for r in this.filt_rows if len(r.grid_info().items()) > 0]
    num_gridded = len(rows_gridded)

    # don't remove the only row
    if num_gridded == 1:
        return
    
    # clear filter for the row
    rowframe.winfo_children()[0].set('')
    rowframe.winfo_children()[1].delete(0, tk.END)

    rowframe.grid_forget()
    this.filt_rows.remove(rowframe)
    
    for index, r in enumerate(this.filt_rows):
        r.grid_forget()
        r.grid(row=index, column=0, sticky='nw')
    
    rows_now_gridded = [r for r in this.filt_rows if len(r.grid_info().items()) > 0]
    rows_now_gridded[-1].winfo_children()[3].grid(row=0, column=3, sticky='nw')

    if this.do_debug:
        print(f'in function: {sys._getframe().f_code.co_name}')
        print(f'...called by: {sys._getframe().f_back.f_code.co_name}')
        print(f'removing row (filt_rows: {len(filt_rows)})')
        print(f'   {num_gridded} rows on grid:')
        for r in rows_gridded:
            print(f'   {r}')
        # print(f'   removing row {rem["row"]}')
        num_now_gridded = len(rows_now_gridded)
        print(f'   {num_now_gridded} rows now on grid: ')
        for index, r in enumerate(rows_now_gridded):
            print(f'   {r}')
        print()

    # Handle data resulting from the selection, if necessary.
    if this.my_fxn is not None:
        this.my_fxn(this.data_1, windows, rows_gridded)
