from django.conf.urls import url, patterns, include

from common.views import APIRoot


apipatterns = patterns(
    '',
    url(r'^$', APIRoot.as_view(), name='root_listing'),
    url(r'^explore/', include('rest_framework_swagger.urls')),
    url(r'^common/', include('common.urls', namespace='common')),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^facilities/', include('facilities.urls', namespace='facilities')),
    url(r'^chul/', include('chul.urls', namespace='chul')),
    url(r'^mfl_gis/', include('mfl_gis.urls', namespace='mfl_gis')),
)

urlpatterns = patterns(
    '',
    url(r'^api/', include(apipatterns, namespace='api')),
    url(r'^api/auth/',
        include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/token/', 'rest_framework.authtoken.views.obtain_auth_token'),

    # The next three patterns are for django-rest-auth
    # They are there Single Page Application authentication and registration
    url(r'^accounts/', include('allauth.urls')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
)
