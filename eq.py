import pandas as pd
import numpy as np
import geopandas as gpd
import shapely

from bokeh.plotting import figure, show, ColumnDataSource, save, curdoc, output_file
from bokeh.layouts import column, row
from bokeh.models.tools import HoverTool
from bokeh.models.formatters import TickFormatter
from bokeh.layouts import widgetbox
from bokeh.models import CheckboxGroup, Dropdown, Select, Panel, Tabs

from bokeh.transform import factor_cmap, factor_mark
from bokeh.palettes import Category10,Plasma256,Spectral6

def update_year_mag_plot(atrr, old, new):
    # see what years are active in selection
    years_active = [selections.labels[i] for i in selections.active]
    # print(years_active)
    # according to the years active the dataframe has to be formed
    new_df = df.loc[df['Year'].isin(years_active)]
    # get the active selections
    new_src = ColumnDataSource(new_df)
    src_1.data.update(new_src.data)

def update_eq_map(atrr, old, new):
    # see what years are active in selection
    years_active = [selections_1.labels[i] for i in selections_1.active]
    # eq_class = pass
    # print(years_active)
    # according to the years active the dataframe has to be formed
    new_df = df.loc[df['Year'].isin(years_active)]
    # get the active selections
    new_src = ColumnDataSource(new_df)
    # print(years_active)
    src_3.data.update(new_src.data)

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
    # Add magnitude category to the dataframe
    size_class = []
    for magnitude in df.Magnitude:
        if magnitude >= 3.0 and magnitude <=3.9:
            size_class.append("Minor")
        elif magnitude >=4.0 and magnitude <=4.9:
            size_class.append("Light")
        elif magnitude >=5.0 and magnitude <=5.9:
            size_class.append("Moderate")
        elif magnitude >=6.0 and magnitude <=6.9:
            size_class.append("Strong")
        elif magnitude >=7.0 and magnitude <=7.9:
            size_class.append("Major")
        else:
            size_class.append("Great")
    df['size_class'] = size_class
    # For second plot (Earthquake count per year)
    df_1 = pd.DataFrame(df.Magnitude.groupby(df.Year).count())
    df_1['index'] = df_1.index
    df_1.columns = ["Count","year"]
    #inital dataframe to plot the Nepal Nepal
    df_2 = df.loc[df['Year']== 2015]
    
    return df,df_1,df_2

#make the dataframes  
df,df_1,df_2 = makedataframe()
#convert the df to ColumnDataSource
src_1 = ColumnDataSource(df)
src_2 = ColumnDataSource(df_1)
src_3 = ColumnDataSource(df_2)

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
             source=src, hover_fill_color='Magnitude')
    p.title.text_color = "black"
    p.title.text_font = "helvetica"
    p.title.text_font_style = "italic"
    tab = Panel(child=p, title="Earthquake and their Magnitude(1994-2014)")
    p.title.text_font_size = '16pt'

    return p,tab
#categories for the earthquakes
eq_type = ['Minor','Light','Moderate','Strong','Major','Great']
#Selection for the first graph
years = list(range(1994, 2020))
years = list(map(str, years))
# the year_options can now be used as options for select as it is an array of string
selections = CheckboxGroup(labels=years, active=[
                           0,1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25])
selections_1 = CheckboxGroup(labels=years, active=[21])
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
    p.vbar(x= 'year', width=0.5, bottom=0,top= 'Count', color="firebrick", source = src)
    tab = Panel(child=p, title="Earthquake count from 1994-2014")
    p.title.text_color = "black"
    p.title.text_font = "helvetica"
    p.title.text_font_style = "italic"
    p.title.text_font_size = '16pt'

    return p,tab

def plot_eq_map(src):
    hover = HoverTool(tooltips=[("Magnitude: ", "@Magnitude"), ("Epicenter: ", "@Epicenter"),
                                ("Date: ", "@DateString")
                                ])
    p = figure(plot_width=800, plot_height=500,
               title='Earthquakes in Nepal (1994-2014)',
               tooltips=hover.tooltips,
               toolbar_location='below')
    #loading the shape file
    map_nepal = gpd.read_file('NPL_adm/NPL_adm3.shp')
    #mapping the shape file
    x, y = [], []
    [(x.append(list(polygon.exterior.coords.xy[0])), y.append(list(polygon.exterior.coords.xy[1]))) for polygon in map_nepal['geometry'] if type(polygon.boundary) == shapely.geometry.linestring.LineString ]
    p.patches('x', 'y', source = ColumnDataSource(dict(x = x, y = y)), line_color = "white", line_width = 0.5)
    for category,color in zip(eq_type,Spectral6):
        p.circle(x='Long', y='Lat', size=10,source=src, legend = category, fill_alpha = 0.5,
             color = color)
    p.legend.location = "top_right"
    p.legend.click_policy="mute"
    p.axis.visible = False
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.border_fill_color = 'white'
    p.background_fill_color = 'black'
    p.outline_line_color = None
    p.grid.grid_line_color = None
    p.title.text_color = "black"
    p.title.text_font = "helvetica"
    p.title.text_font_style = "italic"
    p.title.text_font_size = '16pt'
    tab = Panel(child=p, title="Earthquakes based on their epicenters (1994-2014)")

    return p,tab

    
##########



def callback():
    plot_1, tab_1 = year_mag_plot(src_1)
    plot_2, tab_2 = year_count_plot(src_2)
    plot_3, tab_3 = plot_eq_map(src_3)
    tabs = Tabs(tabs=[ tab_1, tab_2 ,tab_3])
    selections.on_change('active', update_year_mag_plot)
    selections_1.on_change('active', update_eq_map)
    curdoc().add_root(column(row(tabs)))
    # curdoc().add_root(column(row(plot_1, selections)))
    # curdoc().add_root(column(row(plot_2)))
    # curdoc().add_root(column(row(plot_3,selections_1)))
callback()
