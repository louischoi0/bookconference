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
from django.db.utils import IntegrityError
from django.db.models import Max

from django.contrib.auth import authenticate, login

from app.forms import ApplicantForm, NotificationForm, ApplicationForm
from app.models import Applicant, Application, Application
from app.models import Notification

from django.db.models import Count

ADMIN_USER = "admin" #kpc5616

def app_detail(request,aid) :
    app = Application.objects.get(aid=aid)
    biz_img = f'images/a{aid}/img_0.jpg'
    pub_img = f'images/a{aid}/img_1.jpg'

    thumb_img = f'images/a{aid}/img_2.jpg'
    detail_img = f'images/a{aid}/img_3.jpg'

    context = { 'app' : app, "biz_img" : biz_img, "pub_img" : pub_img, "thumb_img" : thumb_img, "detail_img": detail_img }    

    if request.user.uid == ADMIN_USER :
        context["is_admin"] = True

    html_template = loader.get_template('appdetail.html')
    return HttpResponse(html_template.render(context, request))

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

@login_required(login_url="/login/")
def applications(request) :
    context = {}

    if request.user.uid == ADMIN_USER :
        context["is_admin"] = True

    if request.user.uid == ADMIN_USER:
        apps = Application.objects.all().order_by("-aid")
    else:
        apps = Application.objects.filter(app_user=request.user).order_by("-aid")
    context["apps"] = apps

    html_template = loader.get_template('applications.html')
    return HttpResponse(html_template.render(context, request))

def joinpage(request) :
    html_template = loader.get_template( 'join.html' )
    context = {}
    return HttpResponse(html_template.render(context, request))

def page_noti(request,postnum):
    noti = Notification.objects.get(pk=postnum)
    html_template = loader.get_template( 'notipage.html' )
    context = { "noti" : noti }
    if request.user.uid == ADMIN_USER :
        context["is_admin"] = True
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def list_user(request) :
    users = Applicant.objects.all()    
    is_admin = request.user.uid == 'admin'

    context = { "users" : users , "is_admin" : is_admin }

    html_template = loader.get_template( 'users.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def list_noti(request) :
    notis = Notification.objects.all().order_by("-created_at")
    context = {
            "notis" : notis,
            "is_admin" : request.user.uid == 'admin',
    }

    html_template = loader.get_template( 'notifications.html' )
    return HttpResponse(html_template.render(context, request))
    
def post_noti(request) :
    n = NotificationForm(request.POST)
    n.is_valid()

    n =  Notification(title=n.cleaned_data["title"], content=n.cleaned_data["content"])
    n.save()
    context = {}
    if request.user.uid == ADMIN_USER :
        context["is_admin"] = True
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

    if not "name" in form_data :
        context["no_name"] = "(이름 정보를 입력해 주세요.)"
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
    try :
        user = Applicant(**form_data)
        user.save()
    except IntegrityError:
        context["no_uid"] = "(이미 존재하는 아이디입니다.)"
        html_template = loader.get_template( 'join.html' )
        return HttpResponse(html_template.render(context,request))

    login(request, user)
    html_template = loader.get_template( 'notifications.html' )
    return HttpResponse(html_template.render(context,request))

@login_required(login_url="/login/")
def index(request):
    
    context = {}
    context['segment'] = 'index'
    if request.user.uid == ADMIN_USER :
        context["is_admin"] = True

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def app_submit(request) :
    context = {}
    if request.user.uid == ADMIN_USER :
        context["is_admin"] = True
    html_template = loader.get_template( 'submit.html' )
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

def handle_uploaded_file(f,aid,index):
    import os 

    try :
        os.mkdir(f"core/static/images/a{aid}")
    except :
        pass

    file_name = f"a{aid}/img_{index}.jpg"

    des = os.path.join("core/static/images/",file_name)
    destination = open(des, 'wb+')

    for chunk in f.chunks(): 
        destination.write(chunk)

    destination.close()
    return file_name




@login_required(login_url="/login/")
def post_submit(request) :
    app_form = ApplicationForm(request.POST) 
    app_form.is_valid()    
    context = {}
    
    app_data = app_form.cleaned_data

    columns = [ "app_type",
    "isbn",
    "book_title",
    "author_name",
    "publisher_name",
    "published_date", 
    "price", 
    "book_width",
    "book_height",
    "book_page_cnt",
    "book_sales_cnt",
    "book_detail",
    "author_detail",
    "publisher_detail" ] 

    print(request.POST)

    for c in columns :

        if request.POST[c] == "" :
            context = { "noti_msg" : f"{c} 필드를 입력해 주세요." }
            html_template = loader.get_template('submit.html')
            return HttpResponse(html_template.render(context, request))

    kw = { x : request.POST[x] if request.POST[x] else "0" for x in columns } 

    tnum = Application.objects.filter(app_type=kw['app_type']).aggregate(Count('aid'))
    c = tnum['aid__count'] + 1
    t = "일반" if kw['app_type'] == 'g' else '번역'
    token = f"{t}-{c}"

    app = Application(app_user=request.user,**kw,app_token=token)
    app.save()

    if 'biz_file'  in request.FILES:
        handle_uploaded_file(request.FILES['biz_file'],app.aid,0)

    if 'pub_file'  in request.FILES:
        handle_uploaded_file(request.FILES['pub_file'],app.aid,1)
    
    if 'thumb_file' in request.FILES:
        handle_uploaded_file(request.FILES['thumb_file'],app.aid,2)

    if 'detail_file' in request.FILES:
        handle_uploaded_file(request.FILES['detail_file'],app.aid,3)

    return redirect(reverse('app_list'))

@login_required(login_url="/login/")
def update_application(request,aid) :
    app_form = ApplicationForm(request.POST) 
    app_form.is_valid()    
    context = {}
    
    app_data = app_form.cleaned_data

    columns = [ "isbn","book_title","author_name","publisher_name","published_date", "price", "book_width","book_height","book_page_cnt","book_sales_cnt","book_detail","author_detail","publisher_detail" ] 

    kw = { x : request.POST[x] for x in columns } 
    app = Application.objects.get(aid=aid)

    for k in kw :
        v = kw[k]
        setattr(app,k,v)

    app.save()
    print(request.FILES)
    if 'biz_file'  in request.FILES:
        handle_uploaded_file(request.FILES['biz_file'],app.aid,0)

    if 'pub_file'  in request.FILES:
        handle_uploaded_file(request.FILES['pub_file'],app.aid,1)
    
    if 'thumb_file' in request.FILES:
        handle_uploaded_file(request.FILES['thumb_file'],app.aid,2)

    if 'detail_file' in request.FILES:
        handle_uploaded_file(request.FILES['detail_file'],app.aid,3)

    return redirect(reverse(f'app_list'))

@login_required(login_url="/login/")
def confirm(request,aid) :
    
    app = Application.objects.get(aid=aid)
    app.accepted_yn = "Y"
    app.save()
     
    return redirect(reverse('app_list'))


@login_required(login_url="/login/")
def delete_noti(request,nid) :

    noti = Notification.objects.get(nid=nid)
    noti.delete()

    return redirect(reverse('list_noti'))
