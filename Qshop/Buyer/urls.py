from django.urls import path,re_path,include
from Buyer.views import *
urlpatterns = [
    path('register/',register ),
    path('login/',login),
    path('logout/',logout),
    path('index/',index),
    path('base/',base),
]