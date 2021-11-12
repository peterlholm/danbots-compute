"""
URLs for testing
"""

from django.urls import path
from mytest import views

urlpatterns = [
    path("", views.debug),
    path("receiveblender", views.receive_blender),
    path("receiveblender5", views.receive_blender5),
    path("folder", views.rec_folder),
    path("proc_scan", views.proc_scan),
    path("start_scan/", views.start_scan),
    path("start_scan5/", views.start_scan5),
    path("calc5/", views.calc5),
    path("calc5/", views.show5),

    path("debug", views.debug),
    path("calibrate_camera", views.calibrate_camera),
    #path('showresult', views.showresult),
    path('show_pictures', views.show_pictures),

    path("sendply/", views.sendply),
    path("start_scan/", views.start_scan),
    path("install_models/", views.install_models),
    path("sendpicture/", views.sendpicture),
    path('errorlog/', views.errorlog),
    path('upgrade/', views.upgrade),
    path('flash_led/', views.flash_led)
]
