"""
program: main.py

purpose: basic operations with pandas library

comments: For Combobox and Listbox, exportselection=False is needed. Without this, 
          using the combo will clear the Listbox, generating a new ListboxSelect
          event with no content (== error).
          
          Pyarrow will become a required dependency of pandas in the next major 
          release of pandas (pandas 3.0)

author: Russell Folks

history:
-------
11-29-2023  creation
12-01-2023  Add explanatory print statements.
12-03-2023  Refine comments. Modify print statements here and
            in df_basics.py.
12-08-2023  Add function to do basic operations with strain data,
            and button to call it. Add kw param to bar_plot().
            Refine inline comments.
12-09-2023  Add parameters to scatter_plot(). Trim comments,
            remove redundant examples.
12-14-2023  Move some data display to strain_do_basics.py. Update comments.
12-15-2023  Annotate function scatter_plot, and make it more robust by handling
            the case of a missing category list.
12-21-2023  Remove old comments.
01-02-2024  Add output window in the UI, and show_males().
01-04-2024  Highlight data header row, expand sample data file, change
            show_males to data_filter, move simulation fxn to the
            external file strain_test.py.
01-05-2024  refactor scatter_plot().
01-06-2024  Add Combobox to get the data column for line plot.
01-10-2024  Add Radiobuttons for setting x and y data for a scatter plot.
01-12-2024  Add unfilter() to display all data. Use radiobuttons to set scatter data,
            using module-scope variables.
01-20-2024  Read Combobox widgets to determine data column plotted (line, bar).
01-22-2024  Begin UI for data filter options.
01-23-2024  new GitHub repository.
01-27-2024  Create all rows of the data filter in a loop.
01-29-2024  Add validation function for filter criterion.
"""
# TODO: - Need global vars for data column(s) to use for line,bar plots.
#       - use tkinter.font to control multiple Labels, and the '+' character
#       - add category option (gender) to scatter plot UI

import tkinter as tk
from tkinter import ttk
# import tkinter.font as tkfont

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

""" 
----------------------------
widget interaction functions
----------------------------
"""
def attend():
    """postcommand for 1 or more Combobox widgets.
    
    NOT currently used.
    """
    print("combobox activated...")


def read_checkb(var):
    print("\t", var.get())


def add_criterion(n):
    print(f'in add_criterion: {n}')
    match n:
        case 2:
            # crit_row_2.grid(row=1, column=0)
            pass


def remove_row(f):
    """Add or remove a row of widgets for a filter criterion."""

    # Also clear the Entry for the row, so data_filter() does not
    # need to check it.

    pass
    # chk_filt_age.grid_remove()
    # age_crit_entry.grid_remove()
    # btn_add_crit_2.grid_remove()
    

def select_filt_item(ev):
    """Read Combobox to get item for data filter."""

    which_filt = ev.widget.winfo_name()
    val = ev.widget.get()
    # print('last selected filter:')
    # print(f'from {which_filt}, filt by: {val}')
    # print('all filters:')
    # for i in filt_vars:
    #     print(i.get())
    # print('all criteria:')
    # for j in criterion_vars:
    #     print(j.get())


def select_plot_item(ev):
    """Read Comboboxes to get items for line,bar plot."""

    which_plot = ev.widget.winfo_name()
    val = ev.widget.get()
    print(f'Combobox {which_plot} set to: {val}')

    match which_plot:
        case 'lineplot':
            line_data.set(val)
            # print(f'...plotting: {line_data.get()}')
        case 'barplot':
            bar_data.set(val)
    

def scatter_select_x(x):
    """Select X data for scatter plot."""

    value = x.get()
    scatter_data_source['x'] = value
    print(f'x to plot: {value}')


def scatter_select_y(y):
    """Select Y data for scatter plot."""
    
    value = y.get()
    scatter_data_source['y'] = value
    print(f'y to plot: {value}')


