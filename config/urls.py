from django.conf.urls import url, patterns, include
from django.contrib import admin
admin.autodiscover()


apipatterns = patterns(
    '',
    url(r'^common/', include('common.urls', namespace='common')),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^roles/', include('roles.urls', namespace='roles')),
    url(r'^facilities/', include('facilities.urls', namespace='facilities')),
)

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(apipatterns, namespace='api')),
    url(r'^api/auth/',
        include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/token/', 'rest_framework.authtoken.views.obtain_auth_token'),
)
