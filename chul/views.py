from rest_framework import generics

from .models import (
    CommunityHealthUnit,
    CommunityHealthWorker,
    CommunityHealthWorkerContact,
    Status,
    Community,
    CommunityHealthUnitContact,
    Approver,
    CommunityHealthUnitApproval,
    CommunityHealthWorkerApproval,
    ApprovalStatus
)

from .serializers import (
    CommunityHealthUnitSerializer,
    CommunityHealthWorkerSerializer,
    CommunityHealthWorkerContactSerializer,
    StatusSerializer,
    CommunitySerializer,
    CommunityHealthUnitContactSerializer,
    ApproverSerializer,
    CommunityHealthUnitApprovalSerializer,
    CommunityHealthWorkerApprovalSerializer,
    ApprovalStatusSerializer
)

from .filters import (
    CommunityHealthUnitFilter,
    CommunityHealthWorkerFilter,
    CommunityHealthWorkerContactFilter,
    StatusFilter,
    CommunityFilter,
    CommunityHealthUnitContactFilter,
    ApproverFilter,
    CommunityHealthUnitApprovalFilter,
    CommunityHealthWorkerApprovalFilter,
    ApprovalStatusFilter
)


class StatusListView(generics.ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    filter_class = StatusFilter
    ordering_fields = ('name', 'description', )


class StatusDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class CommunityListView(generics.ListCreateAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    filter_class = CommunityFilter
    ordering_fields = ('name', 'code', )


class CommunityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer


class CommunityHealthUnitContactListView(generics.ListCreateAPIView):
    queryset = CommunityHealthUnitContact.objects.all()
    serializer_class = CommunityHealthUnitContactSerializer
    filter_class = CommunityHealthUnitContactFilter
    ordering_fields = ('health_unit', 'contact', )


class CommunityHealthUnitContactDetailView(
        generics.RetrieveUpdateDestroyAPIView):
    queryset = CommunityHealthUnitContact.objects.all()
    serializer_class = CommunityHealthUnitContactSerializer


class ApproverListView(generics.ListCreateAPIView):
    queryset = Approver.objects.all()
    serializer_class = ApproverSerializer
    filter_class = ApproverFilter
    ordering_fields = ('name', 'abbreviation',)


class ApproverDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Approver.objects.all()
    serializer_class = ApproverSerializer


class CommunityHealthUnitApprovalListView(generics.ListCreateAPIView):
    queryset = CommunityHealthUnitApproval.objects.all()
    serializer_class = CommunityHealthUnitApprovalSerializer
    filter_class = CommunityHealthUnitApprovalFilter
    ordering_fields = ('health_unit', 'approver', 'approval_status')


class CommunityHealthUnitApprovalDetailView(
        generics.RetrieveUpdateDestroyAPIView):
    queryset = CommunityHealthUnitApproval.objects.all()
    serializer_class = CommunityHealthUnitApprovalSerializer


class CommunityHealthWorkerApprovalListView(generics.ListCreateAPIView):
    queryset = CommunityHealthWorkerApproval.objects.all()
    serializer_class = CommunityHealthWorkerApprovalSerializer
    filter_class = CommunityHealthWorkerApprovalFilter
    ordering_fields = ('health_worker', 'approver', 'approval_status')


class CommunityHealthWorkerApprovalDetailView(
        generics.RetrieveUpdateDestroyAPIView):
    queryset = CommunityHealthWorkerApproval.objects.all()
    serializer_class = CommunityHealthWorkerApprovalSerializer


class ApprovalStatusListView(generics.ListCreateAPIView):
    queryset = ApprovalStatus.objects.all()
    serializer_class = ApprovalStatusSerializer
    filter_class = ApprovalStatusFilter
    ordering_fields = ('name', 'description',)


class ApprovalStatusDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ApprovalStatus.objects.all()
    serializer_class = ApprovalStatusSerializer


class CommunityHealthUnitListView(generics.ListCreateAPIView):
    queryset = CommunityHealthUnit.objects.all()
    serializer_class = CommunityHealthUnitSerializer
    filter_class = CommunityHealthUnitFilter
    ordering_fields = ('name', 'facility',)


class CommunityHealthUnitDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CommunityHealthUnit.objects.all()
    serializer_class = CommunityHealthUnitSerializer


class CommunityHealthWorkerListView(generics.ListCreateAPIView):
    queryset = CommunityHealthWorker.objects.all()
    serializer_class = CommunityHealthWorkerSerializer
    filter_class = CommunityHealthWorkerFilter
    ordering_fields = ('first_name', 'last_name', 'username',)


class CommunityHealthWorkerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CommunityHealthWorker.objects.all()
    serializer_class = CommunityHealthWorkerSerializer


class CommunityHealthWorkerContactListView(generics.ListCreateAPIView):
    queryset = CommunityHealthWorkerContact.objects.all()
    serializer_class = CommunityHealthWorkerContactSerializer
    filter_class = CommunityHealthWorkerContactFilter
    ordering_fields = ('contact',)


class CommunityHealthWorkerContactDetailView(
        generics.RetrieveUpdateDestroyAPIView):
    queryset = CommunityHealthWorkerContact.objects.all()
    serializer_class = CommunityHealthWorkerContactSerializer
