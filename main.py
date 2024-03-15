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
03-03-2024  Remove commented code (before FramedCombo class.)
            Remove select_plot_item().
03-07-2024  Use FramedCombo class for scatter plot UI. Pass only tk.StringVars
            to scatter_plot(). This is a step toward making the fxn generic.
            Remove old radio button definition to a textfile to document how
            it was done.
03-10-2024  Debug add/delete filter row.

TODO:
    - use tkinter.font to control multiple Labels, and the '+' character
    - separate data_filter() into 2 parts: 1) construct query, 2) apply filter,
      since we will eventually apply filters programmatically.
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
from importlib.machinery import SourceFileLoader

import plotting_ui as plotui

styles_ttk = SourceFileLoader("styles_ttk", "../styles/styles_ttk.py").load_module()

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
    """Add a row of widgets to define a filter criterion."""

    print(f'add row')

    rows_gridded = [r for r in filt_rows if len(r.grid_info().items()) > 0]
    num_gridded = len(rows_gridded)
    print('rows on grid:')
    for r in rows_gridded:
        print(f'   {r}')
    if num_gridded == len(filt_rows):
        return

    rows_not_gridded = [r for r in filt_rows if len(r.grid_info().items()) == 0]
    num_not_gridded = len(rows_not_gridded)
    print('rows not on grid:')
    for r in rows_not_gridded:
        print(f'   {r}')

    print('   removing all "+"')
    for r in filt_rows[0:n]:
        r.winfo_children()[3].grid_remove()

    rows_not_gridded[0].grid(row=n, column=0, sticky='nw')

    print(f'   adding "+" for row {rows_not_gridded[0]}')
    rows_not_gridded[0].winfo_children()[3].grid(row=n, column=3, sticky='w')

    print()


def ORIG_remove_criterion_row(n):
    """Remove a row of widgets for a filter criterion.
    
       Data is automatically re-filtered by the remaining criteria.
    """
    print(f'remove row {n}:')
    rows_gridded = [r for r in filt_rows if len(r.grid_info().items()) > 0]
    num_gridded = len(rows_gridded)
    print(f'   rows on grid: {num_gridded}')

    if num_gridded == 1:
        return
    
    # clear filter for the row
    # print(f'   clearing filter for row {n}')
    filt_cboxes[n].set('')
    filt_entries[n].delete(0, tk.END)

    # don't remove the only row
    # if num_gridded > 1:
    print(f'   removing row {n}')
    filt_rows[n].grid_remove()
    # num_gridded -= 1
    
    rows_now_gridded = [r for r in rows_gridded if len(r.grid_info().items()) > 0]
    num_now_gridded = len(rows_now_gridded)

    # reset display of '-' and '+' buttons
    print('   removing all "+"')
    for row in rows_now_gridded:
        # print(f'row filt {row.winfo_children()[0].get()}')
        row.winfo_children()[3].grid_remove()

    print(f'   adding "+" for row {num_now_gridded - 1}')
    print(f'      filt_vars is {filt_vars[num_now_gridded].get()}')
    # print(f'      cb set to {rows_now_gridded[-1].winfo_children()[0].get()}')
    # rows_now_gridded[-1].winfo_children()[3].grid(row=num_now_gridded - 1, column=3, sticky='w')
    rows_now_gridded[-1].winfo_children()[3].grid(row=num_now_gridded, column=3, sticky='w')
    print()
    data_filter(output_win)


