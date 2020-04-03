from django.conf.urls import url, include
from django.contrib import admin
from .views import home, register, test

urlpatterns = [
    url(r'^$', home),
    url(r'^register/', register),
    url(r'^test/', test),
]
