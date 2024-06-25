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
05-25-2024  Update docstrings for the FramedCombo class. Fix MyEntry text arg.
            Change value_list from a module var to a MyEntry class var, to allow
            each MyEntry instance to keep its own value.
05-30-2024  Add docstrings to MyEntry class.
06-09-2024  Standardize docstrings.
"""
"""
TODO: 
"""

import sys
import tkinter as tk
from tkinter import ttk

this = sys.modules[__name__]
# print(f'this is {this}')

# this.value_list = None

class MyEntry(ttk.Entry):
    """
    MyEntry : Entry widget expecting a comma-separated list of strings.

    Subclass of: ttk.Entry

    Attributes
    ----------
    textvariable : tk.StringVar
    value_list : list

    Methods
    -------
    set_cat_val_list:
        Reads the list upon cursor leaving the Entry.
    """
    def __init__(self, parent,
                       name='',
                       text=''
                ):
        """
        Inits a MyEntry object.

        Parameters
        ----------
        name : str
            widget name attribute
        test : str
            default string, or user-entered text
        """
        super().__init__(parent,
                         width=10,
                         exportselection=False)
        
        # self.name = kwargs['name']
        self.name = name
        self.textvariable = tk.StringVar()
        self.textvariable.set(text)
        self.value_list = []
        self.insert(0, text)

        # optional (works)
        # self.bind('<Return>', self.set_cat_val_list)
        self.bind('<Leave>', self.set_cat_val_list)

    def set_cat_val_list(self, ev):
        rawlist = self.get()
        list1 = list(rawlist.split(','))
        self.value_list = [e.strip() for e in list1]



class FramedCombo(ttk.Frame):
    """
    FramedCombo : Defines a Frame, containing a Combobox and a Label.

    Subclass of: ttk.Frame

    Attributes
    ----------
    label_name: str
        text of the Label.

    Methods
    -------
    create_widgets:
        pass
    props:
        pass
    """
    def __init__(self, parent, 
                       cb_values=['1', '2', '3'],
                       display_name='',
                       name='',
                       var=None,
                       posn=None,
                       stick='w'
                 ):
        """
        Inits a FramedCombo object.

        Parameters
        ----------
        cb_values : list
            values passed through to the Combobox.
        var : str
            variable name.
        posn : list
            x and y position for packing child objects.
        display_name : str
            used to construct the text of the Label.
        name : str
            name attribute of the Combobox.

        Methods
        -------
        create_widgets:
            Creates and displays the widgets.
        props:
            Returns the parameter list for an instance of the class.
        """
        super().__init__(parent)
        
        self.cb_values = cb_values
        self.var = var
        self.posn = posn
        self.display_name = display_name
        self.name = name
        self.stick = stick

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

        self.lab.pack(side='left')#, fill='x')
        self.cb.pack(side='left')#, fill='x')

        self.grid(row=self.posn[0], column=self.posn[1], padx=5, sticky=self.stick)

    def props(self):
        """Return parameter list for the FramedCombo instance."""
        return (self.__init__.__doc__)