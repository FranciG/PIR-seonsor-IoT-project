from django.shortcuts import render, render_to_response

from django.http import HttpResponseRedirect

from django.http import HttpResponse

from .models import Counter
import numpy as np
import pandas as pd

import io
from bokeh.embed import components
from bokeh.plotting import figure, output_file, show
from datetime import datetime

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

        df.record = pd.to_datetime(df.record)

        df['hour'] = df['record'].apply(lambda x: x.hour)

        timeData = df.groupby([pd.Grouper(key='record',freq='d'), df.passed]).size().reset_index(name='dailyCount')

        y = timeData["dailyCount"]
        
        x = timeData["record"]

        plot = figure(title="Daily", x_axis_label="Date",x_axis_type="datetime", y_axis_label="Number of Counts",plot_width=400,plot_height=400)
        
        plot.line(x,y,line_width=2)
        
        script,div = components(plot)

        return render_to_response(template_name,{'script':script, 'div':div})

    def every10Min(df, selectedDate):
        timeData = df.groupby([pd.Grouper(key='record',freq='10min'), df.passed]).size().reset_index(name='10MinCount')
        timeData['date'] = timeData.record.dt.strftime('%y-%m-%d')
        picked = str(selectedDate.year) + "-" + str(selectedDate.month) + "-" + str(selectedDate.day)
        hoursArray = timeData[(timeData['date'] == picked)].record.dt.strftime('%H:%M')
        counts = timeData[(timeData['date'] == picked)]['10MinCount']

        x = hoursArray
        y = counts
        
        plot = figure(title="Counts per Every 10 min", x_axis_label="Time / Hr:Min", y_axis_label="Number of Counts",plot_width=400,plot_height=400)
        
        plot.line(x,y,line_width=2)
        return components(plot)
    
    def hourly(request):
        template_name = 'counter/hourly.html'

        # df = DataView.get_data()

        selectedDate = '2019-10-09 00:00:00'

        if(request.method == 'POST'):
            selectedDate = request.POST['date'] + " 00:00:00"

        selectedDate = datetime.strptime(selectedDate, "%Y-%m-%d %H:%M:%S")
        
        data = DataHandler.get_mysql_data()

        df = DataHandler.more_field(data)

        dt = df[(df['year']==int(selectedDate.year) ) & (df['month']== int(selectedDate.month) ) & (df['day']== int(selectedDate.day) )]

        hrArray = dt['hour'].unique()
        hourlyCount = []

        for hr in hrArray:
            count = df[(df['year']==  int(selectedDate.year) ) & (df['month']== int(selectedDate.month) ) & (df['day']== int(selectedDate.day) ) & (df['hour']==hr )]['passed'].count()
            hourlyCount.append(count)

        x = hrArray
        y = hourlyCount

        chartTitle = dt.record.dt.strftime('%d-%m-%y').unique()[0] + " Hourly"

        plot = figure(title=chartTitle, x_axis_label="Hour", y_axis_label="Number of Counts",plot_width=400,plot_height=400)

        plot.line(x,y,line_width=2)

        script,div = components(plot)

        script2,div2 = DataView.every10Min(df, selectedDate)

        contents = {'script':script, 'div':div, 'script2':script2, 'div2':div2}

        return render_to_response(template_name, contents)

    def hourlyReq(request):
        template_name = 'counter/hourlyReq.html'
        return render(request, template_name)


    def get_data():
        data = list(Counter.objects.all().values())

        df = pd.DataFrame(data)
    
        return df


class DataHandler():
    def get_mysql_data():
        data = list(Counter.objects.all().values())
        return data

    def get_data():
        data = list(Counter.objects.all().values())

        df = pd.DataFrame(data)
    
        return df

    def more_field(data):
        df = pd.DataFrame(data)
        df.record = pd.to_datetime(df.record)
        df['hour'] = df['record'].apply(lambda x: x.hour)
        df['day'] = df['record'].apply(lambda x: x.day)
        df['month'] = df['record'].apply(lambda x: x.month)
        df['year'] = df['record'].apply(lambda x: x.year)
        # df['date'] = df['record'].apply(lambda x: (x.day,x.month,x.year) )
        return df


