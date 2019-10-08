from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from django.http import HttpResponse
from .models import Counter
import numpy as np
import pandas as pd
from django_pandas.managers import DataFrameManager
from django.db import connection
import matplotlib.pyplot as plt

class IndexView():
    def show(request):
        template_name = 'counter/index.html'
        return render(request, template_name)

class DataView():

    def show(request):
        data = Counter.objects.all()
        context = {'data': data}

        query = str(Counter.objects.all().query)
        df = pd.read_sql_query(query, connection)
        template_name = 'counter/data.html'
        ts = pd.Series(df)
        ts = ts.cumsum()
        ts.plot()
        return render(request, template_name)

class StreamView():
    def show(request):
        template_name = 'counter/stream.html'
        return render(request, template_name)





