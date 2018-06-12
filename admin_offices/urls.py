from django.conf.urls import url, patterns

from . import views


urlpatterns = patterns(
    '',

    url(r'^contacts/$',
        views.AdminOfficeContactListView.as_view(),
        name='admin_office_contacts_list'),

    url(r'^contacts/(?P<pk>[^/]+)/$',
        views.AdminOfficeContactDetailView.as_view(),
        name="admin_office_contact_detail"),

    url(r'^(?P<pk>[^/]+)/$',
        views.AdminOfficeDetailView.as_view(),
        name="admin_office_detail"),
    url(r'^$',
        views.AdminOfficeListView.as_view(),
        name='admin_offices_list'),

)