def remove_criterion_row(n):
    """Remove a row of widgets for a filter criterion.
    
       Data is automatically re-filtered by the remaining criteria.
    """
    rows_gridded = [r for r in filt_rows if len(r.grid_info().items()) > 0]
    num_gridded = len(rows_gridded)
    print('rows on grid:')
    for r in rows_gridded:
        print(f'   {r}')

    if num_gridded == 1:
        return
    
    # clear filter for the row
    # filt_cboxes[n].set('')
    # filt_entries[n].delete(0, tk.END)
    n.winfo_children()[0].set('')
    n.winfo_children()[1].delete(0, tk.END)

    # don't remove the only row
    print(f'removing row {n}')
    # filt_rows[n].grid_remove()
    rows_gridded[-2].winfo_children()[3].grid(row=num_gridded - 2, column=3, sticky='nw')
    n.grid_remove()
    
    rows_now_gridded = [r for r in filt_rows if len(r.grid_info().items()) > 0]
    num_now_gridded = len(rows_now_gridded)

    print(f'rows now on grid: {num_now_gridded}')
    for index, r in enumerate(rows_now_gridded):
        print(f'   {r}')
        r.rowconfigure(index, weight=1)


    # re-configure the grid for the current rows
    # for index, row in enumerate(rows_now_gridded):
    #     print(f'   index {index}, row {row}')
    #     row.grid(row=index, column=0, sticky='nw')

        # row.winfo_children()[3].grid_remove()
    
    # print(f'   adding "+" for row {rows_now_gridded[-1]}')
    # rows_now_gridded[-1].winfo_children()[3].grid(row=num_now_gridded, column=3, sticky='nw')

    print()
    data_filter(output_win)


# Not used. Might be used to construct a string to document the filter
# e.g. for exporting the filtered list.
def select_filter_column(ev):
    """Read Combobox to get item for data filter."""

    which_filt = ev.widget.winfo_name()
    val = ev.widget.get()
    # print('in select_filter_column:')
    # print(f'...from {which_filt}, filt by: {val}')
    # print(f'...widget parent: {ev.widget.winfo_parent()}')
    # print()


# NOT USED
def scatter_select_x(x):
    """Select X data for scatter plot."""

    value = x.get()
    # scatter_data_source['x'] = value
    print(f'x to plot: {value}')


# NOT USED
def scatter_select_y(y):
    """Select Y data for scatter plot."""
    
    value = y.get()
    # scatter_data_source['y'] = value
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

            # print(f'i is: {i}')
            # print(f'...filt: {filt_vars[i].get()}, criterion: {criterion_vars[i].get()}')
            # print()
            # print(f'...criteria list: {criteria}')
            # print()

            current_criterion = len(criteria) - 1
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
                    
                current_term = dcolumn[current_criterion] + validated_entry['op'] + quote + validated_entry['value'] + quote
            else:
                print('No valid criterion.')

            terms.append(current_term)

    if len(terms) == 0:
        # no valid filter
        return -1
            
    for t in terms:
        q_expression += (t + ' & ')
    q_expression = q_expression[:-3]

    # print(f'filt columns: {dcolumn}')
    # print(f'filt criteria: {criteria}')
    # print(f'q_expression string: {repr(q_expression)}')
    # print()

    dfresult = data_1.query(q_expression)
    win.delete('1.0', tk.END)
    win.insert('1.0', dfresult)
    win.tag_add('yellowbkg', '1.0', '1.end')

    # update buttons to reflect filter/no filter
    btn_data_unfilter.configure(style='MyButton1.TButton')
    btn_data_filter.configure(style='MyButton2.TButton')


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
        print('char1 value is text')
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

    # update buttons to reflect filter/no filter
    btn_data_unfilter.config(style = 'MyButton2.TButton')
    btn_data_filter.config(style = 'MyButton1.TButton')


def line_plot(df: pd.DataFrame,
              xcol: tk.StringVar,
              ycol: tk.StringVar) -> None:
    """Create line plot (the default) for input df."""

    xdata = xcol.get()
    ydata = ycol.get()
    dfsort = df.sort_values(by=xdata)

    print('line_plot params:')
    print(f'   xcol: {xcol} = {xdata}')
    print(f'   ycol: {ycol} = {ydata}')
    print()

    # ? use df.plot.line for clarity
    # df.plot(x=xcol, y=ydata)
    dfsort.plot(x=xdata, y=ydata)
    plt.show()


def bar_plot(df: pd.DataFrame,
             xcol: tk.StringVar,
             ycol: tk.StringVar) -> None:
    """Create bar plot for input df."""

    xdata = xcol.get()
    ydata = ycol.get()
    dfsort = df.sort_values(by=xdata)

    print('bar_plot params:')
    print(f'   xcol: {xcol} = {xdata}')
    print(f'   ycol: {ycol} = {ydata}')
    print()

    dfsort.plot.bar(x=xdata, y=ydata)
    plt.show()


