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
    url(r'^(?P<pk>[^/]+)',
        CommunityHealthWorkerDetailView.as_view,
        name="community_health_worker_detail"),
    url(r'^$', CommunityHealthWorkerListView.as_view(),
        name='community_health_workers_list'),

    url(r'^(?P<pk>[^/]+)',
        CommunityHealthWorkerContactDetailView.as_view(),
        name="community_health_worker_contact_detail"),
    url(r'^$', CommunityHealthWorkerContactListView.as_view(),
        name='community_health_worker_contacts_list'),

    url(r'^chul/(?P<pk>[^/]+)/',
        CommunityHealthUnitDetailView.as_view,
        name='community_health_unit_detail'),
    url(r'^chul/$', CommunityHealthUnitListView.as_view(),
        name='community_health_units_list'),
)
