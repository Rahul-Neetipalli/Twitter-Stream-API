from django.urls import path
from . import views

app_name = 'twitter'

urlpatterns = [
    #/twitter/
    path('', views.index, name='index'),
    #/twitter/abc/
    path('abc/', views.api1, name='api1'),
    #/twitter/filter/
    path('filter/', views.redirect, name='redirect'),
    #/twitter/
    path('stop/', views.stopStream, name='stop'),
    #/twitter/result/
    path('result/', views.api2, name='api2'),
    #/twitter/sort/
    #path('sort/', views.sort, name='sort')

]
