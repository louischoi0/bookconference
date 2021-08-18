# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path, include
from app import views

urlpatterns = [
    # The home page
    path('', views.index, name='home'),
    path('create', views.join, name='join'),
    path('postn', views.post_noti, name='post_noti'),
    path('postl', views.list_noti, name='list_noti'),
    path('postp/<int:postnum>/',views.page_noti, name='page_noti'),
    path('join', views.joinpage, name="page_join"),
    path('ulogin', views.ulogin, name="ulogin"),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
] 