""" 
--------------------------
data interaction functions
--------------------------
"""
def data_filter(win, dcolumn=None):
    """Display a filtered version of the original DataFrame."""
    # TODO: loop through criteria and connect each one using ' & '

    quote = ''
    dcolumn = []
    criteria = []
    q_expression = ''

    for i in range(len(data_items)):
        if filt_vars[i].get() != '':
            # print('adding criterion:')
            # print(f'    {filt_vars[i].get()}')
            # print(f'    {criterion_vars[i].get()}')
            dcolumn.append(filt_vars[i].get())
            criteria.append(criterion_vars[i].get())

    print(f'filt columns: {dcolumn}')
    print(f'filt criteria: {criteria}')

    validated_entry = validate_criterion(criteria[0])
    if validated_entry['value'] != '':
        filter_term = validate_term(validated_entry)
        # test for numeric value.
        # v1 test: float won't pass
        # if not filter_term['value'].isnumeric():

        # v2 test: float will pass
        if not filter_term['value'].replace('.', '', 1).isnumeric():
            # assume a string value, and add quote marks
            quote = '\"'

        # v3 test: more comprehensive
        """
        from decimal import Decimal, InvalidOperation

        def is_decimal(s):
            try:
                Decimal(s)
                return True
            except InvalidOperation:
                return False
        """
        q_expression = dcolumn[0] + filter_term['op'] + quote + filter_term['value'] + quote
    else:
        print('No valid criterion.')

    print(f'q_expression string: {repr(q_expression)}')
    dfresult = data_1.query(q_expression)
    win.delete('1.0', tk.END)
    win.insert('1.0', dfresult)
    win.tag_add('yellowbkg', '1.0', '1.end')


def validate_criterion(input):
    char1 = input[0]
    op = ''
    op_end = -1
    value = ''
    v = '1.02'
    
    print()    # debug
    criterion = {'op': '',
                 'value': value}

    if char1 in ['=', '>', '<']:
        op_end = input.rfind('=')
        if op_end > -1:
            # op = input[:op_end + 1]
            match op_end:
                case 0:
                    op = '=='
                case 1:
                    op = input[0:2]
                case _:
                    op = input[0:2]
                    print(f'accepting nonstandard operator: {input[0:op_end + 1]} as: {op}')

            value = input[op_end + 1:]
        else:
            op = input[0]
            value = input[1:]
    else:
        print('value is text')
        op = '=='
        value = input[op_end + 1:]

    print(f'in validate_criterion, value is: {value}')
    criterion['op'] = op
    criterion['value'] = value
    return criterion
    

def validate_term(t):
    # if t['value'].isnumeric():
    #     t['value'] = float(t['value'])
    return t


def data_unfilter(win, df):
    """Display the complete dataset."""

    # ? clear filter criteria or leave them

    dfresult = df
    win.delete('1.0', tk.END)
    win.insert('1.0', dfresult)
    win.tag_add('cyanbkg', '1.0', '1.end')


def line_plot(df: pd.DataFrame, col: tk.StringVar):
    """Create line plot (the default) for input df."""

    ydata = col.get()

    # ? use df.plot.line for clarity
    df.plot(x='pt code', y=ydata)
    plt.show()


def bar_plot(df: pd.DataFrame, col: tk.StringVar):
    """Create bar plot for input df."""

    ydata = col.get()

    df.plot.bar(x='pt code', y=ydata)
    plt.show()


def scatter_plot(df: pd.DataFrame, 
                 source: object,
                 category: str = None,
                 catlist: list = []) -> None:
    """Create scatter plot for input df.
    
    Makes a copy of the DataFrame object passed in, to avoid mutating it.
    """
    df2 = pd.DataFrame(df)
    plot_data = None

    def create_plot(data, cat):
        data.plot.scatter(x=source['x'],
                          y=source['y'], 
                          c=cat, 
                          cmap='viridis',
                          s=40)

    if category:
        if ((not catlist) or catlist == None or (not isinstance(catlist, list))):
            print('\nWARNING: no valid category list; finding category values...\n')
            df2[category] = df2[category].astype('category')
            plot_data = df2
        else:
            df2[category] = pd.Categorical(df2[category], categories=catlist, ordered=False)    
            plot_data = df2[df2[category].isin(catlist)]
    else:
        plot_data = df2

    create_plot(plot_data, category)
    plt.show()


