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
from bokeh.models import ColumnDataSource

from datetime import datetime
import calendar

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

        dt = DataHandler.more_field(data)

        df = pd.DataFrame(data)

        df.record = pd.to_datetime(df.record)

        df['hour'] = df['record'].apply(lambda x: x.hour)

        timeData = df.groupby([pd.Grouper(key='record',freq='d'), df.passed]).size().reset_index(name='dailyCount')

        y = timeData["dailyCount"]
        
        x = timeData["record"]

        plot = figure(title="Daily", x_axis_label="Date",x_axis_type="datetime", y_axis_label="Number of Counts",plot_width=600,plot_height=600)
        
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
        script2,div2 = DataView.everyDay(dt)

        contents = {'script':script, 'div':div, 
        'script2': script2, 'div2':div2,
        'dailyAvg': y.mean(), 'dailyMax': y.max(), 'dailyMin': y.min()}

        return render_to_response(template_name, contents)

    def monthly(request):
        template_name = 'counter/data.html'

        data = DataHandler.get_mysql_data()

        df = DataHandler.more_field(data)

        timeData = df.groupby([pd.Grouper(key='record',freq='m'), df.passed]).size().reset_index(name='monthlyCount')

        y = timeData["monthlyCount"]
        
        x = df["Month"].unique()

        plot = figure(title="Monthly", x_axis_label="month",x_range=x ,y_axis_label="Number of Counts",plot_width=600,plot_height=600)        

        cr = plot.wedge(x=x, y=y, radius=15, start_angle=0.6,
           end_angle=4.1, radius_units="screen", color="#2b8cbe")

        plot.line(x,y,line_width=3)
    
        plot.scatter(x,y, marker="square", fill_color="red")

        # cr = plot.line(x,y,line_width=2)
        # cr = plot.hbar(y=y, height=0.2, left=0,
        #   x=x, color="navy", hover_fill_color="firebrick",
        #   hover_alpha=0.3, hover_line_color="white")

        plot.add_tools(HoverTool(tooltips=[
            ("month", "@x"),
            ("counter", "@y{int}"),
        ],
        renderers=[cr], mode='hline'))
        
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
            ("counter", "$y{int}"),
            ("time", "@x{%H:%M}"),
        ],formatters={'x': 'datetime'}, renderers=[cr], mode='hline'))

        return components(plot)

    def weekData(data, hrArray):
        hourlyCount = []
        for hr in hrArray:
            count = data[(data.hour == hr)]['passed'].count()
            hourlyCount.append(count)
        return hourlyCount
    def everyDay(df):
        
        lastweek = datetime.now().isocalendar()[1] -1 

        mon = df[(df.weekNumber == lastweek) &(df.weekday == 0)]
        tue = df[(df.weekNumber == lastweek) &(df.weekday == 1)]
        wed = df[(df.weekNumber == lastweek) &(df.weekday == 2)]
        thu = df[(df.weekNumber == lastweek) &(df.weekday == 3)]
        fri = df[(df.weekNumber == lastweek) &(df.weekday == 4)]


        xArray = []
        monHrArray = mon['hour'].unique()
        xArray.append(monHrArray)
        tueHrArray = tue['hour'].unique()
        xArray.append(tueHrArray)
        wedHrArray = wed['hour'].unique()
        xArray.append(wedHrArray)
        thuHrArray = thu['hour'].unique()
        xArray.append(thuHrArray)
        friHrArray = fri['hour'].unique()
        xArray.append(friHrArray)
        yArray = []
        monHourlyCount = DataView.weekData(mon, monHrArray)
        yArray.append(monHourlyCount)
        tueHourlyCount = DataView.weekData(tue, tueHrArray)
        yArray.append(tueHourlyCount)
        wedHourlyCount = DataView.weekData(wed, wedHrArray)
        yArray.append(wedHourlyCount)
        thuHourlyCount = DataView.weekData(thu, thuHrArray)
        yArray.append(thuHourlyCount)
        friHourlyCount = DataView.weekData(fri, friHrArray)
        yArray.append(friHourlyCount)


        mulData = {'xs': xArray,
                'ys': yArray,
                'legends': ['Monday', 'Tuesday', 'Wednesday','Thursday','Friday'],
                'colors': ['red', 'green', 'blue','purple','black']}

        source = ColumnDataSource(mulData)

        p = figure(title="Counts per day", x_axis_label='Time', y_axis_label='counts')

        cr = p.multi_line(xs='xs', ys='ys', legend='legends', color='colors', source=source)

        p.add_tools(HoverTool(tooltips=[
            ("time", "$x{int}"),
            ("counter", "$y{int}"),
            ("date", "@legends")
            ],
            renderers=[cr], mode='hline'))

        return components(p)
    def bestTimeForLunch(request):
        template_name = 'counter/hourly.html'

        selectedDateStart = '11:00'
        selectedDateEnd = '11:30'

        if(request.method == 'POST'):
            selectedDateStart = request.POST['hr_start'] +":"+ request.POST['min_start']
            selectedDateEnd = request.POST['hr_end'] +":"+ request.POST['min_end']
            if(request.POST['hr_start']>request.POST['hr_end']):
                err = "Sorry, Time setting in error, especially Hour, please take a look one more time"
            elif(request.POST['hr_start'] == request.POST['hr_end']):
                if(request.POST['min_start']>request.POST['min_end']):
                    err = "Sorry, Time setting in error, especially Minutes, please take a look one more time"
                elif(request.POST['min_start'] == request.POST['min_end']):
                    err = "Sorry, Time setting in error, same value settings, please take a look one more time"
            try:
                contents = {'err':err}
                return render_to_response(template_name, contents)
            except NameError:
                print(NameError)

        selectedDateStart = str(datetime.now().year)+"-"+str(datetime.now().month)+"-"+str(datetime.now().day)+" "+selectedDateStart+":00"
        selectedDateEnd = str(datetime.now().year)+"-"+str(datetime.now().month)+"-"+str(datetime.now().day)+" "+selectedDateEnd+":00"


        selectedDay = datetime.now().weekday()

        day = DataHandler.getDay(selectedDay)

        data = DataHandler.get_mysql_data()

        df = DataHandler.more_field(data)

        timeData = df[(df.weekday==selectedDay)].groupby([pd.Grouper(key='record',freq='10min'), df.passed, df.weekday, df.weekNumber]).size().reset_index(name='10MinCount')
        timeData['date'] = timeData.record.dt.strftime('%y-%m-%d')
        timeData['time'] = timeData.record.dt.strftime('%H:%M')

        if(len(timeData)==0):
            err = "Sorry, There is no any available data on selected date"
            contents = {'err':err}
            return render_to_response(template_name, contents)

        hoursArray = timeData.record.dt.strftime('%H:%M')

        fromTime = "2019-10-09 11:00:00"
        toTime = "2019-10-09 11:30:00"

        if selectedDateStart and selectedDateEnd:
            fromTime = selectedDateStart
            toTime = selectedDateEnd

        fromAsTime = datetime.strptime(fromTime, '%Y-%m-%d %H:%M:%S')
        toAsTime = datetime.strptime(toTime, '%Y-%m-%d %H:%M:%S')

        fromTime = fromAsTime.strftime('%H:%M')
        toTime = toAsTime.strftime('%H:%M')

        range = str(fromTime) + " - " + str(toTime)

        avgPer10Min = timeData.groupby('time', as_index=False)['10MinCount'].mean()

        minAvg, bestTime = 99999999,0
        x, y = [], []

        for index, row in avgPer10Min.iterrows():
            if row.time > fromTime and row.time < toTime:
                x.append(row.time)
                y.append(row["10MinCount"])
                if row["10MinCount"]<minAvg:
                    minAvg = row["10MinCount"]
                    bestTime = row.time
        
        chartTitle = str(range) +" " + str(day) + ", Average Counts"

        plot = figure(title=chartTitle, x_range = x, x_axis_label="Time / Hr:Min", y_axis_label="Number of Counts",plot_width=600,plot_height=600)

        plot.line(x,y,line_width=2)

        cr = plot.circle(x, y, size=20,
        fill_color="grey", hover_fill_color="firebrick",
        fill_alpha=0.4, hover_alpha=0.3,
        line_color="red", hover_line_color="white")
        plot.add_tools(HoverTool(tooltips=[
            ("counter", "$y{int}"),
            ("time", "@x"),
        ], renderers=[cr], mode='hline'))


        script,div = components(plot)

        contents = {
            'script':script, 'div':div,
            'range': range, 'day': day, 
            'bestTime': bestTime, 'counts':minAvg,
            'cam':True,}

        return render_to_response(template_name, contents)
    def hourly(request):
        template_name = 'counter/hourly.html'
        selectedDate = '2019-10-09'

        if(request.method == 'POST'):
            selectedDate = request.POST['date'] +" 00:00:00"

        selectedDate = datetime.strptime(selectedDate, "%Y-%m-%d %H:%M:%S")
        
        data = DataHandler.get_mysql_data()

        df = DataHandler.more_field(data)

        dt = df[(df['year']==int(selectedDate.year) ) & (df['month']== int(selectedDate.month) ) & (df['day']== int(selectedDate.day) )]

        if(len(dt)==0):
            err = "Sorry, There is no any available data on selected date"
            contents = {'err':err}
            return render_to_response(template_name, contents)

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
    def lunchTime(request):
        template_name = 'counter/lunchTime.html'
        return render(request, template_name)

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
        df['weekday'] = df['record'].dt.weekday.apply(lambda x: x )
        df['weekNumber'] = df['record'].dt.week.apply(lambda x: x )
        df['Month'] = df['month'].apply(lambda x: calendar.month_abbr[x])
        # df['date'] = df['record'].apply(lambda x: (x.day,x.month,x.year) )
        return df

    def getDay(weekday):
        if weekday == 0:
            return "Monday"
        elif weekday == 1:
            return "Tuesday"
        elif weekday == 2:
            return "Wednesday"
        elif weekday == 3:
            return "Thursday"
        elif weekday == 4:
            return "Friday"
        elif weekday == 5:
            return "Saturday"
        elif weekday == 6:
            return "Sunday"


