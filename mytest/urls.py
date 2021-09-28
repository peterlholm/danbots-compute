"""
URLs for testing
"""

from django.urls import path
from mytest import views

urlpatterns = [
    path("", views.test),
    path("sendply/", views.sendply),
    path("start_scan/", views.start_scan),
    path("sendpicture/", views.sendpicture),
    path('errorlog/', views.errorlog),
    path('upgrade/', views.upgrade),
    path('flash_led/', views.flash_led)
]