root = tk.Tk()
root.title = 'myocardial strain'

output_win = tk.Text(root, width=50, height=15,
                     background='beige',
                     foreground='black',
                     borderwidth=2,
                     relief='sunken', name='datawin')
output_win.pack(padx=10, pady=10, fill='x', expand=True)


# ---------- module scope variables & objects
data_items = ["gender", "age", "TID", "stress EF", "rest EF"]
line_data_source = 'age'
bar_data_source = 'TID'
scatter_data_source = {'x': 'age',
                       'y': 'TID'}
output_win.tag_configure("cyanbkg", background="cyan")
output_win.tag_configure("yellowbkg", background="yellow")


# ---------- Read and display the dataset
# ("1.0 lineend" also works for end-of-line)
data_1 = pd.read_csv('data/strain_nml_sample.csv')

# test and debug: characterize the dataset
# print(data_1)
# print(f'shape of data_1: {data_1.shape}')
# print(f'columns in data_1: {data_1.shape[1]}')
# print('types:')
# for c in data_1.columns:
#     # print(c)
#     print(type(data_1[c]))

output_win.insert('1.0', data_1)
output_win.tag_add('cyanbkg', '1.0', '1.end')


# ---------- filter the data display
filter_column = 'gender'
filter_criterion = 'M'

filter_frame = ttk.Frame(root, border=2, relief='raised')

filter_label = ttk.Label(filter_frame, text='show:')
filter_label.pack(side='left')

btn_data_filter = ttk.Button(filter_frame,
                        text='select:',
                        command=lambda w=output_win, 
                                       col=filter_column: data_filter(w, col))
btn_data_filter.pack(side='left', padx=5, pady=10)

# put this below the entire filter frame (so it moves up/down)
btn_data_unfilter = ttk.Button(filter_frame,
                        text='ALL',
                        width=4,
                        command=lambda w=output_win, d=data_1: data_unfilter(w, d))
# btn_data_unfilter.pack(side='left', padx=5, pady=10)

filter_spec_frame = tk.Frame(filter_frame, border=4, bg='yellow')
filter_spec_frame.pack(side='left', padx=10, pady=10)


filt_rows = []
filt_vars = []
criterion_vars = []
filt_cboxes = []
filt_entries = []
filt_buttons = []

for r in range(len(data_items)):
    rowframe = tk.Frame(filter_spec_frame, border=2, bg='cyan')
    var = tk.StringVar()
    filt_cb = ttk.Combobox(rowframe, height=3, width=7,
                           exportselection=False,
                           state="readonly",
                           name="item" + str(r),
                           textvariable=var,
                           values=data_items)
    # filt_cb.current(0)
    filt_cb.bind('<<ComboboxSelected>>', select_filt_item)

    criterion = tk.StringVar()
    
    entry = ttk.Entry(rowframe, width=7, textvariable=criterion)

    button = ttk.Button(rowframe,
                        text='+',
                        width=1,
                        command=lambda d=2: add_criterion(d))

    filt_rows.append(rowframe)
    filt_cboxes.append(filt_cb)
    filt_entries.append(entry)
    filt_buttons.append(button)

    filt_vars.append(var)
    criterion_vars.append(criterion)

    filt_cb.grid(row=r, column=0)
    entry.grid(row=r, column=1)
    button.grid(row=r, column=2)

    rowframe.grid(row=r, column=0)



filter_frame.pack(padx=10, pady=10, fill='both')


# ---------- Line plot selection
line_data = tk.StringVar(value='age')
frame_lineplot_ui = ttk.Frame(root, border=4)
btn_line_plot = ttk.Button(frame_lineplot_ui,
                  text='Line plot',
                  command=lambda df=data_1, c=line_data: line_plot(df, col=c))
btn_line_plot.pack(side='left', padx=10)

