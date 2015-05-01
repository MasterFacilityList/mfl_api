from __future__ import unicode_literals
from django.conf.urls import url, patterns

from .views import (
    UserList,
    UserDetailView,
    MFLOauthApplicationListView,
    MFLOauthApplicationDetailView
)


urlpatterns = patterns(
    '',

    url(r'^applications/$', MFLOauthApplicationListView.as_view(),
        name='mfl_oauth_applications_list'),
    url(r'^applications/(?P<pk>[^/]+)/$',
        MFLOauthApplicationDetailView.as_view(),
        name='mfl_oauth_application_detail'),

    url(r'^$', UserList.as_view(), name='mfl_users_list'),
    url(r'^(?P<pk>[^/]+)/$', UserDetailView.as_view(),
        name='mfl_user_detail'),
)
