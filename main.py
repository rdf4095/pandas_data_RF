"""
program: main.py

purpose: basic operations with pandas library

comments: For Combobox and Listbox, exportselection=False is needed. Without this, 
          using the combo will clear the Listbox, generating a new ListboxSelect
          event with no content (an error).
          
          Pyarrow will become a required dependency of pandas in the next major 
          release of pandas (pandas 3.0)

author: Russell Folks

history:
-------
11-29-2023  creation

...see: main_history.txt...

06-07-2024  Add apply_filter(), needed for future programmatic filter.
06-11-2024  Bug fix: if data query expression is empty, don't call filter.
            Remove some comments. Reformat scatter plot UI section.
06-15-2024  Rename some vars in the plotting section. Slightly reconfigure
            gridding of the scatterplot objects.
06-19-2024  Remove data_filter_ORIG() to not_used.py. Trim history.
06-21-2024  Refine logic for validating filter criterion.
06-25-2024  Pass filt_rows (list of frames w/ filter widgets) to data_filter().
            In make_filter(), use var 'err' so as not to return from within
            the body of an 'if'.
06-27-2024  Implement status bar for user messages.
07-02-2024  Implement do_debug flag. When set, print() variable values.
            Bug fix: pass needed arguments to data_filter() if a rowframe
            is deleted.
07-04-2024  Allow filter to match a simple string w/o using the '==' operator.
07-05-2024  Make parameter names and order consistent for filter functions,
            and plotting functions.
07-09-2024  Handle spurious characters in the data filter criterion. e.g. for
            age >= 55, handle the typo 'g' in age >= g55.
            Auto-get function name for debug print statements. See do_debug.
            Move (almost) all prints to 'if do_debug' blocks in each fxn.
07-15-2024  For all functions that access the two data display windows (Text
            widgets) pass one dict of the two objects, not separate objects.
07-21-2024  Refine data filter to handle mismatched filter and data types.
            Initial implementation of multi-select UI as an external module.
            This is code that was previously in this module, and will be
            removed after debug.
            multi-select = rows of frames, each with drop-down list and buttons.
10-19-2024  Delete UI code that was moved to an external module. Add flag 
            'use_pandas' to have UI code limit the number of filters to
            the number of data columns.
            Update some variable names to use UI code that is more generic.
            Changed: filt_rows (to item_rows), filt_vars (to item_vars),
            filter_spec_fr (to main_list_fr).
            Import UI module using SourceFileLoader.
            Update associated README.md file.
04-09-2025  Use ThemedTk for the root window (cleaner widget appearance.)
04-11-2025  Remove background show-through around main_filter_fr object.
04-24-2025  Add alpha=0.5 to scatter plot, so overlying points are more apparent.
04-28-2025  Add a plot title, showing the flter and "n= ".
05-02-2025  Debug scatter_plot() to handle category with filtered data. Remove
            data parameter from plotting functions: always use data_current.
05-07-2025  In data_filter(), properly report filter error on the status bar.
            For data_unfilter(), reset status bar to empty (remove any error).
            For filter criterion, report unknown single-character operator.
05-15-2025  Refactor make_filter() to verify the filter parameters using new:
            functions set_criterion() and check_filter_data().
06-16-2025  Use the Entry attribute value_list to get the category list.
            Disable some print statements.
06-20-2025  Use ListEntry instead of MyEntry for criteria list.
06-21-2025  Re-init err when constructing a filter from rows of MultiSelectFrames.
06-24-2025  Update error messages for erroneous filters.
"""
"""
TODO:
    1. Variable names
      a. Make names consistent in code.
      b. add a header comment section explaining abbreviations used for variable
         and function names.
    2. Use tkinter.font to control multiple Labels and other objects.
      a. use custom '+' character for buttons in the filter section.
    3. Update README to explain how combination of valid & invalid filtes
       are handled.
"""

