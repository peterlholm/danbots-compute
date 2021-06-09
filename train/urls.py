from django.urls import path
from train import views

urlpatterns = [
    path('', views.index),
    path('showresult', views.showresult),
]
