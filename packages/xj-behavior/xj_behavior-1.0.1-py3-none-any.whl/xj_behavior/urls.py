# _*_coding:utf-8_*_
from django.urls import re_path

from .apis.standing_book_apis import StandingBookApis

app_name = 'xj_behavior'

# 应用路由
urlpatterns = [
    re_path(r'data?$', StandingBookApis.as_view(), ),
]
