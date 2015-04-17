from rest_framework import generics

from .models import (
    CommunityHealthUnit,
    CommunityHealthWorker,
    CommunityHealthWorkerContact
)

from .serializers import (
    CommunityHealthUnitSerializer,
    CommunityHealthWorkerSerializer,
    CommunityHealthWorkerContactSerializer
)

from .filters import (
    CommunityHealthUnitFilter,
    CommunityHealthWorkerFilter,
    CommunityHealthWorkerContactFilter)


class CommunityHealthUnitListView(generics.ListCreateAPIView):
    queryset = CommunityHealthUnit.objects.all()
    serializer_class = CommunityHealthUnitSerializer
    filter_class = CommunityHealthUnitFilter
    ordering_fields = ('name', 'facility',)


class CommunityHealthUnitDetailView(generics.RetrieveUpdateDestroryAPIView):
    queryset = CommunityHealthUnit.objects.all()
    serializer_class = CommunityHealthUnitSerializer


class CommunityHealthWorkerListView(generics.ListCreateAPIViewA):
    queryset = CommunityHealthWorker.objects.all()
    serializer_class = CommunityHealthWorkerSerializer
    filter_class = CommunityHealthWorkerFilter
    ordering_fields = ('first_name', 'last_name', 'username',)


class CommunityHealthWorkerDetailView(generics.RetrieveUpdateDestroyAPUView):
    queryset = CommunityHealthWorker.objects.all()
    serializer_class = CommunityHealthWorkerSerializer


class CommunityHealthWorkerContactListView(generics.ListCreateAPIView):
    queryset = CommunityHealthWorkerContact.objects.all()
    serializer_class = CommunityHealthWorkerContactSerializer
    filter_class = CommunityHealthWorkerContactFilter
    ordering_fields = ('contact',)


class CommunityHealthWorkerContactDetailView(
        generics.RetrieveUpdateDestroyView):
    queryset = CommunityHealthWorkerContact.objests.all()
    serializer_class = CommunityHealthWorkerContactSerializer

