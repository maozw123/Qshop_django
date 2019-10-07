from django.urls import path,re_path,include
from Buyer.views import *
urlpatterns = [
    path('register/',register ),
    path('login/',login),
    path('logout/',logout),
    path('index/',index),
    path('base/',base),
    path('goods_list/',goods_list),
    path('user_info/',user_center_info),
    path('pay_order/',pay_order),
    path('alipay/',AlipayViews),
    path('pay_result/',pay_result),
    path('add_cart/',add_cart),
    path('cart/',cart),
    path('pay_order_more/',pay_order_more),
    path('uco/',user_center_order),
    path('gt/',get_task),
    re_path('goods_detail/(?P<id>\d+)/', goods_detail),
]