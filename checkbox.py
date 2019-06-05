import pandas as pd
import numpy as np

from bokeh.plotting import figure,show, ColumnDataSource,save,curdoc, output_file
from bokeh.layouts import column,row
from bokeh.models.tools import HoverTool
from bokeh.models.formatters import TickFormatter
from bokeh.layouts import widgetbox
from bokeh.models.widgets import CheckboxGroup, Dropdown, Select

df = pd.read_csv('earthquake.csv')
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
def make_plot(src):
    # Hover tool with vline mode
        hover = HoverTool(tooltips = [("Magnitude: ", "@Magnitude"),("Epicenter: ", "@Epicenter"),
                                    ("Date: ", "@DateString")
        ], mode = 'vline')
        # Blank plot with correct labels
        p = figure(plot_width = 700, plot_height = 700, 
                  title = 'Yearly Earthquake and their magnitudes',
                  x_axis_label = 'Year', y_axis_label = 'Magnitude',tooltips = hover.tooltips)

        # Quad glyphs to create a histogram
        p.circle(x = 'Year', y = 'Magnitude', size = 10 , color = "navy", source = source, hover_fill_color = 'Magnitude')

        return p

years = list(range(1994,2020))
years = list(map(str,years))
# the year_options can now be used as options for select as it is an array of string

selections = CheckboxGroup(labels= years , active = [])

# update the graph function
def update(atrr,old,new):
    # see what years are active in selection
    years_active = [selections.labels[i] for i in selections.active]
    # print(years_active)

    #according to the years active the dataframe has to be formed
    new_df = df.loc[df['Year'].isin(years_active)]
    # get the active selections
    new_src = ColumnDataSource(new_df)
    source.data.update(new_src.data)

plot = make_plot(source)
selections.on_change('active', update)
curdoc().add_root(column(row(plot, selections)))
