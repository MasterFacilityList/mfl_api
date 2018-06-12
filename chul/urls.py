from django.conf.urls import url, patterns

from . import views


urlpatterns = patterns(
    '',

    url(r'^updates/$', views.ChuUpdateBufferListView.as_view(),
        name='chu_updatebufers_list'),

    url(r'^updates/(?P<pk>[^/]+)/$',
        views.ChuUpdateBufferDetailView.as_view(),
        name="chu_updatebuffer_detail"),

    url(r'^services/$', views.CHUServiceListView.as_view(),
        name='chu_services_list'),
    url(r'^services/(?P<pk>[^/]+)/$',
        views.CHUServiceDetailView.as_view(), name="chu_service_detail"),

    url(r'^statuses/$', views.StatusListView.as_view(), name='statuses_list'),
    url(r'^statuses/(?P<pk>[^/]+)/$',
        views.StatusDetailView.as_view(), name="status_detail"),

    url(r'^unit_contacts/$',
        views.CommunityHealthUnitContactListView.as_view(),
        name='community_health_unit_contacts_list'),
    url(r'^unit_contacts/(?P<pk>[^/]+)/$',
        views.CommunityHealthUnitContactDetailView.as_view(),
        name="community_health_unit_contact_detail"),

    url(r'^workers/$', views.CommunityHealthWorkerListView.as_view(),
        name='community_health_workers_list'),
    url(r'^workers/(?P<pk>[^/]+)/$',
        views.CommunityHealthWorkerDetailView.as_view(),
        name="community_health_worker_detail"),

    url(r'^workers_contacts/$',
        views.CommunityHealthWorkerContactListView.as_view(),
        name='community_health_worker_contacts_list'),
    url(r'^workers_contacts/(?P<pk>[^/]+)/$',
        views.CommunityHealthWorkerContactDetailView.as_view(),
        name="community_health_worker_contact_detail"),


    url(r'^units/$',
        views.CommunityHealthUnitListView.as_view(),
        name='community_health_units_list'),
    url(r'^units/(?P<pk>[^/]+)/$',
        views.CommunityHealthUnitDetailView.as_view(),
        name='community_health_unit_detail'),

    url(r'^chu_ratings/$',
        views.CHURatingListView.as_view(), name='chu_ratings'),
    url(r'^chu_ratings/(?P<pk>[a-z0-9\-]{32,32})/$',
        views.CHURatingDetailView.as_view(), name='chu_rating_detail'),

    url(r'^units_detail_report/(?P<pk>[^/]+)/$',
        views.CHUDetailReport.as_view(), name='chu_detail_report'),

)
