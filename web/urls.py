"""
urls for the web
"""
from django.urls import path
from web import views

urlpatterns = [
    path('', views.index),
    path('calibratecamera', views.calibratecamera),
    path('pic_stream', views.pic_stream),
    path('pic_stream2', views.pic)
]
