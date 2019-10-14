from django.shortcuts import render, render_to_response

from django.http import HttpResponseRedirect

from django.http import HttpResponse

from .models import Counter
import numpy as np
import pandas as pd

import io
from bokeh.embed import components
from bokeh.plotting import figure, output_file, show
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.models import HoverTool

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

        cr = plot.circle(x, y, size=20,
                fill_color="grey", hover_fill_color="firebrick",
                fill_alpha=0.4, hover_alpha=0.3,
                line_color="blue", hover_line_color="white")
        plot.add_tools(HoverTool(tooltips=[
            ("counter", "$y{int}"),
            ("date", "@x{%m/%d}"),
        ],formatters={'x': 'datetime'}, renderers=[cr], mode='hline'))
        
        script,div = components(plot)

        return render_to_response(template_name,{'script':script, 'div':div})

    def every10Min(df, selectedDate):
        timeData = df.groupby([pd.Grouper(key='record',freq='10min'), df.passed]).size().reset_index(name='10MinCount')
        timeData['date'] = timeData.record.dt.strftime('%y-%m-%d')

        selectedYr = str(selectedDate.year)[2:]

        if selectedDate.month<10:
            selectedMon = "0" + str(selectedDate.month)
        else:
            selectedMon = str(selectedDate.month)

        if selectedDate.day < 10:
            selectedDy = "0" + str(selectedDate.day)
        else:
            selectedDy = str(selectedDate.day)


        picked = selectedYr + "-" + selectedMon + "-" + selectedDy
        hoursArray = timeData[(timeData['date'] == picked)].record.dt.strftime('%H:%M')
        counts = timeData[(timeData['date'] == picked)]['10MinCount']

        minArray = []

        for min in hoursArray:
            minArray.append(datetime.strptime(min,"%H:%M"))

        x = minArray
        y = counts

        chartTitle = "Counts per Every 10 min"
        data = dict(counts=counts,time=hoursArray)

        plot = figure(title=chartTitle, x_axis_label="Time / Hr:Min", y_axis_label="Number of Counts",plot_width=600,plot_height=600)

        plot.line(x, y, line_dash="4 4", line_width=1, color='gray')

        plot.xaxis.formatter = DatetimeTickFormatter(days="%d-%b-%Y %H:%M:%S")

        cr = plot.circle(x, y, size=20,
                        fill_color="grey", hover_fill_color="firebrick",
                        fill_alpha=0.4, hover_alpha=0.3,
                        line_color="red", hover_line_color="white")
        plot.add_tools(HoverTool(tooltips=[
            ("counter", "$y"),
            ("time", "@x{%H:%M}"),
        ],formatters={'x': 'datetime'}, renderers=[cr], mode='hline'))

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

        plot = figure(title=chartTitle, x_axis_label="Time", y_axis_label="Number of Counts",plot_width=400,plot_height=400)

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


