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
03-18-2024  Finish debug of add/delete filter row. Add window to display result
            of analysis (summary stats, stored query string, etc.)
04-06-2024  Add window for numeric data.
            Add vertical scrollbar (not working.) Delete old code.
04-09-2024  Add scrollbar to stats window. Update parent Frame.
04-11-2024  Rename output_win to data_win.
04-16-2024  Change to rectangular root layout, using .grid(). Add Label to the
            main data ui.
04-19-2024  In plotting ui section, make variable names more consistent (use
            widget name suffixes, e.g. fr = Frame.)
04-22-2024  In filtering ui and statistics ui, revise variable names as above.
04-27-2024  Update statistics window based on how the data is filtered. Move
            styling of statistics window to function style_df_text. Rename
            style tags for main data window. For scatterplot, accept category
            value list upon mouseout of the Entry widget.
05-04-2024  Add n, number of data rows, to statistics window. Remove some
            print statements.
            Filter criterion widget rows are added by passing arguments for
            the output windows (Text widgets).
05-09-2024  Bug fix: when a filter row widget is removed, reset row numbers
            for the remaining rows.
05-16-2024  Small style changes: Bold the panel headings ('data' etc.), stats
            padding & # rows.
05-18-2024  Move 'not used' items to file not_used.py for archiving. Remove some
            old commented lines. Re-arrange global objects definition order.
05-20-2024  Cleaned up the 'inspect functions' section at the bottom, moved some
            old code to not_used.py.
05-22-2024  Debug the inspect section.
05-25-2024  Eliminate the cat_val_var StringVar, since MyEntry creates its own.
05-30-2024  Factor data_filter() into two parts: 1) construct data filter, 
            2) display filtered data.

