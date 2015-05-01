from __future__ import unicode_literals
from django.conf.urls import url, patterns

from .views import UserList, UserDetailView


urlpatterns = patterns(
    '',
    url(r'^$', UserList.as_view(), name='mfl_users_list'),
    url(r'^(?P<pk>[^/]+)/$', UserDetailView.as_view(),
        name='mfl_user_detail'),
)
