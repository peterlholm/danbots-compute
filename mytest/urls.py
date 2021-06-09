from django.urls import path
from mytest import views

urlpatterns = [
    path("", views.test),
    path("sendply/", views.sendply),
    path("sendpicture/", views.sendpicture),
    path('errorlog/', views.errorlog),
    path('upgrade/', views.upgrade)
]
