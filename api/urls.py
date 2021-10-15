"""
urls for the api
"""
from django.urls import path
from api import views

urlpatterns = [
    path('', views.index),
    path('start2d', views.start2d),
    path('save2d', views.save2d),
    path('stop2d', views.stop3d),
    path('start3d', views.start3d),
    path('save3d', views.save3d),
    path('scan3d', views.scan3d),
    path('stop3d', views.stop3d),
    path('sendfiles', views.sendfiles),
    path('pic_stream2', views.pic_stream),
    path('pic_stream', views.pic)
]
