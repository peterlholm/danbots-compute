"""
URLs for NN
"""
from django.urls import path
from nn import views

urlpatterns = [
    path('', views.index),
    path('process_blender_testdata', views.process_blender_testdata),
    path('process_device_folder', views.process_device_folder),
    path('showresult', views.showresult),
    path('show_pictures', views.show_pictures),
]
 