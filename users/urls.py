from __future__ import unicode_literals
from django.conf.urls import url, patterns
from django.contrib.auth import views as contrib_auth_views

from .views import APILogin, APILogout, UserList, UserDetailView, mfl_login

template_name = {'template_name': 'rest_framework/login.html'}


urlpatterns = patterns(
    '',
    url(r'^api_login/$', APILogin.as_view(), name='user_login'),
    url(r'^api_logout/$', APILogout.as_view(), name='user_logout'),

    url(r'^login/$', mfl_login, name='login'),
    url(r'^logout/$', contrib_auth_views.logout, template_name, name='logout'),

    url(r'^$', UserList.as_view(), name='mfl_users_list'),
    url(r'^(?P<pk>[^/]+)/$', UserDetailView.as_view(),
        name='mfl_user_detail'),
)
