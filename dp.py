from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, output_file, show, output_notebook
from bokeh.models.widgets import Select
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.io import output_file, show
from bokeh import models
import pandas as pd

d1 = dict(x=  [10,4,6,4], y =  [6,2,8,10])

d2 = dict(x=  [23,12,50,30], y =  [5,10,23,18,12])

source = ColumnDataSource(data=d1)

p = figure()

select = Select(title="Select d", value = " ", options=['d1', 'd2'])

def update_plot(attrname, old, new):
    if new == 'd1':
        newSource = d1

    if new == 'd2':
        newSource = d2


    source.data =  newSource
    print("Newsource:", newSource)
    print(source.data)

p.line(x='x', y='y',source = source)

select.on_change('value', update_plot)
layout = column(row(select, width=400), p)
curdoc().add_root(layout)
show(layout)