from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import url, include


from . import views

urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^$', views.about_view, name='about'),
]