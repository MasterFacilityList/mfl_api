from django.conf.urls import url, patterns, include
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from common.views import APIRoot, root_redirect_view
from rest_auth.views import (
    PasswordChange, PasswordReset, PasswordResetConfirm
)


# copied from rest_auth.urls just to remove login and logout urls
# this may be a hack but other methods looked scarier
rest_auth_patterns = patterns(
    '',

    url(r'^password/reset/$', PasswordReset.as_view(),
        name='rest_password_reset'),
    url(r'^password/reset/confirm/$', PasswordResetConfirm.as_view(),
        name='rest_password_reset_confirm'),

    url(r'^password/change/$', PasswordChange.as_view(),
        name='rest_password_change'),
    url(r'^registration/',
        include('rest_auth.registration.urls', namespace='registration'))
)

apipatterns = patterns(
    '',

    url(r'^$', login_required(
        cache_page(60*60)(APIRoot.as_view())), name='root_listing'),
    url(r'^explore/',
        include('rest_framework_swagger.urls', namespace='swagger')),
    url(r'^common/', include('common.urls', namespace='common')),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^facilities/', include('facilities.urls', namespace='facilities')),
    url(r'^chul/', include('chul.urls', namespace='chul')),
    url(r'^gis/', include('mfl_gis.urls', namespace='mfl_gis')),

    # rest-auth urls
    url(r'^rest-auth/', include(rest_auth_patterns, namespace='rest_auth')),
)

urlpatterns = patterns(
    '',

    url(r'^$', root_redirect_view, name='root_redirect'),
    url(r'^api/', include(apipatterns, namespace='api')),
    url(r'^accounts/',
        include('rest_framework.urls', namespace='rest_framework')),
    url(r'^oauth2/', include('oauth2_provider.urls')),
)
