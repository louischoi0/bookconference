# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

from django.db.models import CharField as C
from django.db.models import DateField as D
from django.db.models import IntegerField as I
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

class ApplicantManager(BaseUserManager):
    
    def create_user(self,uid,password):
        user = self.model(
            uid=uid,
            password=password
        )
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


# Create your models here.
class Applicant(AbstractBaseUser) :
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

    def get_by_natural_key(self, uid):
        return self.get(uid=uid)

    def has_module_perms(self, app_label):
            return True

    @property
    def is_staff(self):
            return self.is_admin

class Application(models.Model):
    applicant_type = C(max_length=200)
    
    isbn = C(max_length=100)
    book_title = C(max_length=200)
    
    author_name = C(max_length=200)
    publisher_name = C(max_length=200)
    
    published_1st_date = C(max_length=200)
    price = I() 
    
    book_width = I()
    book_height = I()
    book_page_cnt = I()

    book_sales_cnt = I()

    book_feature = C(max_length=1000) 
    author_intro = C(max_length=1000)
    publisher_intro = C(max_length=1000)
    
    biz_no = C(max_length=300)
    biz_document = C(max_length=300)
     
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



