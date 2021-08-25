# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

from django.db.models import CharField as C
from django.db.models import DateField as D
from django.db.models import IntegerField as I
from django.db.models import AutoField as A
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.contrib.auth.models import PermissionsMixin

class ApplicantManager(BaseUserManager):
    
    def create_user(self,uid,password):
        user = self.model(
            uid=uid,
            password=password
        )
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,uid,password):
        user = self.create_user(
            uid=uid,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Applicant(AbstractBaseUser,PermissionsMixin) :
    uuid = A(primary_key=True)

    email = models.CharField(max_length=200,unique=True)
    uid = models.CharField(max_length=200,unique=True)
    name = models.CharField(max_length=200)
    
    password = models.CharField(max_length=200,default="")

    applicant_type = models.CharField(max_length=100)
    applicant_agree_yn = models.CharField(max_length=20,default="")

    contact = C(max_length=100,default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)    
    is_admin = models.BooleanField(default=False)    
    is_superuser = models.BooleanField(default=False)    
    is_staff = models.BooleanField(default=False)     
    date_joined = models.DateTimeField(auto_now_add=True)     

    USERNAME_FIELD = 'uid'
    objects = ApplicantManager()

    @property
    def is_staff(self):
            return self.is_admin

class Application(models.Model):
    aid = A(primary_key=True)
    app_token = C(max_length=50,default="")
    
    app_user = C(max_length=200,default="")
    app_type = C(max_length=200,default="")
    
    isbn = C(max_length=100,default="")
    book_title = C(max_length=200,default="")
    
    author_name = C(max_length=200,default="")
    publisher_name = C(max_length=200,default="")

    accepted_yn = C(max_length=100,default="N")
    
    published_date = C(max_length=200,default="")
    price = I(default=0) 

    inquiries = C(max_length=300,default="")
    inquiries_info = C(max_length=300,default="")
    
    book_width = I(default=0)
    book_height = I(default=0)
    book_page_cnt = I(default=0)

    book_sales_cnt = I(default=0)

    book_detail = C(max_length=1000,default="")
    author_detail = C(max_length=1000,default="")
    publisher_detail = C(max_length=1000,default="")
    
    biz_no = C(max_length=300,default="")
    biz_document = C(max_length=300,default="")
     
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Notification(models.Model) :
    nid = A(primary_key=True)
    title = C(max_length=300)
    content = C(max_length=7000)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

