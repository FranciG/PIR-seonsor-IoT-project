from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.views import generic
from django.http import HttpResponse
from .models import Counter
import numpy as np
import pandas as pd
from django_pandas.managers import DataFrameManager
from django.db import connection
import matplotlib.pyplot as plt
import matplotlib as mat
from plotly.offline import plot
import plotly.graph_objs as go
from matplotlib.backends.backend_agg import FigureCanvasAgg
import io
from bokeh.embed import components
from bokeh.plotting import figure, output_file, show
import datetime

class IndexView():
    def show(request):
        template_name = 'counter/index.html'
        return render(request, template_name)

class DataView():

    def show(request):
        template_name = 'counter/data.html'
        return render(request, template_name)

    def data_analysis1(request):
        template_name = 'counter/data-analysis1.html'

        data = list(Counter.objects.all().values())


        df = pd.DataFrame(data)

        df.record=pd.to_datetime(df.record)
        timeData = df.groupby([pd.Grouper(key='record',freq='H'), df.passed]).size().reset_index(name='count')


        df = pd.DataFrame(data)
        y = timeData["count"]
        x = timeData["record"]

        plot = figure(title="basic", x_axis_label="x",x_axis_type="datetime", y_axis_label="y",plot_width=400,plot_height=400)
        plot.line(x,y,line_width=2)
        script,div = components(plot)
        return render_to_response(template_name,{'script':script, 'div':div})

    def get_data():
        data = list(Counter.objects.all().values())
        df = pd.DataFrame(list(Counter.objects.all().values()))
        
        # data = Counter.objects.all()
        # context = {'data': data}

        # query = str(Counter.objects.all().query)
        # df = pd.read_sql_query(query, connection)

        return df

class StreamView():
    def show(request):
        template_name = 'counter/stream.html'
        return render(request, template_name)





