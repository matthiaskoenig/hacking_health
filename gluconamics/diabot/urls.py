from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import url, include


from . import views

urlpatterns = [
    url(r'^$', views.index_view, name='index'),

    url(r'^users/$', views.users_view, name='users'),
    url(r'^users/(?P<user_id>[0-9]+)/$', views.user_view, name='user'),
    url(r'^recommendations/$', views.recommendations_view, name='recommendations'),

    url(r'^about/$', views.about_view, name='about'),
]