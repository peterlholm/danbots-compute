"""
urls for the api
"""
from django.urls import path
from api import views
from web.views import pic_stream

urlpatterns = [
    path('', views.index),
    path('start2d', views.start2d),
    path('save2d', views.save2d),
    path('stop2d', views.stop3d),
    path('start3d', views.start3d),
    path('scan3d', views.scan3d),
    path('stop3d', views.stop3d),
    path('sendfiles', views.sendfiles),
    path('pic_stream', pic_stream )
]
