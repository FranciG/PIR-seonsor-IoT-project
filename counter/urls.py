from django.urls import path

from . import views

app_name = 'counter'

urlpatterns = [
    path('', views.IndexView.show, name='index'),
    path('data/', views.DataView.show, name='data'),
    path('data/daily', views.DataView.daily, name='daily'),
    path('data/hourly', views.DataView.hourly, name='hourly'),
    path('data/hourlyReq', views.DataView.hourlyReq, name='hourlyReq'),
]