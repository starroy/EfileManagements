# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import views
from django.urls import path, re_path

urlpatterns = [
    # The home page
    path("", views.index, name="home"),
    path("imagetoText", views.imagetoText, name="imagetoText"),
    path("imagetoTextPan", views.imagetoTextPan, name="imagetoTextPan"),
    path("insertintoDatabase", views.insert_into_database, name="insertintoDatabase"),
    path("updateDatabase", views.update_database, name="updateDatabase"),
    path("verifyexists", views.verify_exists, name="verifyexists"),
    path("searchDatabase", views.search_database, name="searchDatabase"),
    path("deleterecord", views.delete_record, name="deleterecord"),

    path("selectText", views.select_text, name="selectText"),
    path("selectTextCropper", views.select_cropper, name="selectTextCropper"),
    path("selectionOCR", views.select_ocr, name="selectionOCR"),
    path("imageUpload", views.image_upload, name="imageUpload"),
    path("speechToText", views.speech_to_text, name="speechToText"),
    path("speechToTextNew", views.speech_to_text_new, name="speechToTextNew"),
    # Matches any html file
    re_path(r"^.*\.*", views.pages, name="pages"),
]