# def get_category_list():
#     catlist_raw = category_values_ent.get()

#     return list(catlist_raw.split(', '))
    

def scatter_plot(df: pd.DataFrame, 
                 x_variable: tk.StringVar,
                 y_variable: tk.StringVar) -> None:
    """Create scatter plot for input df.
    
    Makes a copy of the DataFrame object passed in, to avoid mutating it.
    """
    df2 = pd.DataFrame(df)
    plot_data = None

    source = {'x': x_variable.get(),
              'y': y_variable.get()}
    # print(f"source x,y: {source['x']}, {source['y']}")

    category = category_lb.get(category_lb.curselection())

    catlist = plotui.category_values

    # print('in scatter plot, got these:')
    # print(f'   category: {category}')
    # print(f'   catlist: {catlist}')

    def create_plot(data, cat):
        data.plot.scatter(x=source['x'],
                          y=source['y'], 
                          c=cat, 
                          cmap='viridis',
                          s=40)

    if category:
        if ((not catlist) or catlist == None or (not isinstance(catlist, list))):
            print('\nWARNING: no category list; finding category values...\n')
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
styles_ttk.CreateStyles()

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

output_win.tag_configure("cyanbkg", background="cyan")
output_win.tag_configure("yellowbkg", background="yellow")

# for scatter plot
# is this needed?
use_category = False


# ---------- Read and display the dataset
# ("1.0 lineend" also works for end-of-line)
data_1 = pd.read_csv('data/strain_nml_sample.csv')

data_1 = clean_column_names(data_1)

# TODO: update data_columns with the cleaned version
data_columns = list(data_1.columns)

output_win.insert('1.0', data_1)
output_win.tag_add('cyanbkg', '1.0', '1.end')


# ---------- UI for filtered data display
filter_ui = ttk.Frame(root, border=2, relief='raised')

filter_frame = ttk.Frame(filter_ui, border=2, relief='groove')

filter_label = ttk.Label(filter_frame, text='show data:')
filter_label.pack(side='left')

btn_data_filter = ttk.Button(filter_frame,
                        text='filter:',
                        command=lambda w=output_win: data_filter(w))

btn_data_filter.pack(side='left', padx=5, pady=10)

filter_spec_frame = tk.Frame(filter_frame, border=4, bg='yellow')
filter_spec_frame.pack(side='left', padx=10, pady=10)

filt_rows = []
filt_vars = []
criterion_vars = []
filt_cboxes = []
filt_entries = []
filt_buttons_add = []
filt_buttons_subt = []

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

    button_subt = ttk.Button(rowframe,
                             text='-',
                             width=1,
                            #  command=lambda d=r: remove_criterion_row(d))
                             command=lambda rf=rowframe: remove_criterion_row(rf))

    button_add = ttk.Button(rowframe,
                            text='+',
                            width=1,
                            command=lambda d=r + 1: add_criterion_row(d))
    
    # try 03-15-2024
    # rowframe.columnconfigure(0, weight=1)
    # rowframe.columnconfigure(1, weight=1)
    # rowframe.columnconfigure(2, weight=1)
    # rowframe.columnconfigure(3, weight=1)
    rowframe.rowconfigure(r, weight=1)

    filt_rows.append(rowframe)
    filt_cboxes.append(filt_cb)
    filt_entries.append(entry)
    filt_buttons_subt.append(button_add)
    filt_buttons_add.append(button_add)

    filt_vars.append(var)
    criterion_vars.append(criterion)

    filt_cb.grid(row=r, column=0)
    entry.grid(row=r, column=1)
    button_subt.grid(row=r, column=2)
    button_add.grid(row=r, column=3)

# filt_rows[0].grid(row=0, column=0, sticky='w')
filt_rows[0].grid(row=0, column=0, sticky='nw')

# print(f'filt_rows[0] grid info: {filt_rows[0].grid_info()}')
# print(f'filt_rows[1] grid info: {filt_rows[1].grid_info()}')
# print(f'   items: {filt_rows[1].grid_info().items}')