import tkinter as tk
from tkinter import ttk
from importlib.machinery import SourceFileLoader

# only used by the debug flag: to get function name and caller
import sys

from ttkthemes import ThemedTk
import pandas as pd
import matplotlib.pyplot as plt

# msel = SourceFileLoader("ui_multi_select", "../ui_RF/ui_multi_select.py").load_module()
msel = SourceFileLoader("msel", "../utilities/tool_classes.py").load_module()
styles_ttk = SourceFileLoader("styles_ttk", "../styles/styles_ttk.py").load_module()

do_debug = False      # print statements for debug
do_profile = False    # report function signatures

""" 
----------------------------
widget interaction functions
----------------------------
"""
def style_df_text(win: object, itemlist: list=['test']) -> None:
    """Apply text styling to a pandas DataFrame displayed in a Text widget."""
    win.tag_add('bolded', '1.0', '1.end')

    for e in range(2, len(itemlist) + 2):
        row = str(format(e, '0.1f'))
        strend = row + ' wordend'
        win.tag_add('bolded', row, strend)

    win.configure(state='disabled')


def set_use_category(varname: str) -> None:
    """Checkbutton callback: for scatter plot, use/don't use categories.
    
    Selects a row in the corresponding Listbox.
    """
    do_cat = use_category.get()
    do_cat_test = scatter_setup_fr.getvar(name=varname)

    if int(do_cat) == 1:
        print('selecting category from list...')
        category_lb.select_clear(0)
        category_lb.select_set(1)
    else:
        category_lb.select_clear(1)
        category_lb.select_set(0)

    if do_debug:
        print(f'in function: {sys._getframe().f_code.co_name}')
        print(f'...called by: {sys._getframe().f_back.f_code.co_name}')
        print(f'   do_cat: {do_cat}')
        print(f'   do_cat_test: {do_cat_test}')


def chkb_extra(ev):
    # print('in chkb_extra...')
    # print(f'   ev: {ev}')
    pass

def set_status(status_msg):
    # print('in set_status...')
    status_txt.set(status_msg)


