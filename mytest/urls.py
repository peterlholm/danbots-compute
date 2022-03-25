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
    # show
    path('show_pictures', views.show_pictures, name="show_pictures"),
    path("showset/", views.show_set, name="show_set"),
    # device
    path("device", views.device_op),

    #process set
    path('processfolder', views.process_folder_set, name="process_folder_set"),
    # test steps
    path("inference/", views.inference),
    #path('show_folder_pictures', views.show_folder_pictures),


    # mesh
    path("mesh/", views.mesh),
    # blender
    path("receiveblender", views.receive_blender, name="receiveblender"),
    path("receiveblender5", views.receive_blender5, name="receiveblender5"),

    # server debug

    #old

    #stitch
    path("stitch_model/", views.stitch_model),
    path("genstitch/", views.gen_stitch),
    path("stitchfolder/", views.stitch_folder),


    path("folder", views.rec_folder),
    path("folder5", views.rec_folder5),

    path("proc_scan", views.proc_scan),
    path("start_scan/", views.start_scan),
    path("calc_scan/", views.calc_scan),

    path("start_scan5/", views.start_scan5),
    path("calc5/", views.calc5),


    path("debug", views.debug),

    path("calibrate_camera", views.calibrate_camera),
    #path('showresult', views.showresult),

    path("sendply/", views.sendply),
    path("start_scan/", views.start_scan),
    path("sendpicture/", views.sendpicture),
    path('errorlog/', views.errorlog),
    path('upgrade/', views.upgrade),
    path('flash_led/', views.flash_led)
]