btn_data_unfilter = ttk.Button(filter_ui,
                        text='all data',
                        style='MyButton2.TButton',
                        command=lambda w=output_win, d=data_1: data_unfilter(w, d))
btn_data_unfilter.pack(side='bottom', pady=10)

filter_frame.pack(padx=10, pady=10, fill='both')
filter_ui.pack(padx=5, pady=5, fill='both')


# plotting UI
# ===========
plotting_main = ttk.Frame(root, border=2, relief='raised')

# ---------- Line plot
# line_data = tk.StringVar(value=data_columns[2])
line_data_x = tk.StringVar()
line_data_y = tk.StringVar()

btn_line_plot = ttk.Button(plotting_main,
                  text='Line plot',
                  command=lambda df=data_1, x=line_data_x, y=line_data_y: line_plot(df, x, y))

frame_line_x = plotui.FramedCombo(plotting_main,
                                  cb_values=data_columns,
                                  name='x data',
                                  var=line_data_x,
                                  posn=[0,1])

frame_line_y = plotui.FramedCombo(plotting_main,
                                  cb_values=data_columns[2:],
                                  name='y data',
                                  var=line_data_y,
                                  posn=[0,2])

# ---------- Bar plot
# bar_data = tk.StringVar(value=data_columns[2])
bar_data_x = tk.StringVar()
bar_data_y = tk.StringVar()

btn_bar_plot = ttk.Button(plotting_main,
                  text='Bar plot',
                  command=lambda df=data_1, x=bar_data_x, y=bar_data_y: bar_plot(df, x, y))

frame_bar_x = plotui.FramedCombo(plotting_main,
                               cb_values=data_columns,
                               name='x data',
                               var=bar_data_x,
                               posn=[1,1])

frame_bar_y = plotui.FramedCombo(plotting_main,
                               cb_values=data_columns[1:],
                               name='y data',
                               var=bar_data_y,
                               posn=[1,2])

# ---------- Scatter plot selection
scatter_x = tk.StringVar()
scatter_y = tk.StringVar()
btn_scatter_plot = ttk.Button(plotting_main,
                   text='Scatter plot',
                   command=lambda df=data_1, x=scatter_x, y=scatter_y: scatter_plot(df, x, y)
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

# alternate way to load values to the Listbox category_lb. This may be the
# only way to number the list items.
# for ind, val in enumerate(category_list):
#     category_lb.insert(ind, val)

label_cat_list = tk.Label(frame_scatter_basic, text='with category values:')

category_values = '(auto)'
cat_val_var = tk.StringVar(value=category_values)
category_values_ent = plotui.MyEntry(frame_scatter_basic, textvariable=cat_val_var)


do_category_chkb.grid(row=0, column=0, padx=5, sticky='w')

category_lb.grid(row=1, column=0, padx=5, pady=10, sticky='w')

label_cat_list.grid(row=0, column=1, padx=5, sticky='w')
category_values_ent.grid(row=1, column=1, padx=5, pady=5, sticky='w')

scatter_x_fr = plotui.FramedCombo(plotting_main,
                               cb_values=data_columns,
                               name='x data',
                               var=scatter_x,
                               posn=[2,1])

scatter_y_fr = plotui.FramedCombo(plotting_main,
                               cb_values=data_columns[1:],
                               name='y data',
                               var=scatter_y,
                               posn=[2,2])


# grid the plotting UI
# --------------------
btn_line_plot.grid(row=0, column=0, padx=5, pady=10, sticky=tk.W)
btn_bar_plot.grid(row=1, column=0, padx=5, pady=10, sticky=tk.W)
btn_scatter_plot.grid(row=2, column=0, padx=5, pady=10, sticky=tk.W)
frame_scatter_basic.grid(row=3, column=0, columnspan=3, padx=5, pady=10)

plotting_main.pack(padx=5, pady=5)

btnq = ttk.Button(root, text='Quit', command=root.destroy)
btnq.pack(fill='x', padx=10, pady=10)

root.mainloop()