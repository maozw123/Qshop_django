import hashlib

from django.core.paginator import Paginator

from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from Seller.models import *
from django.http import JsonResponse


# Create your views here.
def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result


def loginValid(fun):
    def inner(request, *args, **kwargs):
        cookie_username = request.COOKIES.get('username')
        session_username = request.session.get('username')
        if cookie_username and session_username and cookie_username == session_username:
            return fun(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/Seller/login/')

    return inner


def register(request):
    error_message = ''
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email:
            user = LoginUser.objects.filter(email=email).first()
            if not user:
                new_user = LoginUser()
                new_user.email = email
                new_user.username = email
                new_user.password = setPassword(password)
                new_user.save()
            else:
                error_message = '邮箱已经被注册，请登录'
        else:
            error_message = '邮箱不可以为空'
    return render(request, 'seller/register.html', locals())


import datetime,time


def login(request):
    error_message = ''
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        code = request.POST.get('valid_code')
        if email:
            user = LoginUser.objects.filter(email=email).first()
            if user:
                db_password = user.password
                password = setPassword(password)
                if db_password == password:
                    codes = Valid_Code.objects.filter(code_user=email).order_by("-code_time").first()
                    now = time.mktime(datetime.datetime.now().timetuple())
                    db_time = time.mktime(codes.code_time.timetuple())
                    t=(now-db_time)/60
                    if codes and codes.code_state==0 and t<=5 and codes.code_content.upper()==code.upper():
                        response = HttpResponseRedirect('/Seller/index/')
                        response.set_cookie('username', user.username)
                        response.set_cookie('user_id', user.id)
                        request.session['username'] = user.username
                        return response
                    else:
                        error_message="验证码错误"
                else:
                    error_message = '密码错误'
            else:
                error_message = '用户不存在'
        else:
            error_message = '邮箱不可以空'

    return render(request, 'seller/login.html', locals())


def logout(request):
    response = HttpResponseRedirect('/Seller/login/')
    keys = request.COOKIES.keys()
    for key in keys:
        response.delete_cookie(key)
    del request.session['username']
    return response


@loginValid
def index(request):
    return render(request, 'seller/index.html', locals())


@loginValid
def base(request):
    return render(request, 'seller/base.html', locals())





