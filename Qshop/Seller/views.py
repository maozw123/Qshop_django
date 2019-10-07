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


@loginValid
def goods_list(request, status, page=1):
    page = int(page)
    # print(status,type(status))
    if status == '1':
        # print('------------------')
        goodses = Goods.objects.filter(goods_status=1)
    elif status == '0':
        goodses = Goods.objects.filter(goods_status=0)
    else:
        goodses = Goods.objects.all()

    all_goods = Paginator(goodses, 10)
    goods_list = all_goods.page(page)
    return render(request, 'seller/goods_list.html', locals())


@loginValid
def goods_status(request, state, id):
    id = int(id)
    goods = Goods.objects.get(id=id)
    if state == 'up':
        goods.goods_status = 1
    elif state == 'down':
        goods.goods_status = 0
    goods.save()
    url = request.META.get('HTTP_REFERER', '/goods_list/1/1')
    return HttpResponseRedirect(url)


@loginValid
def personal_info(request):
    user_id = request.COOKIES.get('user_id')
    user = LoginUser.objects.get(id=user_id)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.gender = request.POST.get('gender')
        user.age = request.POST.get('age')
        user.phone_number = request.POST.get('phone_number')
        user.address = request.POST.get('address')
        user.photo = request.FILES.get('photo')
        user.save()
    return render(request, 'seller/personal_info.html', locals())


@loginValid
def goods_add(request):
    goods_type_list = GoodsType.objects.all()
    if request.method == 'POST':
        data = request.POST
        files = request.FILES
        goods = Goods()
        # 常规保存
        goods.goods_number = data.get('goods_number')
        goods.goods_name = data.get('goods_name')
        goods.goods_price = data.get('goods_price')
        goods.goods_count = data.get('goods_count')
        goods.goods_location = data.get('goods_location')
        goods.goods_safe_date = data.get('goods_safe_date')
        goods.goods_pro_time = data.get('goods_pro_time')
        goods.goods_status = 1
        # 保存外键类型
        goods_type_id = data.get('goods_type')
        goods.goods_type = GoodsType.objects.get(id=goods_type_id)
        # 保存图片
        picture = files.get('picture')
        goods.picture = picture
        # 保存对应的卖家
        user_id = request.COOKIES.get('user_id')
        goods.goods_store = LoginUser.objects.get(id=int(user_id))
        goods.save()
    return render(request, 'seller/goods_add.html', locals())


import random


def random_code(len=6):
    #  生成六位验证码
    string = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    valid_code = "".join([random.choice(string) for i in range(len)])
    return valid_code


import json
import requests
from Qshop.settings import DING_URL


def sendDing(content, to=None):
    headers = {
        "Content-Type": "application/json",
        "Charset": "utf-8"
    }
    requests_data = {
        "msgtype": "text",
        "text": {
            "content": content
        },
        "at": {
            "atMobiles": [
            ],
            "isAtAll": True
        }
    }
    if to:
        requests_data["at"]["atMobiles"].append(to)
        requests_data["at"]["isAtAll"] = False
    else:
        requests_data["at"]["atMobiles"].clear()
        requests_data["at"]["isAtAll"] = True
    sendData = json.dumps(requests_data)
    response = requests.post(url=DING_URL, headers=headers, data=sendData)
    content = response.json()
    return content


from django.views.decorators.csrf import csrf_exempt
from CeleryTask.tasks import sendDing

@csrf_exempt
def send_login_code(request):
    result = {
        "code": 200,
        "data": ""
    }
    if request.method == "POST":
        email = request.POST.get("email")
        code = random_code()
        c = Valid_Code()
        c.code_user = email
        c.code_content = code
        c.save()
        send_data = "%s的验证码是%s" % (email, code)
        # sendDing(send_data)  # 发送验证
        sendDing.delay(send_data)
        result["data"] = "发送成功"
    else:
        result["code"] = 400
        result["data"] = "请求错误"
    return JsonResponse(result)

def order_list(request,status):
    """
    status  订单状态
    0 未支付
    1 已支付
    2 待收货
    3/4 完成/拒收
    """
    status=int(status)
    user_id=request.COOKIES.get("user_id")  #获取店铺的id
    store=LoginUser.objects.get(id=user_id)  #获取店铺的信息
    store_order=store.orderinfo_set.filter(order_status=status).order_by('-id')   #获取店铺对应的订单
    return render(request,'seller/order_list.html',locals())

from Buyer.models import OrderInfo
def change_order(request):
    #通过订单详情id来锁定订单详情
    order_id=request.GET.get("order_id")
    #获取要修改的状态
    order_status=request.GET.get("order_status")
    order=OrderInfo.objects.get(id=order_id)
    order.order_status=int(order_status)
    order.save()
    return JsonResponse({"data":"修改完成"})