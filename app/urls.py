# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path, include
from app import views

urlpatterns = [
    # The home page
    path('', views.applications, name='home'),
    path('create', views.join, name='join'),
    path('postn', views.post_noti, name='post_noti'),
    path('postl', views.list_noti, name='list_noti'),
    path('postp/<int:postnum>/',views.page_noti, name='page_noti'),
    path('join', views.joinpage, name="page_join"),
    path('ulogin', views.ulogin, name="ulogin"),
    path('submit', views.app_submit, name="app_submit"),

    path('applications', views.applications, name="app_list"), #내공모
    path('users',views.list_user,name='list_user'),

    path('apply', views.post_submit, name="post_submit"),
    path('update/<int:aid>/',views.update_application, name="app_update"),

    path('appdetail/<int:aid>/',views.app_detail, name="app_detail"),
    path('confirm/<int:aid>/',views.confirm, name="confirm"),

    path('noti_delete/<int:nid>/', views.delete_noti, name="delte_noti"),


    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
] 
