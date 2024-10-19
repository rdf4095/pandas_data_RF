# pandas_data_RF

PURPOSE
-------
This application reads csv data into a pandas data structure, then
provides a 4-panel interface to review the data.


DEPENDENCIES
------------
pandas       - data analysis library (external)
matplotlib   - data plotting library (external)

ui_RF        - custom user interface elements
styles_ttk   - custom ttk widget styles
tkinter      - may need to install, on linux


OPERATION
---------
Data display (panel 1, upper left)

   Standard display of pandas Dataframe, in a scrollable Text widget. Columns
    represent fields in the data, and rows are records. If filtered data is 
    displayed, the header row text will be red, to match the red text of the
    "criteria" button.

Statistics (panel 2, lower left)

   A table is displayed, containing the basic pandas statistics for all data
    columns. Statistics are updated automatically to reflect data filtering.

Data Filtering (panel 3, upper right)

   Rows of widgets to select the data column and criterion by which the
    data will be filtered. Rows can be added or removed using the "+" and "-"
    buttons, to filter by multiple columns. The "show all data" button revokes
    filters and displays all rows (records) in panel 1. Column headers revert
    to blue, to match the "show all data" button.

Plotting (panel 4, lower right)

   Line, bar and scatter plots are available for the data displayed in panel 1.
    X and Y axes are set using the Comboboxes. For scatter plots, a categorical
    variable can be defined. Categoricals are fields whose values are confined to
    a small list of values that define or categorize the data. For medical data, gender
    could be a categorical, and this is the default if you check the "use categorical"
    box, with "auto" as the value. Or, you can specify another categorical value, as
    a comma-separated list. For example, if your gender values include "U" for 
    "unknown", and you wish to exclude these records from the plot, enter "M,F" as
    the categorical value (without quotes.) To uses all values found in the dataset,
    including for this case the "U", leave the value at "auto".
