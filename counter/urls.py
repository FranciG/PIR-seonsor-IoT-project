from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.show, name='index'),
    path('data/', views.DataView.show, name='data'),
    path('data/ex', views.DataView.data_analysis1, name='data-analysis1'),
    path('stream/', views.StreamView.show, name='stream'),
]