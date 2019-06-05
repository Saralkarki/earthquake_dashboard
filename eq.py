import pandas as pd
import numpy as np

from bokeh.plotting import figure, show, ColumnDataSource, save, curdoc, output_file
from bokeh.layouts import column, row
from bokeh.models.tools import HoverTool
from bokeh.models.formatters import TickFormatter
from bokeh.layouts import widgetbox
from bokeh.models.widgets import CheckboxGroup, Dropdown, Select

def update_year_mag_plot(atrr, old, new):
    # see what years are active in selection
    years_active = [selections.labels[i] for i in selections.active]
    # print(years_active)
    # according to the years active the dataframe has to be formed
    new_df = df.loc[df['Year'].isin(years_active)]
    # get the active selections
    new_src = ColumnDataSource(new_df)
    src_1.data.update(new_src.data)

#bar plot for earthquake counts for each year
def update_barplot_eq_count(atrr,old,new):
    pass

def makedataframe():
    # For first plot (Earthquake and their magnitudes for each year)
    df = pd.read_csv('earthquake.csv')
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    # check if the conversion is done
    # # print(df['DateTime'].dtype)
    # assign a new column with just the year
    df['Year'] = df.DateTime.dt.year
    df['Date'] = df.DateTime.dt.date
    df['Date'] = pd.to_datetime(df['Date'])
    # Convert the date into format that can be shown correctly in the bokeh plot
    df["DateString"] = df["Date"].dt.strftime("%Y-%m-%d")
    df['Time'] = df.DateTime.dt.time
    # print(df.head())
    year = df["Year"]
    # For second plot (Earthquake count per year)
    df_1 = pd.DataFrame(df.Magnitude.groupby(df.Year).count())
    df_1['index'] = df_1.index
    df_1.columns = ["Count","year"]
    return df,df_1
    
df,df_1 = makedataframe()
src_1 = ColumnDataSource(df)

src_2 = ColumnDataSource(df_1)

#Plot the first graph with yearly earthquake and their magnitudes
def year_mag_plot(src):
    # Hover tool with vline mode
    hover = HoverTool(tooltips=[("Magnitude: ", "@Magnitude"), ("Epicenter: ", "@Epicenter"),
                                ("Date: ", "@DateString")
                                ], mode='vline')
    # Blank plot with correct labels
    p = figure(plot_width=700, plot_height=700,
               title='Yearly Earthquake with Magnitudes(1994-2014)',
               x_axis_label='Year', y_axis_label='Magnitude', tooltips=hover.tooltips,
               toolbar_location='below')

    # Quad glyphs to create a histogram
    p.circle(x='Year', y='Magnitude', size=10, color="navy",
             source=src_1, hover_fill_color='Magnitude')

    return p
#Selection for the first graph
years = list(range(1994, 2020))
years = list(map(str, years))
# the year_options can now be used as options for select as it is an array of string
selections = CheckboxGroup(labels=years, active=[
                           0,1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25])

# Graph the yearly earthquake with their magnitudes
def year_count_plot(src):
    # Hover tool with vline mode
    hover = HoverTool(tooltips=[("Count ", "@Count"),
                                ], mode='vline')
    # Blank plot with correct labels
    p = figure(plot_width=700, plot_height=700,
               title='Yearly Earthquake count(1994-2014)',
               x_axis_label='Year', y_axis_label='Count', tooltips=hover.tooltips,
               toolbar_location='below')

    # Quad glyphs to create a histogram
    p.vbar(x= 'year', width=0.5, bottom=0,top= 'Count', color="firebrick", source = src_2)
    

    return p
##########


plot_1 = year_mag_plot(src_1)
plot_2 = year_count_plot(src_2)
selections.on_change('active', update_year_mag_plot)
curdoc().add_root(column(row(plot_1, selections)))
curdoc().add_root(column(row(plot_2)))
