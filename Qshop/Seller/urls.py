from django.urls import path, re_path
from Seller.views import *
# from django.views.decorators.cache import cache_page
urlpatterns = [
    # path('register/', cache_page(60*15)(register)),
    path('register/', register),
    path('login/', login),
    path('index/', index),
    path('logout/', logout),
    path('base/', base),
]
