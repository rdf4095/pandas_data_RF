"""
module: rf_custom_ui.py

purpose: provide custom tkinter widget classes.

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
08-30-2024  Add optional callback for the Combobox in FramedCombo.
10-26-2024  Update FramedCombo docstring
"""
"""
TODO: 
"""

import sys
import tkinter as tk
from tkinter import ttk

class MyEntry(ttk.Entry):
    """
    MyEntry : Entry widget that expects a comma-separated list of strings.

    Extends: ttk.Entry

    Attributes
    ----------
    textvariable : tk.StringVar
    value_list : list

    Methods
    -------
    set_cat_val_list:
        Reads the list upon the cursor leaving the widget.
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
        text : str
            default string, or user-entered text
        """
        super().__init__(parent,
                         width=10,
                         exportselection=False)
        
        self.name = name
        self.textvariable = tk.StringVar()
        self.textvariable.set(text)
        self.value_list = []
        self.insert(0, text)

        self.bind('<Leave>', self.set_cat_val_list)

    def set_cat_val_list(self, ev):
        rawlist = self.get()
        list1 = list(rawlist.split(','))
        self.value_list = [e.strip() for e in list1]



class FramedCombo(ttk.Frame):
    """
    FramedCombo : Defines a Frame, containing a Label and a Combobox.

    Extends: ttk.Frame

    Attributes
    ----------
    sep: str
        character appended to the Label text
    label_name: str
        text of the Label
    cb: object
        class variable for external reference to the Combobox widget

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
                       callb=None,
                       posn=None,
                       stick='w'
                 ):
        """
        Inits a FramedCombo object.

        Parameters
        ----------
        cb_values : list
            values passed through to the Combobox.
        display_name : str
            used to construct the text of the Label
        name : str
            name attribute of the Combobox
        var : str
            variable name.
        posn : function
            callback for the ComboboxSelected event.
        posn : list
            x and y position for packing child objects.
        stick : text
            flag for widget placement in the grid

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
        self.callb = callb
        self.posn = posn
        self.display_name = display_name
        self.name = name
        self.stick = stick

        self.sep = ': '
        self.label_name = self.display_name.title() + self.sep
        self.cb = None

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
                        #   validate='key',
                        #   postcommand=self.post,
                          values=self.cb_values,
                          textvariable=self.var
                          )
        self.cb.bind('<<ComboboxSelected>>', self.callb)
        
        self.cb.current(0)

        self.lab.pack(side='left')#, fill='x')
        self.cb.pack(side='left')#, fill='x')

        self.grid(row=self.posn[0], column=self.posn[1], padx=5, pady=10, sticky=self.stick)

    def props(self):
        """Return parameter list for the FramedCombo instance."""
        return (self.__init__.__doc__)