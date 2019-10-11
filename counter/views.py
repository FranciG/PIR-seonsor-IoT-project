from django.shortcuts import render, render_to_response

from django.http import HttpResponseRedirect

from django.http import HttpResponse

from .models import Counter
import numpy as np
import pandas as pd

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

    def daily(request):
        template_name = 'counter/data.html'

        data = list(Counter.objects.all().values())

        df = pd.DataFrame(data)

        df.record=pd.to_datetime(df.record)

        # df['hour'] = df['record'].apply(lambda x: x.hour)

        timeData = df.groupby([pd.Grouper(key='record',freq='d'), df.passed]).size().reset_index(name='dailyCount')

        y = timeData["dailyCount"]
        
        x = timeData["record"]

        plot = figure(title="Daily", x_axis_label="Date",x_axis_type="datetime", y_axis_label="Number of Counts",plot_width=400,plot_height=400)
        
        plot.line(x,y,line_width=2)
        
        script,div = components(plot)

        return render_to_response(template_name,{'script':script, 'div':div})

    def hourly(request):
        template_name = 'counter/hourly.html'

        df = DataView.get_data()

        df.record=pd.to_datetime(df.record)

        recordDates = df.record.dt.strftime('%d-%m-%y').unique()

        return render_to_response(template_name,{'dates':recordDates})

        # df = DataView.get_data()

        # df.record=pd.to_datetime(df.record)

        # timeData = df.groupby([pd.Grouper(key='record',freq='H'), df.passed]).size().reset_index(name='hourlyCount')

        # y = timeData["count"]

        # x = timeData["record"]

        # plot = figure(title="Daily", x_axis_label="Date",x_axis_type="datetime", y_axis_label="Number of Counts",plot_width=400,plot_height=400)

        # plot.line(x,y,line_width=2)

        # script,div = components(plot)

        # return render_to_response(template_name,{'script':script, 'div':div})

    def get_data():
        data = list(Counter.objects.all().values())

        df = pd.DataFrame(data)
    
        return df





