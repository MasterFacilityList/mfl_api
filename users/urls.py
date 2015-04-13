from django.conf.urls import url, patterns

from .views import (
    APILogin, APILogout, UserList, UserDetailView, UserCountiesView,
    UserCountyDetailView,
)

urlpatterns = patterns(
    '',
    url(r'^login/$', APILogin.as_view(), name='user_login'),
    url(r'^logout/$', APILogout.as_view(), name='user_logout'),

    url(r'^counties/$', UserCountiesView.as_view(), name='users_county_list'),
    url(r'^counties/(?P<pk>[^/]+)/$', UserCountyDetailView.as_view(),
        name='user_county_detail'),


    url(r'^$', UserList.as_view(), name='users_list'),
    url(r'^(?P<pk>[^/]+)/$', UserDetailView.as_view(),
        name='user_detail'),

)
