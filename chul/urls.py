from django.conf.urls import url, patterns

from .views import(
    CommunityHealthUnitListView,
    CommunityHealthUnitDetailView,
    CommunityHealthWorkerListView,
    CommunityHealthWorkerDetailView,
    CommunityHealthWorkerContactListView,
    CommunityHealthWorkerContactDetailView)


urlpatterns = patterns(
    '',
    url(r'^workers/$', CommunityHealthWorkerListView.as_view(),
        name='community_health_workers_list'),
    url(r'^workers/(?P<pk>[^/]+)/$',
        CommunityHealthWorkerDetailView.as_view(),
        name="community_health_worker_detail"),


    url(r'^workers_contacts/$', CommunityHealthWorkerContactListView.as_view(),
        name='community_health_worker_contacts_list'),
    url(r'^workers_contacts/(?P<pk>[^/]+)/$',
        CommunityHealthWorkerContactDetailView.as_view(),
        name="community_health_worker_contact_detail"),


    url(r'^units/$', CommunityHealthUnitListView.as_view(),
        name='community_health_units_list'),
    url(r'^units/(?P<pk>[^/]+)/$',
        CommunityHealthUnitDetailView.as_view(),
        name='community_health_unit_detail'),
)
