from django.urls import path
from nn import views

urlpatterns = [
    path('', views.index),
    path('process', views.process),
    path('showresult', views.showresult),
]
