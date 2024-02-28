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
02-06-2024  Rename some variables for consistency. verify both parts of filter are
            nonempty. Move "all data" button to bottom of filter_ui frame.
02-16-2024  Begin changing the plotting UI to grid geometry.
02-17-2024  Remove commented .pack calls, and unnecessary variables.
02-22-2024  Debug category setting for scatter plots. Remove commented-out code.
            Update comments and TODO.
02-23-2024  Scatter category now works.
02-25-2024  Move scatterplot Entry widget to external module, myglobals.py.
            More UI will be moved later. Rename data_items to data_columns.
02-27-2024  Debug line and bar plot selection UI.
02-28-2024  Renamed plotting_ui Frame to plotting_main. Moved line plot
            and bar plot UI elements to a class in plotting_ui.py. This object
            includes a Frame, Label and Combobox for selecting plot parameters.
            Future: Verify we don't need select_plot_item() and then delete.

TODO:
    - ? Need global vars for data column(s) to use for line,bar plots.
        vs: pass values to/from functions.
    - use tkinter.font to control multiple Labels, and the '+' character
    - separate data_filter() into 2 parts: 1) construct query, 2) apply filter,
      since we will eventually apply filters programmatically.
    - separate scatter plot functionality into 2 parts: 1) get settings, 2) create plot,
      since we may eventually change plot settings programmatically.
    - data_filter now returns -1 if the filter failed. Try
      reading this by replacing the button's command attribute
      with a bind().
    - There is a mixture of tk and ttk widgets. ? consistency.
