from django.urls import path
from nn import views

urlpatterns = [
    path('', views.index),
    path('process_testdata', views.process_testdata),
    path('showresult', views.showresult),
]
 