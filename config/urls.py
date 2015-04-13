from django.conf.urls import url, patterns, include


apipatterns = patterns(
    '',
    url(r'^explore/', include('rest_framework_swagger.urls')),
    url(r'^common/', include('common.urls', namespace='common')),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^facilities/', include('facilities.urls', namespace='facilities')),
)

urlpatterns = patterns(
    '',
    url(r'^api/', include(apipatterns, namespace='api')),
    url(r'^api/auth/',
        include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/token/', 'rest_framework.authtoken.views.obtain_auth_token'),
)
