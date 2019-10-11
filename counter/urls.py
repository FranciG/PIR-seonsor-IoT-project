from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.show, name='index'),
    path('data/', views.DataView.show, name='data'),
    path('data/daily', views.DataView.daily, name='daily'),
    path('data/hourly', views.DataView.hourly, name='hourly'),
]