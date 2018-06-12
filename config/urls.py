from django.conf.urls import url, patterns, include
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from common.views import APIRoot, root_redirect_view

from rest_auth.views import (
    Login, Logout, UserDetails, PasswordChange,
    PasswordReset, PasswordResetConfirm
)

rest_auth_patterns = patterns(
    # re-written from rest_auth.urls because of cache validation

    '',
    # URLs that do not require a session or valid token
    url(r'^password/reset/$',
        cache_page(0)(PasswordReset.as_view()),
        name='rest_password_reset'),
    url(r'^password/reset/confirm/$',
        cache_page(0)(PasswordResetConfirm.as_view()),
        name='rest_password_reset_confirm'),
    url(r'^login/$',
        cache_page(0)(Login.as_view()), name='rest_login'),
    # URLs that require a user to be logged in with a valid session / token.
    url(r'^logout/$',
        cache_page(0)(Logout.as_view()), name='rest_logout'),
    url(r'^user/$',
        cache_page(0)(UserDetails.as_view()), name='rest_user_details'),
    url(r'^password/change/$',
        cache_page(0)(PasswordChange.as_view()), name='rest_password_change'),
)

apipatterns = patterns(
    '',
    url(r'^$', login_required(
        cache_page(60*60)(APIRoot.as_view())), name='root_listing'),
    url(r'^explore/', include('rest_framework_swagger.urls',
        namespace='swagger')),
    url(r'^common/', include('common.urls', namespace='common')),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^facilities/', include('facilities.urls', namespace='facilities')),
    url(r'^chul/', include('chul.urls', namespace='chul')),
    url(r'^gis/', include('mfl_gis.urls', namespace='mfl_gis')),
    url(r'^reporting/', include('reporting.urls', namespace='reporting')),
    url(r'^admin_offices/', include('admin_offices.urls', namespace='admin_offices')),
    url(r'^rest-auth/', include(rest_auth_patterns, namespace='rest_auth')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls',
        namespace='rest_auth_registration'))
)

urlpatterns = patterns(
    '',
    url(r'^$', root_redirect_view, name='root_redirect'),
    url(r'^api/', include(apipatterns, namespace='api')),
    url(r'^accounts/',
        include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/token/', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
)
