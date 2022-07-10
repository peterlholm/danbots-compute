"""
urls for the web
"""
from django.urls import path
from web import views

urlpatterns = [
    path('', views.index),
    path('show_set', views.show_set),
    path('calibratecamera', views.calibratecamera),
    path('distance', views.distance),
    path('pic_stream', views.pic_stream),
    path('pic_stream2', views.pic)
]
