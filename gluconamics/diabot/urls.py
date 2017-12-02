from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import url, include


from . import views

urlpatterns = [
    url(r'^$', views.studies_view, name='index'),

]