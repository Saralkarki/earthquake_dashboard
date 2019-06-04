import pandas as pd
import numpy as np

from bokeh.plotting import figure,show, ColumnDataSource,save,curdoc, output_file
from bokeh.layouts import column,row
from bokeh.models.tools import HoverTool
from bokeh.models.formatters import TickFormatter
from bokeh.layouts import widgetbox
from bokeh.models.widgets import CheckboxGroup, Dropdown, Select

#import the required file
df = pd.read_csv('earthquake.csv')

# define outfile_file
# output_file('test.html')

#check if imported 
# print(df.head())
#convert the Datetime to date type
df['DateTime'] = pd.to_datetime(df['DateTime'])
#check if the conversion is done
# print(df['DateTime'].dtype)

# assign a new column with just the year
df['Year'] = df.DateTime.dt.year
df['Date'] = df.DateTime.dt.date
df['Date'] = pd.to_datetime(df['Date'])
#Convert the date into format that can be shown correctly in the bokeh plot

df["DateString"] = df["Date"].dt.strftime("%Y-%m-%d")
df['Time'] = df.DateTime.dt.time
# print(df.head())
year = df["Year"]
#assign data to a source
source = ColumnDataSource(df)

#define the tools to show
tl = ['pan','zoom_in','zoom_out','reset','save']

#defining the info to be shown on hover

hover = HoverTool(
tooltips = [
    ("Magnitude: ", "@Magnitude"),
    ("Epicenter: ", "@Epicenter"),
    ("Date: ", "@DateString")
    ]
)
#scatterplot magnitudes of earthquake according to the year
p = figure(title="Earthquakes from 1994-2019", 
        x_axis_label = "Year", 
        y_axis_label = "Magnitude",
        tools =  tl ,
        tooltips = hover.tooltips,
        toolbar_location="below")
# selecting the options
# generate options of years using nupy arange functoin
year_options = list(range(1994,2020))
#change the options to string
year_options = list(map(str,year_options))
# the year_options can now be used as options for select as it is an array of string
year_select = Select(title="Year Select", options= year_options)

def update_plot(attrname, old, new):
    if new == '2015':
        new_df = pd.DataFrame()
        new_df = (df.loc[df['Year'] == 2015])
    if new == '2003':
        new_df = pd.DataFrame()
        #get the dataframe from only year 1994
        new_df = (df.loc[df['Year'] == 2003])
    # print("Previous label: " + old)
    # print("Updated label: " + new)
    # print("Attribute: " + attrname
    source = new_df
    p.circle(x = 'Year', y = 'Magnitude', size = 10 , color = "navy", source = source)
# p.circle(x = 'Year', y = 'Magnitude', size = 10 , color = "navy", source = source)
year_select.on_change('value', update_plot)



#Display the plot in a layout and add to document
layout = column(row(year_select, width=400), p)
curdoc().add_root(layout)
# curdoc().add_root(dropdown)