"""

import tkinter as tk
from tkinter import ttk
# import tkinter.font as tkfont

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# external widget UI
import plotting_ui as plotui

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


# def read_checkb(var):
#     print("\t", var.get())

def set_use_category(varname):
    """Checkbutton callback: scatter plot, with/without using categories.
    
    Select a row in the corresponding Listbox.
    """

    do_cat = do_category.get()

    do_cat_test = frame_scatter_basic.getvar(name=varname)

    print('in set_use_category:')
    print(f'   do_cat: {do_cat}')
    print(f'   do_cat_test: {do_cat_test}')

    if int(do_cat) == 1:
        print('selecting category from list...')
        category_lb.select_clear(0)
        category_lb.select_set(1)
    else:
        category_lb.select_clear(1)
        category_lb.select_set(0)


def chkb_extra(ev):
    print('in chkb_extra...')
    print(f'   ev: {ev}')


# debug: demonstrate that the value was set
def set_category(ev):
    """Listbox callback: select categorical variable (data column).
    
    Used for a scatter plot.
    """

    cat = category_lb.get(category_lb.curselection())


# debug: demonstrate that the value list was set
def set_category_value_list(ev):
    """Entry callback: set the category value list."""

    cat_list = category_values_ent.get()
    print(f'in set_category list: {cat_list}')
    print()


def add_criterion_row(n):
    """Add a row of widgets to input a filter criterion."""

    if n == len(filt_rows):
        # no more rows
        return

    filt_rows[n].grid(row=n, column=0)
    filt_buttons[n - 1].configure(text = '-')

    if n == len(filt_rows) - 1:
        # this is the last row
        filt_buttons[n].configure(text = '-')

    # change callback fxn to remove the row...
    filt_buttons[n - 1].configure(command=lambda d=n - 1: remove_criterion_row(d))


def remove_criterion_row(n):
    """Remove a row of widgets for a filter criterion.
    
       Data is automatically re-filtered by the remaining criteria.
    """
    # TODO:
    # if the user adds a row and skips entering anything in it,
    # the app will lose track of which rows should have '-' and '+'
    # (all will have '-')

    filt_buttons[n].configure(text = '+')

    filt_entries[n].delete(0, tk.END)

    filt_cboxes[n].set('')
    
    filt_rows[n].grid_remove()

    data_filter(output_win)


# Not used. Is there a use for it?
def select_filter_column(ev):
    """Read Combobox to get item for data filter."""

    which_filt = ev.widget.winfo_name()
    val = ev.widget.get()
    print('in select_filter_column:')
    print(f'...from {which_filt}, filt by: {val}')
    print(f'...widget parent: {ev.widget.winfo_parent()}')
    print()


# def select_plot_item(ev):
#     """Read Combobox widgets to get items for line or bar plot."""

#     which_plot = ev.widget.winfo_name()
#     val = ev.widget.get()
#     print(f'Combobox {which_plot} set to: {val}')

#     match which_plot:
#         case 'lineplot':
#             line_data.set(val)
#             # print(f'...plotting: {line_data.get()}')
#         case 'barplot':
#             bar_data.set(val)
    

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
def clean_column_names(df):
    """Convert single spaces in column names to underscore character.
    
    Future: remove other python-unacceptable characters.
    """
    cols = df.columns
    # print(f'cols: {cols}')
    cols = cols.map(lambda x: x.replace(' ', '_') if isinstance(x, str) else x)
    df.columns = cols

    return df


# def data_filter(win, dcolumn=None):
def data_filter(win):
    """Display a filtered version of the original DataFrame."""

    dcolumn = []
    criteria = []
    terms = []
    quote = ''
    q_expression = ''

    for i in range(len(data_columns)):
        """Another method, instead of of query, is to use a series of 
        terms like: df[col] > 55. This doesn't require cleaning col names.
        """
        current_term = ''
        if filt_vars[i].get() != '' and criterion_vars[i].get() != '':

            dcolumn.append(filt_vars[i].get())
            criteria.append(criterion_vars[i].get())

            print(f'i is: {i}')
            print(f'...filt: {filt_vars[i].get()}, criterion: {criterion_vars[i].get()}')
            print()
            print(f'...criteria list: {criteria}')
            print()

            current_criterion = len(criteria) - 1
            # validated_entry = validate_criterion(criteria[i])
            validated_entry = validate_criterion(criteria[current_criterion])
            if validated_entry['value'] != '':
    
                # ? need this
                # filter_term = validate_term(validated_entry)
    
                # test for numeric value.
                # v2 test: float will pass
                if validated_entry['value'].replace('.', '', 1).isnumeric():
                    quote = ''
                else:
                    # assume a string value
                    quote = '\"'
                # q_expression = dcolumn[i] + filter_term['op'] + quote + filter_term['value'] + quote
                    
                # current_term = dcolumn[i] + validated_entry['op'] + quote + validated_entry['value'] + quote
                current_term = dcolumn[current_criterion] + validated_entry['op'] + quote + validated_entry['value'] + quote
            else:
                print('No valid criterion.')

            terms.append(current_term)

    if len(terms) == 0:
        # no valid filter for this criterion row
        return -1
            
    for t in terms:
        q_expression += (t + ' & ')
    q_expression = q_expression[:-3]

    print()
    print(f'filt columns: {dcolumn}')
    print(f'filt criteria: {criteria}')
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
        print('char1 `value is text')
        op = '=='
        value = input[op_end + 1:]

    # print(f'...in validate_criterion, value is: {value}')
    criterion['op'] = op
    criterion['value'] = value

    return criterion
    

def validate_term(t):
    """Future: Make a reasonable guess about ambiguous filter entry.
     
    Example: >=>>value. Handle typos, redundant operators, numerics in    
    text columns, etc.
    """
    pass
    # return t


def data_unfilter(win, df):
    """Display the complete dataset."""

    dfresult = df
    win.delete('1.0', tk.END)
    win.insert('1.0', dfresult)
    win.tag_add('cyanbkg', '1.0', '1.end')


def line_plot(df: pd.DataFrame,
              xcol: str,
              ycol: tk.StringVar) -> None:
    """Create line plot (the default) for input df."""

    ydata = ycol.get()
    dfsort = df.sort_values(by=ydata)

    print('line_plot params:')
    print(f'   xcol: {xcol}')
    print(f'   ycol: {ycol} = {ydata}')
    print()

    # ? use df.plot.line for clarity
    # df.plot(x=xcol, y=ydata)
    dfsort.plot(x=xcol, y=ydata)
    plt.show()


def bar_plot(df: pd.DataFrame,
             xcol: str,
             ycol: tk.StringVar) -> None:
    """Create bar plot for input df."""

    ydata = ycol.get()
    dfsort = df.sort_values(by=ydata)

    dfsort.plot.bar(x=xcol, y=ydata)
    plt.show()


# def get_category_list():
#     catlist_raw = category_values_ent.get()

#     return list(catlist_raw.split(', '))
    


def scatter_plot(df: pd.DataFrame, 
                 source: object) -> None:
    """Create scatter plot for input df.
    
    Makes a copy of the DataFrame object passed in, to avoid mutating it.
    """
    df2 = pd.DataFrame(df)
    plot_data = None

    category = category_lb.get(category_lb.curselection())

    catlist = plotui.category_values

    print('in scatter plot, got these:')
    print(f'   category: {category}')
    print(f'   catlist: {catlist}')

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
            print('if category else...')
            df2[category] = pd.Categorical(df2[category], categories=catlist, ordered=False)    
            plot_data = df2[df2[category].isin(catlist)]
    else:
        plot_data = df2
        category = None

    create_plot(plot_data, category)
    plt.show()


root = tk.Tk()
root.title = 'myocardial strain'

# Style objects will be added later.
# style = ttk.Style()
# style.configure('MyCheckbutton.TCheckbutton', foreground='black')

# print(f'pandas library: {pd.__version__}')
# print(f'pandas dependencies: {pd.show_versions()}')

output_win = tk.Text(root, width=50, height=15,
                     background='beige',
                     foreground='black',
                     borderwidth=2,
                     relief='sunken', name='datawin')
output_win.pack(padx=10, pady=10, fill='x', expand=True)


# ---------- module scope objects
data_columns = ["gender", "age", "TID", "stress EF", "rest EF"]
line_data_source = 'age'
bar_data_source = 'TID'
scatter_data_source = {'x': 'age',
                       'y': 'TID'}
output_win.tag_configure("cyanbkg", background="cyan")
output_win.tag_configure("yellowbkg", background="yellow")

# for scatter plot
use_category = False


# ---------- Read and display the dataset
# ("1.0 lineend" also works for end-of-line)
data_1 = pd.read_csv('data/strain_nml_sample.csv')

data_1 = clean_column_names(data_1)

# TODO: update data_columns with the cleaned version
data_columns = list(data_1.columns)

# debug
# print(f'data_columns:\n{data_columns}')
# print(f'data_columns[2:]:\n{data_columns[2:]}')

# print(f'column age:\n{data_1.sort_values(by=["age"])}')
# END debug

output_win.insert('1.0', data_1)
output_win.tag_add('cyanbkg', '1.0', '1.end')


# ---------- UI for filtered data display
filter_ui = ttk.Frame(root, border=2, relief='raised')

filter_frame = ttk.Frame(filter_ui, border=2, relief='groove')

filter_label = ttk.Label(filter_frame, text='show data:')
filter_label.pack(side='left')

btn_apply_filter = ttk.Button(filter_frame,
                        text='filter:',
                        command=lambda w=output_win: data_filter(w))
                                    #    col=filter_column: data_filter(w, col))
                                    #    : data_filter(w, col))
btn_apply_filter.pack(side='left', padx=5, pady=10)

filter_spec_frame = tk.Frame(filter_frame, border=4, bg='yellow')
filter_spec_frame.pack(side='left', padx=10, pady=10)

filt_rows = []
filt_vars = []
criterion_vars = []
filt_cboxes = []
filt_entries = []
filt_buttons = []

for r in range(len(data_columns)):
    rowframe = tk.Frame(filter_spec_frame, border=2, bg='cyan')
    var = tk.StringVar()
    filt_cb = ttk.Combobox(rowframe, height=3, width=7,
                           exportselection=False,
                           state="readonly",
                           name="item" + str(r),
                           textvariable=var,
                           values=data_columns)

    filt_cb.bind('<<ComboboxSelected>>', select_filter_column)

    criterion = tk.StringVar()    
    entry = ttk.Entry(rowframe, width=7, textvariable=criterion)

    button = ttk.Button(rowframe,
                        text='+',
                        width=1,
                        command=lambda d=r + 1: add_criterion_row(d))
    
    filt_rows.append(rowframe)
    filt_cboxes.append(filt_cb)
    filt_entries.append(entry)
    filt_buttons.append(button)

    filt_vars.append(var)
    criterion_vars.append(criterion)

    filt_cb.grid(row=r, column=0)
    entry.grid(row=r, column=1)
    button.grid(row=r, column=2)

filt_rows[0].grid(row=0, column=0)

btn_data_unfilter = ttk.Button(filter_ui,
                        text='all data',
                        command=lambda w=output_win, d=data_1: data_unfilter(w, d))
btn_data_unfilter.pack(side='bottom', pady=10)

filter_frame.pack(padx=10, pady=10, fill='both')
filter_ui.pack(padx=5, pady=5, fill='both')


# plotting UI
# ===========
plotting_main = ttk.Frame(root, border=2, relief='raised')

# ---------- Line plot selection
# maybe:
# line_data = tk.StringVar(value=data_columns[2])
line_data = tk.StringVar(value='default_line')

btn_line_plot = ttk.Button(plotting_main,
                  text='Line plot',
                  command=lambda df=data_1, x=data_columns[0], c=line_data: line_plot(df, x, c))

# frame_cb1 = ttk.Frame(plotting_main, border=4)

# cb1_label = ttk.Label(frame_cb1,
#                       text="Y data: ",
#                       style="MyLabel.TLabel")

# cb1 = ttk.Combobox(frame_cb1, height=3, width=10,
#                    exportselection=False,
#                    state='readonly',
#                    textvariable=line_data,
#                    name='lineplot',
#                    values=data_columns)

# cb1.current(0)
# cb1.bind('<<ComboboxSelected>>', select_plot_item)
# cb1_label.pack(side="left", fill='x')
# cb1.pack(side="left", fill='x')

frame_cb1 = plotui.FramedCombo(plotting_main,
                               cb_values=data_columns[2:],
                               boxname='lineplot',
                               var=line_data)

# ---------- Bar plot selection
# bar_data = tk.StringVar(value=data_columns[2])
bar_data = tk.StringVar(value='default_bar')

btn_bar_plot = ttk.Button(plotting_main,
                  text='Bar plot',
                  command=lambda df=data_1, x=data_columns[0], c=bar_data: bar_plot(df, x, c))

# frame_cb2 = ttk.Frame(plotting_main, border=4)

# cb2_label = ttk.Label(frame_cb2,
#                       text="Y data: ",
#                       style="MyLabel.TLabel")

# cb2 = ttk.Combobox(frame_cb2, height=3, width=10,
#                    exportselection=False,
#                    state="readonly",
#                    textvariable=bar_data,
#                    name='barplot',
#                    values=data_columns
#                    )
# cb2.current(1)
# cb2.bind('<<ComboboxSelected>>', select_plot_item)
# cb2_label.pack(side="left", fill='x')
# cb2.pack(side='left', fill='x')

frame_cb2 = plotui.FramedCombo(plotting_main,
                               cb_values=data_columns[1:],
                               boxname='barplot',
                               var=bar_data)


# ---------- Scatter plot selection
btn_scatter_plot = ttk.Button(plotting_main,
                   text='scatter plot',
                   command=lambda df=data_1, src=scatter_data_source: scatter_plot(df,
                                                          source=src
                                                          )
                   )

frame_scatter_basic = ttk.Frame(plotting_main, border=2, relief='groove')
do_category = tk.IntVar(master=frame_scatter_basic, value = 0, name='do_category')
do_category_chkb = ttk.Checkbutton(frame_scatter_basic,
                                   text='Use category:',
                                   width=15,
                                   offvalue=0,
                                   variable=do_category,
                                   command=lambda n='do_category': set_use_category(n)
                                   )
                                #  style='MyCheckbutton.TCheckbutton')
do_category_chkb.bind('<Button-1>', chkb_extra)


category_list = ['', 'gender']
cat_var = tk.Variable(value=category_list)

category_lb= tk.Listbox(frame_scatter_basic,
                        exportselection=False,
                        height=2,
                        width=10,
                        listvariable=cat_var
                        )

# not required: use for debug
category_lb.bind('<<ListboxSelect>>', set_category)
category_lb.select_set(0)

# alternate way to load values to the Listbox category_lb
# for ind, val in enumerate(category_list):
#     category_lb.insert(ind, val)

label_cat_list = tk.Label(frame_scatter_basic, text='with category values:')

category_values = '(auto)'
cat_val_var = tk.StringVar(value=category_values)
category_values_ent = plotui.MyEntry(frame_scatter_basic, textvariable=cat_val_var)


do_category_chkb.grid(row=0, column=0, padx=5, sticky='w')

category_lb.grid(row=1, column=0, padx=5, pady=10, sticky='w')

label_cat_list.grid(row=2, column=0, padx=5, sticky='w')
category_values_ent.grid(row=3, column=0, padx=5, pady=5, sticky='w')

# Scatter plot radio buttons ----------
radiob_xframe = tk.Frame(plotting_main,
                         border=4,
                         name='scatter_x')

label_x = tk.Label(plotting_main,
                   text='Plot X',
                   relief='groove',
                   borderwidth=2,
                   font=('Arial', 12, 'bold'))

# ? value of the container attribute (defaults to root)
# xplot = tk.StringVar(radiob_xframe, 'age')
xplot = tk.StringVar(value='age')

radiob_yframe = tk.Frame(plotting_main,
                         border=4,
                         name='scatter_y')

label_y = tk.Label(plotting_main,
                   text='Plot Y',
                   relief='groove',
                   borderwidth=2,
                   font=('Arial', 12, 'bold'))

# ? value of the container attribute (defaults to root)
# yplot = tk.StringVar(radiob_xframe, 'TID')
yplot = tk.StringVar(value='TID')

for i in data_columns:
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
# ---------- END Radio buttons


# grid the plotting UI
# --------------------
btn_line_plot.grid(row=0, column=0, padx=5, pady=10, sticky=tk.W)
frame_cb1.grid(row=0, column=1)

btn_bar_plot.grid(row=1, column=0, padx=5, pady=10, sticky=tk.W)
frame_cb2.grid(row=1, column=1)

btn_scatter_plot.grid(row=2, column=0, padx=5, sticky=tk.W)#, pady=10)
label_x.grid(row=2, column=2)
label_y.grid(row=2, column=3)

frame_scatter_basic.grid(row=3, column=1, padx=5, pady=5)
radiob_xframe.grid(row=3, column=2)
radiob_yframe.grid(row=3, column=3)

plotting_main.pack(padx=5, pady=5)


btnq = ttk.Button(root, text='Quit', command=root.destroy)
btnq.pack(fill='x', padx=10, pady=10)

root.mainloop()