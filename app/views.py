# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.template import loader
from django.http import HttpResponse
from django import template
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from django.contrib.auth import authenticate, login

from app.forms import ApplicantForm, NotificationForm
from app.models import Applicant
from app.models import Post,Notification

def ulogin(request) :
    print(request.POST)
    username = request.POST['username']
    password = request.POST['password']

    try :
        user = Applicant.objects.get(uid=username,password=password) 
        login(request, user)
        return redirect(reverse('list_noti'))
    except Applicant.DoesNotExist :
        messages.error(request,"로그인 정보가 올바르지 않습니다.")
        return redirect('/login/')

def joinpage(request) :
    html_template = loader.get_template( 'join.html' )
    context = {}
    return HttpResponse(html_template.render(context, request))

def page_noti(request,postnum):
    noti = Notification.objects.get(pk=postnum)
    html_template = loader.get_template( 'notipage.html' )
    context = { "noti" : noti }
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def list_noti(request) :
    notis = Notification.objects.all()
    context = {
            "notis" : notis
    }

    html_template = loader.get_template( 'notifications.html' )
    return HttpResponse(html_template.render(context, request))
    
def post_noti(request) :
    n = NotificationForm(request.POST)
    n.is_valid()

    n =  Notification(title=n.cleaned_data["title"], content=n.cleaned_data["content"])
    n.save()
    return redirect(reverse('list_noti'))

def join(request) :
    if request.method != "POST" :
        return HttpResponse("For biden")

    form = ApplicantForm(request.POST)
    form.is_valid()

    form_data = form.cleaned_data
    print(form_data) 
    context = {}
    for k in form_data:
        key = "old_" + k
        context[key] = form_data[k] 
    
    if not "uid" in form_data:
        context["no_uid"] = "(아이디를 입력해 주세요.)"
        html_template = loader.get_template( 'join.html' )
        return HttpResponse(html_template.render(context, request))

    if (not "password" in form_data) or (not "password_check" in form_data):
        context["not_eq"] = "(비밀번호를 입력해 주세요.)"
        html_template = loader.get_template( 'join.html' )
        return HttpResponse(html_template.render(context, request))

    if not "contact" in form_data:
        context["no_contact"] = "(연락처를 입력해 주세요.)"
        html_template = loader.get_template( 'join.html' )
        return HttpResponse(html_template.render(context, request))

    if not "email" in form_data:
        context["no_email"] = "(이메일을 입력해 주세요.)"
        html_template = loader.get_template( 'join.html' )
        return HttpResponse(html_template.render(context,request))

    if form_data["password"] != form_data["password_check"]:
        context["not_eq"] = "(비밀번호가 동일하지 않습니다.)"
        html_template = loader.get_template( 'join.html' )
        return HttpResponse(html_template.render(context,request))
    
    del form_data["password_check"]
    print(form_data)
    Applicant(**form_data).save()
    return HttpResponse("ok")

@login_required(login_url="/login/")
def index(request):
    
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))
