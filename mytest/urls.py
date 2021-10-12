"""
URLs for testing
"""

from django.urls import path
from mytest import views

urlpatterns = [
    path("", views.debug),
    path("debug", views.debug),
    path("calibrate_camera", views.calibrate_camera),

    path("sendply/", views.sendply),
    path("start_scan/", views.start_scan),
    path("install_models/", views.install_models),
    path("sendpicture/", views.sendpicture),
    path('errorlog/', views.errorlog),
    path('upgrade/', views.upgrade),
    path('flash_led/', views.flash_led),
    path('stream/', views.pic_stream),
    path("include_masks/", views.include_masks)
]
