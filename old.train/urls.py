from django.urls import path
from train import views

urlpatterns = [
    path('showresult', views.showresult),
]
