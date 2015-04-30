from __future__ import unicode_literals
from django.conf.urls import url, patterns

from .views import APILogin, APILogout, UserList, UserDetailView

template_name = {'template_name': 'rest_framework/login.html'}


urlpatterns = patterns(
    '',
    url(r'^api_login/$', APILogin.as_view(), name='user_login'),
    url(r'^api_logout/$', APILogout.as_view(), name='user_logout'),

    url(r'^$', UserList.as_view(), name='mfl_users_list'),
    url(r'^(?P<pk>[^/]+)/$', UserDetailView.as_view(),
        name='mfl_user_detail'),
)