frame_cb1 = ttk.Frame(frame_lineplot_ui, border=4)
cb1_label = ttk.Label(frame_cb1, text="data: ",
                style="MyLabel.TLabel")
cb1 = ttk.Combobox(frame_cb1, height=3, width=10,
                   exportselection=False,
                   state='readonly',
                   textvariable=line_data,
                   name='lineplot',
                   values=data_items)
cb1.current(0)
cb1.bind('<<ComboboxSelected>>', select_plot_item)
cb1_label.pack(side="left", fill='x')
cb1.pack(side="left", fill='x')

frame_cb1.pack(padx=5, fill='both')
frame_lineplot_ui.pack(padx=5, fill='x')


# ---------- Bar plot selection
bar_data = tk.StringVar(value='TID')
frame_barplot_ui = ttk.Frame(root, border=4)
btn_bar_plot = ttk.Button(frame_barplot_ui,
                  text='Bar plot',
                  command=lambda df=data_1, c=bar_data: bar_plot(df, col=c))
btn_bar_plot.pack(side='left', padx=10)

frame_cb2 = ttk.Frame(frame_barplot_ui, border=4)
cb2_label = ttk.Label(frame_cb2, text="data: ",
                style="MyLabel.TLabel")
cb2 = ttk.Combobox(frame_cb2, height=3, width=10,
                   exportselection=False,
                   state="readonly",
                   textvariable=bar_data,
                   name='barplot',
                   values=data_items)
cb2.current(1)
cb2.bind('<<ComboboxSelected>>', select_plot_item)
cb2_label.pack(side="left", fill='x')
cb2.pack(side='left', fill='x')

frame_cb2.pack(padx=5, fill='both')
frame_barplot_ui.pack(padx=5, fill='x')

# ---------- Scatter plot selection
frame_scatterplot_ui = ttk.Frame(root, border=2, relief='raised')

btn_scatter_plot = ttk.Button(frame_scatterplot_ui,
                  text='scatter plot',
                  command=lambda df=data_1: scatter_plot(df,
                                                         source=scatter_data_source,
                                                         category='gender',
                                                         catlist=['M', 'F'])
                  )
btn_scatter_plot.pack(side='left', padx=10)

# Radio buttons ----------
radiob_xframe = tk.Frame(frame_scatterplot_ui,
                         border=4,
                         name='scatter_x')
radiob_xframe.pack(padx=5, pady=5)
label_x = tk.Label(radiob_xframe,
                   text='Plot X',
                   relief='groove',
                   borderwidth=2,
                   font=('Arial', 12, 'bold'))
label_x.pack(fill='x', pady=5)

xplot = tk.StringVar(radiob_xframe, 'age')

radiob_yframe = tk.Frame(frame_scatterplot_ui,
                         border=4,
                         name='scatter_y')
radiob_yframe.pack(padx=5, pady=5)
label_y = tk.Label(radiob_yframe,
                   text='Plot Y',
                   relief='groove',
                   borderwidth=2,
                   font=('Arial', 12, 'bold'))
label_y.pack(fill='x', pady=5)

yplot = tk.StringVar(radiob_xframe, 'TID')

for i in data_items:
    radiobutx = tk.Radiobutton(radiob_xframe,
                              text=i, value=i,
                              variable=xplot,
                              command=lambda x=xplot: scatter_select_x(x))
    radiobutx.pack(anchor='w', padx=5)

    radiobuty = tk.Radiobutton(radiob_yframe,
                              text=i, value=i,
                              variable=yplot,
                              command=lambda y=yplot: scatter_select_y(y))
    radiobuty.pack(anchor='w', padx=5)

radiob_xframe.pack(side='left', pady=10)
radiob_yframe.pack(side='left', pady=10)
# ---------- END Radio buttons

frame_scatterplot_ui.pack(padx=5, fill='x')


btnq = ttk.Button(root, text='Quit', command=root.destroy)
btnq.pack(fill='x', padx=10, pady=10)

root.mainloop()