""" 
--------------------------
data interaction functions
--------------------------
"""
def clean_column_names(df: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
    """Convert single spaces in column names to underscore character."""

    cols0 = df.columns
    cols1 = cols0.map(lambda x: x.replace(' ', '_') if isinstance(x, str) else x)
    df.columns = cols1

    return df


def data_filter(data: pd.core.frame.DataFrame, 
                windows: dict,
                filters: list) -> None:
    """Manage the construction and implementation of a dataset filter."""
    # global data_current
    global filter_summary

    expr = make_filter(data, filters)

    if expr not in [-1, -2, -3, -4, -5]:
        nvalue = str(data.count().iloc[0])
        # do more to the string?

        expr_display = expr.replace('==', '=')
        filter_summary = expr_display
        # apply_filter(data, expr, windows)
        report_filter(expr)
        apply_filter(data, expr, windows)
    else:
        # if expr == -2:
        #     data_unfilter(data, windows)
        data_unfilter(data, windows)
        report_filter(expr)


def make_filter_orig(data: pd.core.frame.DataFrame, filt_rows: list) -> int | str:
    """Construct a data filter for a pandas DataFrame.
    module variables
    """
    dcolumn = []
    criteria = []
    terms = []

    # define these in check_criterion()
    err = 0  # False == no error
    # quote = ''

    q_expression = ''
    current_term = ''

    for i in range(len(filt_rows)):

        this_filter = filt_rows[i].winfo_children()[0].get()
        this_criterion = filt_rows[i].winfo_children()[1].get()

        if this_filter != '' and this_criterion != '':
            quote = ''
            dcolumn.append(this_filter)
            criteria.append(this_criterion)

            crit_number = len(criteria) - 1
            valid_criterion = set_criterion(criteria[crit_number])

            # the_op = valid_criterion['op']
            # the_value = valid_criterion['value']

            data_type = data[this_filter].dtype

            if valid_criterion['value'] != '':
                # test for numeric value.
                # ...int or float will pass
                if valid_criterion['value'].replace('.', '', 1).isnumeric():
                # if the_value.replace('.', '', 1).isnumeric():
                    if data_type == 'object':
                        err = -4
                    quote = ''
                else:
                    # value to check is not numeric, see if data is numeric
                    if data_type == 'int64' or data_type == 'float64':
                        err = -3
                    quote = '\"'
            else:
                err = -1
                print(f'not valid criterion: {this_criterion}')

            quoted_value = quote + valid_criterion['value'] + quote
            current_term = dcolumn[crit_number] + valid_criterion['op'] + quoted_value

            terms.append(current_term)

    if len(terms) == 0:
        # No filter defined
        err = -2

    if do_debug:
        print(f'in function: {sys._getframe().f_code.co_name}')
        print(f'...called by: {sys._getframe().f_back.f_code.co_name}')
        print(f'filt, crit: {this_filter}, {this_criterion}')
        print()
        print(f'column {this_filter} contains type: {data_type}')
        print(data_type in ['str', 'object', 'int64'])
        print(f'q_expression string: {repr(q_expression)}')
        print()

    if err:
        print(f'make_filter, returning _{err}_')

        return err
    else:
        for t in terms:
            q_expression += (t + ' & ')
        q_expression = q_expression[:-3]
        print(f'make_filter, returning {q_expression}')

        return q_expression


def make_filter(data: pd.core.frame.DataFrame, filt_rows: list) -> int | str:
    """Construct a data filter for a pandas DataFrame.
    module variables
    """
    dcolumn = []
    criteria = []
    terms = []

    err = 0  # False == no error

    q_expression = ''
    current_term = ''

    for i in range(len(filt_rows)):

        this_filter = filt_rows[i].winfo_children()[0].get()
        this_criterion = filt_rows[i].winfo_children()[1].get()
        valid_criterion = ''

        if this_filter == '':
            err = -1

        if this_criterion == '':
            err += -2
        else:
            valid_criterion = set_criterion(this_criterion)

        print(f'{err=}, {valid_criterion=}')

        if err == 0:
            # quote = ''
            dcolumn.append(this_filter)
            criteria.append(this_criterion)

            crit_number = len(criteria) - 1

            data_type = data[this_filter].dtype
            # print(f'data is {data[this_filter]}')

            filter_check = check_filter_data(valid_criterion['value'], data_type)

            # if filter_check['err'] == -3:
            #     quote = '\"'
            if filter_check['err'] == 0:
                quote = filter_check['quote']
                quoted_value = quote + valid_criterion['value'] + quote
                current_term = dcolumn[crit_number] + valid_criterion['op'] + quoted_value

                terms.append(current_term)
                # print(f'{current_term=}')
            else:
                err = filter_check['err']
        # print(f'    {terms=}')
        # err = 0

    if do_debug:
        print(f'in function: {sys._getframe().f_code.co_name}')
        print(f'...called by: {sys._getframe().f_back.f_code.co_name}')
        print(f'filt, crit: {this_filter}, {this_criterion}')
        print()
        print(f'column {this_filter} contains type: {data_type}')
        print(data_type in ['str', 'object', 'int64'])
        print(f'q_expression string: {repr(q_expression)}')
        print()

    if err and terms == []:
        print(f'make_filter, returning _{err}_')

        return err
    else:
        for t in terms:
            q_expression += (t + ' & ')
        q_expression = q_expression[:-3]
        print(f'make_filter, returning {q_expression}')
        # report nonfatal error
        if err == -2:
            report_filter(err)

        return q_expression


def set_criterion(inp: list) -> dict:
    """Validate user-entered criterion for filtering data."""
    op = ''
    value = ''

    # this definition is not required...
    criterion = {'op': op,
                 'value': value}

    char1 = inp[0]
    if len(inp) > 1:
        char2 = inp[1]
    else:
        char2 = ''

    if char1 in ['!', '=', '>', '<']:
        if char2 == '=':
            value = inp[2:]
            op = inp[0:2]
        else:
            value = inp[1:]
            match char1:
                case '!':
                    op = '!='
                case '=':
                    op = '=='
                case _:
                    op = char1
    else:
        op = '=='
        value = inp

    criterion['op'] = op
    criterion['value'] = value

    if do_debug:
        print(f'in function: {sys._getframe().f_code.co_name}')
        print(f'...called by: {sys._getframe().f_back.f_code.co_name}')
        print(f'vallidate input: {inp}')
        print()
        print(f'char1, char2: {char1}, {char2}')
        if char1 not in ['!', '=', '>', '<']:
            print(f'setting filter criterion to: ' == ' {value}')
        print(f'validated op, value: {op}, {value}')
        print('---------')
        print()

    return criterion


def check_filter_data(value, data_type):
    """Check for mismatch between data type and the filter criterion."""
    data_status = {'err': 0, 'quote': ''}

    # ...int or float will pass this test
    if value.replace('.', '', 1).isnumeric():
        if data_type == 'object':
            data_status['err'] = -4
    else:
        # value to check is not numeric, see if data is numeric
        if data_type == 'int64' or data_type == 'float64':
            data_status['err'] = -5
        data_status['quote'] = '\"'

    return data_status


def report_filter(res):
    match res:
        case -1:
            # in the current case, this should not happen.
            set_status('Data item not specified.')
        case -2:
            # valid and invalid filter rows
            set_status('At least one invalid filter criterion.')
        case -3:
            set_status('No filter defined.')
        case -4:
            # e.g. 'gender' + '>55'
            set_status("Can\'t compare numeric filter to string data.")
        case -5:
            # e.g. 'age' + 'older'
            set_status("Can\'t compare filter string to numeric data.")
        case _:
            set_status('ok')


def apply_filter(data: pd.core.frame.DataFrame,
                 expr: str, 
                 windows: dict) -> None:
    """Apply a data filter to a pandas DataFrame.

    The query() function requires cleaning column names. Another method
    is to use a series of terms like: df[col] > 55.
    """
    global data_current
    data_current = data.query(expr)
    show_filtered(data_current, windows)
    

def show_filtered(data: pd.core.frame.DataFrame, 
                  windows: dict) -> None:
    """Display results of filtering a dataset."""
    windows["data"].configure(state='normal')
    windows["data"].delete('1.0', tk.END)
    windows["data"].insert('1.0', data)
    windows["data"].tag_add('redtext', '1.0', '1.end')
    windows["data"].configure(state='disabled')

    stats_agg = data.agg(stats_dict)
    windows["stats"].configure(state='normal')
    windows["stats"].delete('1.0', tk.END)
    with pd.option_context('display.float_format', '{:0.2f}'.format):
        windows["stats"].insert('1.0', stats_agg)

    style_df_text(windows["stats"], stat_list)

    nvalue = 'n = ' + str(data.count().iloc[0])
    stat_n_lab.configure(text=nvalue)

    data_filter_btn.configure(style='MyButton2.TButton')

    if data.empty:
        set_status('No data found.')


def data_unfilter(data: pd.core.frame.DataFrame, 
                  windows: dict) -> None:
    """Display the complete dataset."""
    global data_current

    data_current = data
    windows["data"].configure(state='normal')
    windows["data"].delete('1.0', tk.END)
    windows["data"].insert('1.0', data)
    windows["data"].tag_add('bluetext', '1.0', '1.end')
    windows["data"].configure(state='disabled')

    stats_agg = data_current.agg(stats_dict)
    windows["stats"].configure(state='normal')
    windows["stats"].delete('1.0', tk.END)
    with pd.option_context('display.float_format', '{:0.2f}'.format):
        windows["stats"].insert('1.0', stats_agg)

    style_df_text(windows["stats"], stat_list)

    nvalue = 'n = ' + str(data_current.count().iloc[0])
    stat_n_lab.configure(text=nvalue)
    # print(f'{nvalue=}')
    data_unfilter_btn.configure(style = 'MyButton3.TButton')
    data_filter_btn.configure(style = 'MyButton1.TButton')

    set_status('')

    if do_debug:
        print(f'in function: {sys._getframe().f_code.co_name}')
        print(f'...called by: {sys._getframe().f_back.f_code.co_name}')
        print(f'locals are: {locals().keys()}')
        func = data_unfilter
        print(f'    co_varnames: {func.__code__.co_varnames}')
        print(f'    co_argcount: {func.__code__.co_argcount}')
        print(f'    co_nlocals: {func.__code__.co_nlocals}')
        print()


def line_plot(data: pd.DataFrame,
              xcol: tk.StringVar,
              ycol: tk.StringVar) -> None:
    """Create line plot (the default) for the current dataset."""
    xdata = xcol.get()
    ydata = ycol.get()
    sorted = data.sort_values(by=xdata)

    # ? or use data.plot.line for explicitness
    sorted.plot(x=xdata, y=ydata)
    plt.show()

    if do_debug:
        print(f'in function: {sys._getframe().f_code.co_name}')
        print(f'...called by: {sys._getframe().f_back.f_code.co_name}')
        print('line_plot params:')
        print(f'   xcol: {xcol} = {xdata}')
        print(f'   ycol: {ycol} = {ydata}')
        print()


def bar_plot(data: pd.DataFrame,
             xcol: tk.StringVar,
             ycol: tk.StringVar) -> None:
    """Create bar plot for the current dataset."""

    xdata = xcol.get()
    ydata = ycol.get()
    dfsort = data.sort_values(by=xdata)

    dfsort.plot.bar(x=xdata, y=ydata)
    plt.show()

    if do_debug:
        print(f'in function: {sys._getframe().f_code.co_name}')
        print(f'...called by: {sys._getframe().f_back.f_code.co_name}')
        print('bar_plot params:')
        print(f'   xcol: {xcol} = {xdata}')
        print(f'   ycol: {ycol} = {ydata}')
        print()


def create_plot(data, source, cat):
    """Execute the scatter plot."""
    if cat is None:
        clr = "#00aaaa"
    else:
        clr = cat
    data.plot.scatter(x=source['x'],
                      y=source['y'],
                      c=clr,
                      cmap='viridis',
                      alpha=0.5,
                      s=40)


def scatter_plot(data: pd.DataFrame,
                 ent: object,
                 x_variable: tk.StringVar,
                 y_variable: tk.StringVar) -> None:
    """Create scatter plot for the current dataset.
    
    Makes a copy of the DataFrame object passed in, to avoid mutating it.
    """
    global data_current

    data_copy = pd.DataFrame(data_current)
    # print(f'data_current:\n{data_current}')
    # print(f'data_copy:\n{data_copy}')
    # print(f'data:\n{data}')
    # print()

    source = {'x': x_variable.get(),
              'y': y_variable.get()}

    category = category_lb.get(category_lb.curselection())

    # a catlist value of 'auto' is a mnemonic for the user
    # catlist = category_values_entry.get()
    # catlist = ent.get()
    catlist = ent.value_list

    # if the user deletes the category list or manually enters 'auto'
    if catlist in ['auto', ['']]:
        catlist = []
    # else:
        # must be a list
        # pass
        # catlist = catlist.strip().split(',')

    if category != '':
        # if not catlist: print('not catlist')
        # if ((not catlist) or catlist == None or (not isinstance(catlist, list))):
        if ((not catlist) or (not isinstance(catlist, list))):
            print('\nWARNING: no category list; finding category values...\n')
            data_copy[category] = data_copy[category].astype('category')
            plot_data = data_copy
        else:
            # print(f'{catlist=}')
            # print(f'data_copy:\n{data_copy}')
            # print(f'\n{category=}')
            data_copy[category] = pd.Categorical(data_copy[category], categories=catlist, ordered=False)
            plot_data = data_copy[data_copy[category].isin(catlist)]
    else:
        plot_data = data_copy
        category = None

    # print(f'plot_data:\n{plot_data}')
    create_plot(plot_data, source, category)
    number_of_points = str(data_current.count().iloc[0])

    if filter_summary == '':
        mytitle = 'All Data ' + ' (n = ' + number_of_points + ')'
    else:
        mytitle = filter_summary + ' (n = ' + number_of_points + ')'
    plt.title(mytitle)
    plt.show()


# ===== END Functions =====
    

# print(f'pandas library: {pd.__version__}')
# print(f'pandas dependencies: {pd.show_versions()}')

# Module scope objects
# ====================
# root = tk.Tk()
root = ThemedTk()
root.title = 'myocardial strain'

styles_ttk.create_styles()

# flag for external module(s)
use_pandas = True

category_values_entry = None

data_columns = ["gender", "age", "TID", "stress EF", "rest EF"]
line_data_source = 'age'
bar_data_source = 'TID'

# text widgets
windows = {'data': None,
           'stats': None}

x_text = 'x'
y_text = 'y'

# Read the dataset
# ================
# subset of 21 records
data_0 = pd.read_csv('data/strain_nml_sample.csv')

# entire 91 records, slightly different columns
# data_1 = pd.read_csv('data/strain_nml.csv')

data_1 = clean_column_names(data_0)
data_columns = list(data_1.columns)

# to update the display after filtering
data_current = data_1


# Data Display UI
# ===============
data_ui = ttk.Frame(root, border=2, relief='raised')
# data_ui = ttk.Frame(root, style='alt.TFrame')

data_label = ttk.Label(data_ui, text='data:',
                       style='BoldLabel.TLabel')
data_label.pack(anchor='w')

data_win = tk.Text(data_ui, width=50, height=15,
                   background='beige',
                   foreground='black',
                   borderwidth=2,
                   relief='sunken',
                   name='datawin')
windows["data"] = data_win

data_win.tag_configure("bluetext", foreground='blue')
data_win.tag_configure("redtext", foreground='red')
data_win.tag_add('bluetext', '1.0', '1.end')

data_win.insert('1.0', data_current)
data_win.configure(state='disabled')

data_win.pack(side='left', pady=5, fill='x', expand=True)

data_scroll = ttk.Scrollbar(data_ui, orient='vertical', command=data_win.yview)
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
windows["stats"] = stat_win

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

# get the number of rows in the data that have a 'pt code' (are valid records):
# method 1: the chosen method, the most succinct way I can find that uses
# a pandas function. Makes 2 assumptions, both of which are true for the
# present use case:
#   - 'pt code' is in column 1
#   -  all rows (records) have a 'pt code' -- no missing values.
# print(f'items in data_current: {data_current.count().iloc[0]}')

# method 2: does the count() a different way
# print(f'items in data_current: {data_current.iloc[:, 0].count()}')

# method 3: doesn't assume column 1, and so needs the column header ('pt code'), 
# which could be passed in if this is a function. This is more generic,
# print(f'items in data_current: {data_current["pt_code"].count()}')

# method 4: simple, does not use a pandas function
# print(f'items in data_current: {len(data_current)}')

nvalue = 'n = ' + str(data_current.count().iloc[0])
stat_n_lab.configure(text=nvalue)

# Format floating point values
# method 1: format for display but don't change the DataFrame
with pd.option_context('display.float_format', '{:0.2f}'.format):
    stat_win.insert('1.0', stats_agg)

# method 2: create a new DataFrame with formatted values.
# Preserves stats for the whole dataset, for possible later conparison to
# stats for a filtered dataset.
# stats_agg_format = stats_agg.map('{:0.2f}'.format)
# stat_win.insert('1.0', stats_agg_format)

stat_win.tag_configure("bolded", font=('Courier New', 14, 'bold'))

style_df_text(stat_win, stat_list)


# Data filtering UI
# =================
# filt_rows = []
# filt_vars = []
# ? don't need this
# item_rows = []
item_vars = []

criterion_vars = []

# ? don't need these:
filt_cboxes = []
filt_entries = []
filt_buttons_add = []
filt_buttons_subt = []

filter_ui = ttk.Frame(root, border=2, relief='raised')

filter_fr = ttk.Frame(filter_ui, border=2, relief='groove')

filter_lab = ttk.Label(filter_ui, text='filter:',
                       style='BoldLabel.TLabel')
filter_lab.pack(anchor='w')

# main_list_fr = tk.Frame(filter_fr, border=4)
# main_list_fr = ttk.Frame(filter_fr, border=4, style='test.TFrame')

# border=0 prevents the background color from showing around the object
main_list_fr = ttk.Frame(filter_fr, border=0)
# print(f'main_list_fr background: {main_list_fr.configure()}')
main_list_fr.pack(side='right', padx=10, pady=10)

my_fxn = data_filter

rowframe = msel.init_selection_row(main_list_fr, data_columns, '', use_pandas, windows)
main_list_fr.grid_propagate(True)

# ? don't need this
# item_rows.append(rowframe)

# ? don't need these:
filt_cboxes.append(rowframe.winfo_children()[0])
filt_entries.append(rowframe.winfo_children()[1])
filt_buttons_subt.append(rowframe.winfo_children()[2])
filt_buttons_add.append(rowframe.winfo_children()[3])

# rowframe.grid(row=0, column=0, sticky='nw')

data_filter_btn = ttk.Button(filter_fr,
                        text='criteria:',
                        style='MyButton1.TButton',
                        command=lambda d=data_1,
                                       w=windows,
                                       # f=item_rows: data_filter(d, w, f))
                                       f=rowframe.item_rows: data_filter(d, w, f))
data_filter_btn.pack(side='left', padx=5, pady=10)

data_unfilter_btn = ttk.Button(filter_ui,
                        text='show all data',
                        style='MyButton3.TButton',
                        command=lambda d=data_1, 
                                       w=windows: data_unfilter(d, w))
data_unfilter_btn.pack(side='bottom', pady=5)

filter_fr.pack(padx=10, pady=10, fill='both')

# try: 04-22-2025
filter_summary = ''

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
                text='Line',
                command=lambda df=data_current, x=line_data_x, y=line_data_y: line_plot(df, x, y))

