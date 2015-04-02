from django.conf.urls import url, patterns

from .views import (
    RolesList, RoleDetailView, PermissionsList, PermissionDetailView,
    RolePermissionsList, RolePermissionDetailView, UserRolesList,
    UserRoleDetailView)


urlpatterns = patterns(
    '',
    url(r'^user_roles/$', UserRolesList.as_view(),
        name='user_roles_list'),

    url(r'^user_roles/(?P<id>\w+)/$', UserRoleDetailView.as_view(),
        name='user_role_detail'),

    url(r'^role_permissions/$', RolePermissionsList.as_view(),
        name='role_permissions_list'),

    url(r'^role_permissions/(?P<id>\w+)/$', RolePermissionDetailView.as_view(),
        name='role_permission_detail'),

    url(r'^permissions/$', PermissionsList.as_view(), name='permissions_list'),
    url(r'^permissions/(?P<id>\w+)/$', PermissionDetailView.as_view(),
        name='permission_detail'),

    url(r'^$', RolesList.as_view(), name='roles_list'),
    url(r'^(?P<id>\w+)/$', RoleDetailView.as_view(),
        name='role_detail'),
)
