from django import forms
from django.forms import CharField as C
from django.forms import IntegerField as I

class NotificationForm(forms.Form):
    title = C(max_length=300)
    content = C(max_length=7000)

class ApplicantForm(forms.Form):
    uid = forms.CharField(label='uid', max_length=200,required=True)
    password = forms.CharField(label='password', max_length=200,required=True)
    password_check = forms.CharField(label='password_check', max_length=200,required=True)
    
    name = C(label='name',max_length=100)
    email = C(label='email',max_length=100)

    contact = C(label='contact',max_length=100)

    applicant_type = C(label='applicant_type', max_length=20)
    applicant_agree_yn = C(label='applicant_type', max_length=20)

class ApplicationForm(forms.Form):
    app_type = C(label="app_type",max_length=20)
    
    isbn = C(label='isbn',max_length=30)
    book_title = C(label='book_title',max_length=300)
    
    author_name = C(label='author_name',max_length=200)
    publisher_name = C(label='publisher_name',max_length=200)
    
    publish_1st_date = C(label='publish_date',max_length=100)

    price = C(label='price')

    book_width = C(label='width')
    book_height = C(label='height')
    book_page_cnt = C(label='page_num')
    
    book_detail = C(label='book_detail',max_length=3000)
    author_detail = C(label='author_detail', max_length=3000)

    publisher_detail =  C(label='author_detail', max_length=3000)
    



