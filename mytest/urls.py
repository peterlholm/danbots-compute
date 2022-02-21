"""
URLs for testing
"""

from django.urls import path
from mytest import views

urlpatterns = [
    # indexes
    path("", views.index),
    path("debug", views.debug),
    path("test", views.test),

    # test steps
    path("inference/", views.inference),
    #path('show_folder_pictures', views.show_folder_pictures),
    path('show_pictures', views.show_pictures, name="show_pictures"),

    # mesh
    path("mesh/", views.mesh),
 
    # blender

    path("receiveblender", views.receive_blender, name="receiveblender"),
    path("receiveblender5", views.receive_blender5, name="receiveblender5"),
    path("showblender5", views.showblender5, name="showblender5"),

    # server debug

    #old


    path("show5/", views.show5),
    path("showset/", views.show_set),

    path("folder", views.rec_folder),
    path("folder5", views.rec_folder5),

    path('processfolder', views.process_folder_set),



    path("proc_scan", views.proc_scan),
    path("start_scan/", views.start_scan),
    path("calc_scan/", views.calc_scan),

    path("start_scan5/", views.start_scan5),
    path("calc5/", views.calc5),


    path("genstitch/", views.gen_stitch),
    path("stitchfolder/", views.stitch_folder),
    path("debug", views.debug),
    path("mytest", views.mytest),
    path("calibrate_camera", views.calibrate_camera),
    #path('showresult', views.showresult),

    path("sendply/", views.sendply),
    path("start_scan/", views.start_scan),
    path("install_models/", views.install_models),
    path("sendpicture/", views.sendpicture),
    path('errorlog/', views.errorlog),
    path('upgrade/', views.upgrade),
    path('flash_led/', views.flash_led)
]