line_x_fr = msel.ComboboxFrame(plotting_main,
                               cb_values=data_columns,
                               display_name=x_text,
                               name='line_x',
                               var=line_data_x,
                               width=10,
                               posn=[1,0]
                               )

# print(f'line_x_fr doc: {line_x_fr.__doc__}')
# print()
# print(f'props:{line_x_fr.props()}')

line_y_fr = msel.ComboboxFrame(plotting_main,
                               cb_values=data_columns[2:],
                               display_name=y_text,
                               name='line_y',
                               var=line_data_y,
                               width=10,
                               posn=[2,0]
                               )

# ---------- Bar plot
# bar_data = tk.StringVar(value=data_columns[2])
bar_data_x = tk.StringVar()
bar_data_y = tk.StringVar()

btn_bar_plot = ttk.Button(plotting_main,
               text='Bar',
               command=lambda df=data_current, x=bar_data_x, y=bar_data_y: bar_plot(df, x, y))

bar_x_fr = msel.ComboboxFrame(plotting_main,
                              cb_values=data_columns[1:],
                              display_name=x_text,
                              name='bar_x',
                              var=bar_data_x,
                              width=10,
                              posn=[1, 1]
                              )

bar_y_fr = msel.ComboboxFrame(plotting_main,
                              cb_values=data_columns[2:],
                              display_name=y_text,
                              name='bar_y',
                              var=bar_data_y,
                              width=10,
                              posn=[2, 1]
                              )