TODO:
    - use tkinter.font to control multiple Labels, and the '+' character
    - does it make sense to separate "apply filter", so we can apply 
      filters programmatically? (it's only one line.)
    - filter setup now returns -1 if the filter failed. Can we read this
      by replacing the button's command attribute with a bind()?
    - filter fxns use module variables. Can we pass these instead, to make
      the fxns more general-purpose?
"""

import tkinter as tk
from tkinter import ttk
# import tkinter.font as tkfont
from importlib.machinery import SourceFileLoader

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import rf_custom_ui as custui

styles_ttk = SourceFileLoader("styles_ttk", "../styles/styles_ttk.py").load_module()

do_profile = False    # report function signatures

""" 
----------------------------
widget interaction functions
----------------------------
"""
def style_df_text(win: object, itemlist: list=['test']) -> None:
    """Apply text styling to pandas DataFrame (df) displayed in a Text widget.

    The tag that is added is defined externally.
    """
    win.tag_add('bolded', '1.0', '1.end')

    for e in range(2, len(itemlist) + 2):
        row = str(format(e, '0.1f'))
        strend = row + ' wordend'
        win.tag_add('bolded', row, strend)

    win.configure(state='disabled')


def set_use_category(varname: str):
    """Checkbutton callback: for scatter plot, use/don't use categories.
    
    Select a row in the corresponding Listbox.
    """
    do_cat = use_category.get()

    do_cat_test = scatter_setup_fr.getvar(name=varname)

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


def create_criterion_row(datawin: object, statwin: object) -> object:
    """Add a new row of widgets for defining a data filter criterion."""

    nextrowframe = tk.Frame(filter_spec_fr, border=2, bg='cyan')

    var = tk.StringVar()
    filt_cb = ttk.Combobox(nextrowframe, height=3, width=7,
                           exportselection=False,
                           state="readonly",
                           textvariable=var,
                           values=data_columns)

    # filt_cb.bind('<<ComboboxSelected>>', select_filter_column)

    criterion = tk.StringVar()    
    entry = ttk.Entry(nextrowframe, width=7, textvariable=criterion)

    button_subt = ttk.Button(nextrowframe,
                             text='-',
                             width=1,
                             command=lambda rf=nextrowframe, d=datawin, s=statwin: remove_criterion_row(rf, d, s))

    button_add = ttk.Button(nextrowframe,
                            text='+',
                            width=1,
                            command=lambda d=datawin, s=statwin: add_criterion_row(d, s))
    
    filt_cb.grid(row=0, column=0)
    entry.grid(row=0, column=1)
    button_subt.grid(row=0, column=2)
    button_add.grid(row=0, column=3)

    # what is this?
    button_add.configure

    return nextrowframe


def add_criterion_row(datawin: object, statwin: object) -> None:
    """Add a row of widgets to define a filter criterion.
    
    The 'criteria' button must be used to filter with the new criterion.
    """
    rows_gridded = [r for r in filt_rows if len(r.grid_info().items()) > 0]
    num_gridded = len(rows_gridded)
    print(f'adding row (filt_rows: {len(filt_rows)})')
    print(f'   {num_gridded} rows on grid:')
    for r in rows_gridded:
        print(f'   {r}')
        # print(f'   row: {r.grid_info()["row"]}')

    if num_gridded == len(data_columns):
        return

    newrow = create_criterion_row(datawin, statwin)
    print(f'   ...adding row {newrow} at row: {num_gridded}')
    filt_rows.append(newrow)
    newrow.grid(row=num_gridded, column=0, sticky='nw')

    for row in rows_gridded:
        row.winfo_children()[3].grid_remove()

    print()


def remove_criterion_row(n: object, datawin: object, statwin: object) -> None:
    """Remove a row of widgets for a filter criterion.
    
       Data is automatically re-filtered by the remaining criteria.
    """
    rows_gridded = [r for r in filt_rows if len(r.grid_info().items()) > 0]
    num_gridded = len(rows_gridded)

    print(f'removing row (filt_rows: {len(filt_rows)})')
    print(f'   {num_gridded} rows on grid:')
    for r in rows_gridded:
        print(f'   {r}')

    # don't remove the only row
    if num_gridded == 1:
        return
    
    rem = n.grid_info()
    print(f'   removing row {rem["row"]}')
    # clear filter for the row
    n.winfo_children()[0].set('')
    n.winfo_children()[1].delete(0, tk.END)

    n.grid_forget()
    filt_rows.remove(n)
    
    for index, r in enumerate(filt_rows):
        print(f'index, r: {index}, {r}')
        r.grid_forget()
        r.grid(row=index, column=0, sticky='nw')
    
    rows_now_gridded = [r for r in filt_rows if len(r.grid_info().items()) > 0]
    num_now_gridded = len(rows_now_gridded)

    print(f'   rows now on grid: {num_now_gridded}')
    for index, r in enumerate(rows_now_gridded):
        print(f'   {r}')
        # r.rowconfigure(index, weight=1)
    print()

    rows_now_gridded[-1].winfo_children()[3].grid(row=0, column=3, sticky='nw')

    data_filter(datawin, statwin)


""" 
--------------------------
data interaction functions
--------------------------
"""
def clean_column_names(df: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
    """Convert single spaces in column names to underscore character."""

    # print(f'type df to clean: {type(df)}')
    cols = df.columns
    # print(f'cols: {cols}')
    cols = cols.map(lambda x: x.replace(' ', '_') if isinstance(x, str) else x)
    df.columns = cols

    return df


def data_filter_ORIG(win: object, statwin: object) -> None:
    """Display a filtered version of the original DataFrame."""

    dcolumn = []
    criteria = []
    terms = []
    quote = ''
    q_expression = ''

    for i in range(len(filt_rows)):
        """Another method, instead of query, would be to use a series of 
        terms like: df[col] > 55. This doesn't require cleaning col names.
        """
        current_term = ''

        this_filter = filt_rows[i].winfo_children()[0].get()
        this_criterion = filt_rows[i].winfo_children()[1].get()
        print(f'filt, crit: {this_filter}, {this_criterion}')

        if this_filter != '' and this_criterion != '':

            # dcolumn.append(filt_vars[i].get())
            # criteria.append(criterion_vars[i].get())
            dcolumn.append(this_filter)
            criteria.append(this_criterion)

            # print()

            current_criterion = len(criteria) - 1
            validated_entry = validate_criterion(criteria[current_criterion])
            if validated_entry['value'] != '':
    
                # ? need this
                # filter_term = validate_term(validated_entry)
    
                # test for numeric value.
                # test: float will pass
                if validated_entry['value'].replace('.', '', 1).isnumeric():
                    quote = ''
                else:
                    # string value
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
    print(f'q_expression string: {repr(q_expression)}')
    print()

    data_current = data_1.query(q_expression)

    win.configure(state='normal')
    win.delete('1.0', tk.END)

    win.insert('1.0', data_current)
    win.tag_add('redtext', '1.0', '1.end')
    win.configure(state='disabled')

    stats_agg = data_current.agg(stats_dict)
    stat_win.configure(state='normal')
    statwin.delete('1.0', tk.END)
    with pd.option_context('display.float_format', '{:0.2f}'.format):
        statwin.insert('1.0', stats_agg)

    # statwin.tag_add('bolded', '1.0', '1.end')
    style_df_text(statwin, stat_list)

    nvalue = 'n = ' + str(data_current.count().iloc[0])
    stat_n_lab.configure(text=nvalue)


    # print('filtered stats:')
    # print(f'data_current is\n {data_current}')
    # print(f'stat_win is {stat_win}')
    # print(f'stats_agg is\n {stats_agg}')
    # print()

    data_unfilter_btn.configure(style='MyButton1.TButton')
    data_filter_btn.configure(style='Opt1_on.TButton')

# new
def data_filter(win, statwin):
    d = make_filter()
    show_filtered(win, statwin, d)

# new
def make_filter():
    dcolumn = []
    criteria = []
    terms = []
    quote = ''
    q_expression = ''

    for i in range(len(filt_rows)):
        """query() requires cleaning column names.
        Another method would be to use a series of terms like: df[col] > 55.
        """
        current_term = ''

        this_filter = filt_rows[i].winfo_children()[0].get()
        this_criterion = filt_rows[i].winfo_children()[1].get()
        print(f'filt, crit: {this_filter}, {this_criterion}')

        if this_filter != '' and this_criterion != '':
            dcolumn.append(this_filter)
            criteria.append(this_criterion)

            current_criterion = len(criteria) - 1
            validated_entry = validate_criterion(criteria[current_criterion])
            if validated_entry['value'] != '':
    
                # test for numeric value.
                # test: float will pass
                if validated_entry['value'].replace('.', '', 1).isnumeric():
                    quote = ''
                else:
                    # string value
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
    print(f'q_expression string: {repr(q_expression)}')
    print()

    data_current = data_1.query(q_expression)

    return data_current

# new
def show_filtered(win, statwin, data):
    win.configure(state='normal')
    win.delete('1.0', tk.END)

    win.insert('1.0', data)
    win.tag_add('redtext', '1.0', '1.end')
    win.configure(state='disabled')

    stats_agg = data.agg(stats_dict)
    stat_win.configure(state='normal')
    statwin.delete('1.0', tk.END)
    with pd.option_context('display.float_format', '{:0.2f}'.format):
        statwin.insert('1.0', stats_agg)

    # statwin.tag_add('bolded', '1.0', '1.end')
    style_df_text(statwin, stat_list)

    nvalue = 'n = ' + str(data.count().iloc[0])
    stat_n_lab.configure(text=nvalue)


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
    

def data_unfilter(win, statwin, df):
    """Display the complete dataset."""

    # print(f'in data_unfilter, locals are: {locals().keys()}')
    # print()

    # dfresult = df
    win.configure(state='normal')
    win.delete('1.0', tk.END)
    win.insert('1.0', df)
    win.tag_add('bluetext', '1.0', '1.end')

    stats_agg = data_current.agg(stats_dict)
    statwin.configure(state='normal')
    statwin.delete('1.0', tk.END)
    with pd.option_context('display.float_format', '{:0.2f}'.format):
        statwin.insert('1.0', stats_agg)

    style_df_text(statwin, stat_list)

    nvalue = 'n = ' + str(data_current.count().iloc[0])
    stat_n_lab.configure(text=nvalue)

    data_unfilter_btn.config(style = 'Opt2_on.TButton')
    data_filter_btn.config(style = 'MyButton1.TButton')

# func = data_unfilter
# print(f'in data_unfilter, __code__ params are:')
# print(f'    co_varnames: {func.__code__.co_varnames}')
# print(f'    co_argcount: {func.__code__.co_argcount}')
# print(f'    co_nlocals: {func.__code__.co_nlocals}')
# print()


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


def scatter_plot(df: pd.DataFrame, 
                 ent: object,
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

    # catlist = custui.value_list
    catlist = ent.value_list

    # print(f'   catlist: {catlist}')
    if catlist in [['auto'], ['']]:
        # user must have deleted the category list or 
        # entered 'auto'
        catlist = []


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
            # print('if category else...')
            df2[category] = pd.Categorical(df2[category], categories=catlist, ordered=False)    
            plot_data = df2[df2[category].isin(catlist)]
    else:
        plot_data = df2
        category = None

    create_plot(plot_data, category)
    plt.show()


# ===== END Functions =====
    

# print(f'pandas library: {pd.__version__}')
# print(f'pandas dependencies: {pd.show_versions()}')

# Module scope objects
# ====================
root = tk.Tk()
root.title = 'myocardial strain'

styles_ttk.CreateStyles()

category_values_ent = None

data_columns = ["gender", "age", "TID", "stress EF", "rest EF"]
line_data_source = 'age'
bar_data_source = 'TID'

x_text = 'x'
y_text = 'y'

data_current = None

# Read the dataset
# ================
# subset of 21 records
data_1 = pd.read_csv('data/strain_nml_sample.csv')

# entire 91 records, slightly different columns
# data_1 = pd.read_csv('data/strain_nml.csv')

data_1 = clean_column_names(data_1)
data_columns = list(data_1.columns)

# to update the display after filtering
data_current = data_1


# Display UI
# ==========
data_ui = ttk.Frame(root, border=2, relief='raised')

data_label = ttk.Label(data_ui, text='data:',
                       style='BoldLabel.TLabel')
data_label.pack(anchor='w')

data_win = tk.Text(data_ui, width=50, height=15,
                   background='beige',
                   foreground='black',
                   borderwidth=2,
                   relief='sunken',
                   name='datawin')

data_win.tag_configure("bluetext", foreground='blue')
data_win.tag_configure("redtext", foreground='red')

data_win.pack(padx=10, pady=5, fill='x', expand=True)

# data_win.insert('1.0', data_1)
data_win.insert('1.0', data_current)
data_win.configure(state='disabled')

# ("1.0 lineend" also works for end-of-line)
data_win.tag_add('bluetext', '1.0', '1.end')

data_scroll = ttk.Scrollbar(data_ui, orient='vertical', command=data_win.yview)
data_win.pack(side='left', pady=5, fill='x', expand=True)
data_scroll.pack(side='right', fill='y', pady=5)
data_win['yscrollcommand'] = data_scroll.set


# Statistics UI
# =============
# plusminus = u'\u00B1'

stat_ui = ttk.Frame(root, border=2, relief='raised')

stat_lab = ttk.Label(stat_ui, text='statistics:',
                     style='BoldLabel.TLabel')
stat_lab.pack(anchor='w')

stat_n_lab = ttk.Label(stat_ui, text='n')
stat_n_lab.pack(anchor='w', padx=10)

stat_win = tk.Text(stat_ui, width=50, height=10,
                     background='beige',
                     foreground='black',
                     font=('Courier New', 14),
                     borderwidth=2,
                     relief='sunken', name='statwin')

stat_scroll = ttk.Scrollbar(stat_ui, orient='vertical', command=stat_win.yview)
stat_win.pack(side='left', padx=10, pady=5, fill='x', expand=True)
stat_scroll.pack(side='right', fill='y', pady=5)
stat_win['yscrollcommand'] = stat_scroll.set

# for a good summary of skew and kurtosis, see medium.com
stat_list = ['mean', 'std', 'min', 'median', 'max', 'skew', 'kurtosis']

stats_dict = {}
for c in data_1.columns:
    if data_1[c].dtype == 'int64' or data_1[c].dtype == 'float64':
        # numeric_cols.append(c)
        stats_dict[c] = stat_list

# stats_agg = data_1.agg(stats_dict)
stats_agg = data_current.agg(stats_dict)

# get the number of data rows that have a 'pt code' (which is all of them):
# one way: the most succinct way that I can find, that uses a pandas function
# ...The chosen way, since for this data, column 1 is guaranteed to contain
# only real data, with no missing values.
# print(f'items in data_current: {data_current.count().iloc[0]}')

# a ssecond way: slightly more verbose
# print(f'items in data_current: {data_current.iloc[:, 0].count()}')

# a third way: depends on knowing the column header
# print(f'items in data_current: {data_current["pt_code"].count()}')

# a fourth way: simplest, does not use a pandas function
# print(f'items in data_current: {len(data_current)}')


nvalue = 'n = ' + str(data_current.count().iloc[0])
stat_n_lab.configure(text=nvalue)

# print('initial stats:')
# print(f'data_current is\n {data_current}')
# print(f'stat_win is {stat_win}')
# print(f'stats_agg is\n {stats_agg}')
# print()

# Format floating point values
# method 1: format for display but don't change the DataFrame
with pd.option_context('display.float_format', '{:0.2f}'.format):
    stat_win.insert('1.0', stats_agg)

# method 2: create a new DataFrame with formatted values
# stats_agg_format = stats_agg.map('{:0.2f}'.format)
# stat_win.insert('1.0', stats_agg_format)

# method 3: use the default styler object
# TODO

stat_win.tag_configure("bolded", font=('Courier New', 14, 'bold'))

style_df_text(stat_win, stat_list)


# Data filtering UI
# =================
filter_ui = ttk.Frame(root, border=2, relief='raised')

filter_fr = ttk.Frame(filter_ui, border=2, relief='groove')

filter_lab = ttk.Label(filter_ui, text='filter:',
                       style='BoldLabel.TLabel')
filter_lab.pack(anchor='w')

data_filter_btn = ttk.Button(filter_fr,
                        text='criteria:',
                        style='MyButton1.TButton',
                        command=lambda w=data_win, s=stat_win: data_filter(w, s))

data_filter_btn.pack(side='left', padx=5, pady=10)

filter_spec_fr = tk.Frame(filter_fr, border=4, bg='yellow')
filter_spec_fr.pack(side='left', padx=10, pady=10)

filt_rows = []
filt_vars = []
criterion_vars = []
filt_cboxes = []
filt_entries = []
filt_buttons_add = []
filt_buttons_subt = []

rowframe = create_criterion_row(data_win, stat_win)
filter_spec_fr.grid_propagate(True)

# print(f'cb     filt: {rowframe.winfo_children()[0]}')
# print(f'entry  crit: {rowframe.winfo_children()[1]}')
# print(f'button -: {rowframe.winfo_children()[2]}')
# print(f'button +: {rowframe.winfo_children()[3]}')
filt_rows.append(rowframe)

filt_cboxes.append(rowframe.winfo_children()[0])
filt_entries.append(rowframe.winfo_children()[1])
filt_buttons_subt.append(rowframe.winfo_children()[2])
filt_buttons_add.append(rowframe.winfo_children()[3])

# filt_rows[0].grid(row=0, column=0, sticky='nw')
rowframe.grid(row=0, column=0, sticky='nw')


# print(f'filt_rows[0] grid info: {filt_rows[0].grid_info()}')
# print(f'filt_rows[1] grid info: {filt_rows[1].grid_info()}')
# print(f'   items: {filt_rows[1].grid_info().items}')

data_unfilter_btn = ttk.Button(filter_ui,
                        text='show all data',
                        # style='MyButton2.TButton',
                        style='Opt2_on.TButton',
                        command=lambda w=data_win, s=stat_win, d=data_1: data_unfilter(w, s, d))
data_unfilter_btn.pack(side='bottom', pady=5)

filter_fr.pack(padx=10, pady=10, fill='both')


# plotting UI
# ===========
plot_label_fr = ttk.Frame(root, border=2, relief='raised')
plotting_label = ttk.Label(plot_label_fr, text='plotting:',
                           style='BoldLabel.TLabel')
plotting_main = ttk.Frame(plot_label_fr)
plotting_label.pack(anchor='w')

# ---------- Line plot
line_data_x = tk.StringVar()
line_data_y = tk.StringVar()

btn_line_plot = ttk.Button(plotting_main,
                text='Line plot',
                command=lambda df=data_1, x=line_data_x, y=line_data_y: line_plot(df, x, y))

line_x_fr = custui.FramedCombo(plotting_main,
                               cb_values=data_columns,
                               display_name=x_text,
                               name='line_x',
                               var=line_data_x,
                               posn=[0,1])

# print(f'line_x_fr doc: {line_x_fr.__doc__}')
# print()
# print(f'props:{line_x_fr.props()}')

line_y_fr = custui.FramedCombo(plotting_main,
                               cb_values=data_columns[2:],
                               display_name=y_text,
                               name='line_y',
                               var=line_data_y,
                               posn=[0,2])

# ---------- Bar plot
# bar_data = tk.StringVar(value=data_columns[2])
bar_data_x = tk.StringVar()
bar_data_y = tk.StringVar()

btn_bar_plot = ttk.Button(plotting_main,
               text='Bar plot',
               command=lambda df=data_1, x=bar_data_x, y=bar_data_y: bar_plot(df, x, y))

bar_x_fr = custui.FramedCombo(plotting_main,
                              cb_values=data_columns[1:],
                              display_name=x_text,
                              name='bar_x',
                              var=bar_data_x,
                              posn=[1,1])

bar_y_fr = custui.FramedCombo(plotting_main,
                              cb_values=data_columns[2:],
                              display_name=x_text,
                              name='bar_y',
                              var=bar_data_y,
                              posn=[1,2])

# ---------- Scatter plot
scatter_x = tk.StringVar()
scatter_y = tk.StringVar()

scatter_setup_fr = ttk.Frame(plotting_main, border=2, relief='groove')

category_values = 'auto'
category_values_ent = custui.MyEntry(scatter_setup_fr, 
                                     name='categories',
                                    #  text=cat_val_var)
                                     text=category_values)

test_ent = custui.MyEntry(scatter_setup_fr, 
                                     name='test_ent',                                    #  text=cat_val_var)
                                     text='arbitrary')

btn_scatter_plot = ttk.Button(plotting_main,
                   text='Scatter plot',
                   command=lambda df=data_1, ent=category_values_ent, x=scatter_x, y=scatter_y: scatter_plot(df, ent, x, y)
                   )

scatter_x_fr = custui.FramedCombo(plotting_main,
                               cb_values=data_columns[1:],
                               display_name=x_text,
                               name='scatter_x',
                               var=scatter_x,
                               posn=[2,1])

scatter_y_fr = custui.FramedCombo(plotting_main,
                               cb_values=data_columns[2:],
                               display_name=x_text,
                               name='scatter_y',
                               var=scatter_y,
                               posn=[2,2])

# scatter_setup_fr = ttk.Frame(plotting_main, border=2, relief='groove')

use_category = tk.IntVar(master=scatter_setup_fr, value = 0, name='use_category')
use_category_chkb = ttk.Checkbutton(scatter_setup_fr,
                                   text='Use category:',
                                   width=15,
                                   offvalue=0,
                                   variable=use_category,
                                   command=lambda n='use_category': set_use_category(n)
                                   )
                                #  style='MyCheckbutton.TCheckbutton')
use_category_chkb.bind('<Button-1>', chkb_extra)

category_list = ['', 'gender']
cat_var = tk.Variable(value=category_list)

category_lb= tk.Listbox(scatter_setup_fr,
                        exportselection=False,
                        height=2,
                        width=10,
                        listvariable=cat_var
                        )

category_lb.select_set(0)

# alternate way to load values to the Listbox category_lb. This may be the
# only way to number the list items.
# for ind, val in enumerate(category_list):
#     category_lb.insert(ind, val)

label_cat_list = tk.Label(scatter_setup_fr, text='with category values:')

# category_values = '(auto)'
# cat_val_var = tk.StringVar(value=category_values)
# category_values_ent = custui.MyEntry(scatter_setup_fr, 
#                                      name='categories',
#                                      text=cat_val_var)

use_category_chkb.grid(row=0, column=0, padx=5, sticky='w')

category_lb.grid(row=1, column=0, padx=5, pady=10, sticky='w')

label_cat_list.grid(row=0, column=1, padx=5, sticky='w')
category_values_ent.grid(row=1, column=1, padx=5, pady=5, sticky='w')
test_ent.grid(row=2, column=1, padx=5, pady=5, sticky='w')


# global UI
# =========
btnq = ttk.Button(root, text='Quit', command=root.destroy)
btnq.configure(style='MyButton1.TButton')


# grid the UI
# -----------
y_spacing = 5

# plotting
btn_line_plot.grid(row=0, column=0, padx=5, pady=y_spacing, sticky=tk.W)
btn_bar_plot.grid(row=1, column=0, padx=5, pady=y_spacing, sticky=tk.W)
btn_scatter_plot.grid(row=2, column=0, padx=5, pady=y_spacing, sticky=tk.W)
scatter_setup_fr.grid(row=3, column=0, columnspan=3, padx=5, pady=y_spacing)

plotting_main.pack(padx=5, pady=5, fill='both')

# main UI sections
data_ui.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
stat_ui.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
filter_ui.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
plot_label_fr.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

btnq.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# inspect functions in this module
# =================
if do_profile:
    import inspect
    import sys

    all_module_fxn = [obj for name, obj in inspect.getmembers(sys.modules[__name__]) 
                        if (inspect.isfunction(obj) and
                            obj.__module__ == __name__)]
    for f in all_module_fxn:
        print(f.__name__)
        # parameter names and type hints
        sig = (inspect.signature(f))
        print(f'   signature: {sig}')
    print()

root.mainloop()