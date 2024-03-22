# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import views
from django.urls import path, re_path
# from .views import save_and_check_data
from .views import mongodb_test, save_to_mongo, find_in_mongo

urlpatterns = [
    # The home page
    # path('save_and_check_data/', save_and_check_data, name='save_and_check_data'),
    path('mongodb_test', views.mongodb_test, name='mongodb_test'),
    path('save_to_mongo', views.save_to_mongo, name='save_to_mongo'),
    path('find_in_mongo', views.find_in_mongo, name='find_in_mongo'),
    path('send_custom_data', views.send_custom_data, name='send_custom_data'),
    path('unique_id', views.unique_id, name='unique_id'),
    # path('extract_metadata', views.extract_metadata, name='extract_metadata'),
    path("", views.index, name="home"),
    path("imagetoText", views.imagetoText, name="imagetoText"),
    path("imagetoTextPan", views.imagetoTextPan, name="imagetoTextPan"),
    path("insertintoDatabase", views.insert_into_database, name="insertintoDatabase"),
    path("updateDatabase", views.update_database, name="updateDatabase"),
    path("verifyexists", views.verify_exists, name="verifyexists"),
    path("searchDatabase", views.search_database, name="searchDatabase"),
    path("deleterecord", views.delete_record, name="deleterecord"),
    path('autocomplete', views.AdharAutocomplete, name="adhar-autocomplete"),
    # path('kmsDataView', views.kmsDataView, name="kmsDataView"),

    path("selectText", views.select_text, name="selectText"),
    path("selectTextCropper", views.select_cropper, name="selectTextCropper"),
    path("selectionOCR", views.select_ocr, name="selectionOCR"),
    path("imageUpload", views.image_upload, name="imageUpload"),
    path("speechToText", views.speech_to_text, name="speechToText"),
    path("speechToTextNew", views.speech_to_text_new, name="speechToTextNew"),
    path("kms", views.KMS, name="kms"),
    path("myQueue", views.MyQueue, name="myQueue"),
    path("management", views.UserManagement, name="management"),
    path("dashboard", views.Dashboard, name="dashboard"),
    path("mahadiscomreg", views.mahadiscomreg, name="mahadiscomreg"),
    path("firform", views.fir, name="firform"),
    # Matches any html file
    re_path(r"^.*\.*", views.pages, name="pages"),
]
