from django.urls import path
from api import views

urlpatterns = [
    path('start3d', views.start3d),
    path('scan3d', views.scan3d),
    path('stop3d', views.stop3d),
    path('test3d', views.test3d),

]
