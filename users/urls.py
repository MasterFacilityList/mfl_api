from django.conf.urls import url, patterns

from .views import APILogin, APILogout, UserList, UserDetailView

urlpatterns = patterns(
    '',
    url(r'^login/$', APILogin.as_view(), name='user_login'),
    url(r'^logout/$', APILogout.as_view(), name='user_logout'),

    url(r'^$', UserList.as_view(), name='mfl_users_list'),
    url(r'^(?P<pk>[^/]+)/$', UserDetailView.as_view(),
        name='mfl_user_detail'),
)