# ---------- Scatter plot
scatter_x = tk.StringVar()
scatter_y = tk.StringVar()

scatter_setup_fr = ttk.Frame(plotting_main, border=2, relief='groove')

category_values = 'auto'
category_values_entry = msel.ListEntry(scatter_setup_fr,
                                       name='categories',
                                       text=category_values
                                       )


scatter_select_fr = ttk.Frame(scatter_setup_fr)

scatter_plot_btn = ttk.Button(scatter_select_fr,
                   text='Scatter',
                   width=6,
                   command=lambda df=data_current, ent=category_values_entry, x=scatter_x, y=scatter_y: scatter_plot(df, ent, x, y)
                   # command=lambda ent=category_values_entry, x=scatter_x, y=scatter_y: scatter_plot(ent, x, y)
                   )

scatter_x_fr = msel.ComboboxFrame(scatter_select_fr,
                                  cb_values=data_columns[1:],
                                  display_name=x_text,
                                  name='scatter_x',
                                  var=scatter_x,
                                  width=10,
                                  posn=[1, 0]
                                  )

scatter_y_fr = msel.ComboboxFrame(scatter_select_fr,
                                  cb_values=data_columns[2:],
                                  display_name=y_text,
                                  name='scatter_y',
                                  var=scatter_y,
                                  width=10,
                                  posn=[2, 0]
                                  )

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

