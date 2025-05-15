# pandas_data_RF

## PURPOSE
This application reads csv data into a pandas data structure, then
provides a 4-panel interface for reviewing the data.


## DEPENDENCIES
- **pandas**       - data analysis library (external)
- **matplotlib**   - data plotting library (external)
- **ui_RF**        - custom user interface elements
- **styles_ttk**   - custom ttk widget styles
- **tkinter**      - may need to be installed, on some linux distributions


## OPERATION
### Data display (panel 1, upper left)

Tabular display of data items from the pandas Dataframe, in a scrollable Text 
widget. Columns represent fields in the data, and rows are records. 
If filtered data is displayed, the header row text will be red, to match the 
red text of the "criteria" button.

### Statistics (panel 2, lower left)

Tabular display of the basic set of descriptive statistics for all data 
columns. This includes: mean, standard deviation, minimum, median, maximum, skew and kurtosis.
Statistics are updated automatically to reflect data filtering.

### Data Filtering (panel 3, upper right)

Displays rows of widgets to select the data column and criterion by which the
data will be filtered. Rows can be added or removed using the "+" and "-"
buttons, to filter by multiple columns. There are two buttons that apply and remove
filters.
- **criteria**: filters the dataset according to all criteria set in panel 3. 
The data displayed in panel 1, and statistics in panel 2 are updated. The button text
changes to red, and the column header text in panel 1 changes to red, to indicate
that a filtered dataset is displayed.
- **show all data**: reverts to display of the complete dataset in panel 1, and
its statistics in panel 2. The column header text 
in panel 1 changes to blue, matching the "show all data" button, to indicate that 
the complete dataset is displayed. The "criteria" button changes to black. **Note**
that the filter criteria are not cleared in panel 3. This allows you to toggle between
filtered and unfiltered displays.

If the type of the data in the selected data column does not match the filter
criterion, a descriptive message will be printed on the status bar at the bottom
of the main window.

### Plotting (panel 4, lower right)

Controls graphical display of data and data relationships. Each graph is displayed 
in a new floating window, which persists until explictly closed. X and Y axis data
can be set separately for each type of graph. The types are:
- **Line**
- **Bar** 
- **Scatter**, with the following additional settings 
  - **use category**: chooses the categorical variable for grouping data. 
  Categoricals are fields whose values are confined to a small list of values 
  that define or categorize the data. In this dataset, 'gender' is the default
  categorical, but in some other dataset, there will be a list of categoricals
  displayed below the "use category" checkbox. 
  - **with category values**: 
  By default, the application uses all values of the categorical variable.  You
  can also specify the list of values to be found, as
  a comma-separated list. For the example of gender, if your gender values include
  "U" for "unknown", and you wish to exclude these records from the plot, 
  enter "M,F" as the categorical value list (without the quotes.)
  This will plot only data for which the gender value is M or F. To plot all
  data in the dataset, leave the value at "auto".
