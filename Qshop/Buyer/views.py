import hashlib
from django.shortcuts import render, HttpResponseRedirect
from Seller.models import *
from Buyer.models import *
from django.http import JsonResponse


# Create your views here.
def loginValid(fun):
    def inner(request, *args, **kwargs):
        cookie_uesr = request.COOKIES.get('username')
        session_user = request.session.get('username')
        if cookie_uesr and session_user and cookie_uesr == session_user:
            return fun(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/Buyer/login/')

    return inner


def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result

from django.views.decorators.cache import cache_page

@cache_page(60*15)
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pwd')
        if email:
            user = LoginUser.objects.filter(email=email).first()
            if user:
                db_password = user.password
                password = setPassword(password)
                if db_password == password:
                    response = HttpResponseRedirect("/Buyer/index/")
                    response.set_cookie("username", user.username)
                    response.set_cookie("user_id", user.id)
                    request.session["username"] = user.username
                    return response
    return render(request, 'buyer/login.html', locals())


def register(request):
    if request.method == 'POST':
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        if email:
            user1 = LoginUser.objects.filter(email=email).first()
            if not user1:
                user = LoginUser()
                user.username = username
                user.password = setPassword(password)
                user.email = email
                user.save()
                return HttpResponseRedirect("/Buyer/login/")
    return render(request, 'buyer/register.html')


def logout(request):
    url = request.META.get("HTTP_REFERER", "/Buyer/index/")
    response = HttpResponseRedirect(url)
    for k in request.COOKIES:
        response.delete_cookie(k)
    del request.session["username"]
    return response


def index(request):
    result = []
    goods_type = GoodsType.objects.all()
    for ty in goods_type:
        goods = ty.goods_set.order_by('-goods_pro_time')
        if len(goods) >= 4:
            goods = goods[:4]
            result.append({'type': ty, 'goods_list': goods})
    return render(request, 'buyer/index.html', locals())


def base(request):
    return render(request, 'buyer/base.html', locals())





