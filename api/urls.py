from django.urls import path
from api import views

urlpatterns = [
    path('start3d', views.start3d),
    path('save3d', views.save3d),
    path('scan3d', views.scan3d),
    path('stop3d', views.stop3d),
    path('test3d', views.test3d),

    path('start2d', views.start2d),
    path('save2d', views.save2d),
    path('stop2d', views.stop3d),

]