scatter_select_fr.grid(row=0, column=0, columnspan=3, pady=10)

use_category_chkb.grid(row=1, column=0,   padx=20,         sticky='w')
category_lb.grid(row=2, column=0,         padx=20, pady=10, sticky='w')
label_cat_list.grid(row=1, column=1,      padx=0,         sticky='w')
category_values_entry.grid(row=2, column=1, padx=0, pady=10, sticky='w')


# test object placement on the UI
# test_ent = custui.MyEntry(scatter_setup_fr, 
#                           name='test_ent',                                    #  text=cat_val_var)
#                           text='arbitrary')

# test
# print(f'MyEntry name attr = {category_values_ent.name}')

# test_ent.grid(row=3, column=1, padx=5, pady=5, sticky='w')


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

scatter_setup_fr.grid(row=2, column=0, columnspan=3, padx=5, pady=y_spacing,
                      ipadx=5, ipady=5)

scatter_plot_btn.grid(row=0, column=0, padx=5, sticky=tk.W)

plotting_main.pack(padx=5, pady=5, fill='both')

# status bar
# ----------
status_fr = ttk.Frame(root, relief='groove')
status_lab = ttk.Label(status_fr, text='status: ')

status_txt = tk.StringVar()
status_bar = ttk.Label(status_fr, textvariable=status_txt)

status_lab.pack(side='left', padx=3, pady=3)
status_bar.pack(side='left', padx=3, pady=3, expand=True, fill='both')


# main UI sections
data_ui.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
stat_ui.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
filter_ui.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
plot_label_fr.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

status_fr.grid(row=2, column=0, columnspan=2, padx=5, sticky='ew')

btnq.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# inspect functions in this module
# =================
if do_profile:
    import inspect

    all_module_fxn = [obj for name, obj in inspect.getmembers(sys.modules[__name__]) 
                        if (inspect.isfunction(obj) and
                            obj.__module__ == __name__)]
    for f in all_module_fxn:
        print(f.__name__)
        # parameter names and type hints
        sig = (inspect.signature(f))
        print(f'   signature: {sig}')
    print()

if __name__ == "__main__":
    root.mainloop()
