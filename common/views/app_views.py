from rest_framework import generics, views, response, parsers

from rest_framework_xml.parsers import XMLParser

from ..models import (
    Contact,
    PhysicalAddress,
    County,
    Ward,
    Constituency,
    ContactType,
    UserCounty,
    UserContact,
    Town,
    UserConstituency,
    SubCounty,
    DocumentUpload,
    ErrorQueue,
    UserSubCounty,
    Notification
)
from facilities.models import(
    FacilityStatus,
    ServiceCategory,
    FacilityType,
    OwnerType,
    Owner,
    Service,
    KephLevel
)
from users.models import JobTitle
from chul import models as chu_models
from ..serializers import (
    ContactSerializer,
    CountySerializer,
    CountyDetailSerializer,
    WardSerializer,
    WardDetailSerializer,
    PhysicalAddressSerializer,
    ConstituencySerializer,
    ConstituencyDetailSerializer,
    ConstituencySlimDetailSerializer,
    CountySlimDetailSerializer,
    WardSlimDetailSerializer,
    ContactTypeSerializer,
    UserCountySerializer,
    UserContactSerializer,
    TownSerializer,
    FilteringSummariesSerializer,
    UserConstituencySerializer,
    SubCountySerializer,
    DocumentUploadSerializer,
    ErrorQueueSerializer,
    UserSubCountySerializer,
    NotificationSerializer
)
from ..filters import (
    ContactTypeFilter,
    ContactFilter,
    PhysicalAddressFilter,
    CountyFilter,
    ConstituencyFilter,
    WardFilter,
    UserCountyFilter,
    UserContactFilter,
    TownFilter,
    UserConstituencyFilter,
    SubCountyFilter,
    DocumentUploadFilter,
    ErrorQueueFilter,
    UserSubCountyFilter,
    NotificationFilter
)
from .shared_views import AuditableDetailViewMixin
from ..utilities import CustomRetrieveUpdateDestroyView


class NotificationListView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    ordering_fields = ('group', 'created', 'title')
    filter_class = NotificationFilter

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if not user.is_national:
            user_groups = user.groups.all()
            return self.queryset.filter(group__in=user_groups)
        return self.queryset


class NotificationDetailView(CustomRetrieveUpdateDestroyView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class UserSubCountyListView(generics.ListCreateAPIView):

    """
    Lists and creates user sub counties

    user  -- The user id of the linked user
    sub_county --  The id of the sub_county
    Created ---  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = UserSubCounty.objects.all()
    serializer_class = UserSubCountySerializer
    ordering_fields = ('user', 'sub_county',)
    filter_class = UserSubCountyFilter


class UserSubCountyDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):

    """
    Retrieves a particular user sub_county
    """
    queryset = UserSubCounty.objects.all()
    serializer_class = UserSubCountySerializer


class SubCountyListView(generics.ListCreateAPIView):

    """
    Lists and creates sub counties

    county  --  A county pk
    name  -- The name of the sub county
    code --  The code given to the sub county
    Created ---  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = SubCounty.objects.all()
    serializer_class = SubCountySerializer
    ordering_fields = ('name', 'code', 'county')
    filter_class = SubCountyFilter

    def get_queryset(self):
        if self.request.user.sub_county:
            county_ids = [
                user_con.sub_county.county.id for user_con in
                UserSubCounty.objects.filter(user=self.request.user)
            ]
            return SubCounty.objects.filter(county_id__in=county_ids)
        if self.request.user.constituency:
            county_ids = [
                user_con.constituency.county.id for user_con in
                UserConstituency.objects.filter(user=self.request.user)
            ]
            return SubCounty.objects.filter(county_id__in=county_ids)
        if self.request.user.county:
            county_ids = [
                uc.county.id for uc in
                UserCounty.objects.filter(user=self.request.user)
            ]
            return SubCounty.objects.filter(county_id__in=county_ids)
        return self.queryset


class SubCountyDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):

    """
    Retrieves a particular sub_county
    """
    queryset = SubCounty.objects.all()
    serializer_class = SubCountySerializer


class ContactView(generics.ListCreateAPIView):

    """
    Lists and creates contacts

    contact_type  --  A contact type pk
    Created ---  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    ordering_fields = ('contact_type', 'contact',)
    filter_class = ContactFilter


class ContactDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):

    """
    Retrieves a particular contact
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class PhysicalAddressView(generics.ListCreateAPIView):

    """
    Lists and creates physical addresses

    Created ---  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = PhysicalAddress.objects.all()
    serializer_class = PhysicalAddressSerializer
    ordering_fields = ('town', )
    filter_class = PhysicalAddressFilter


class PhysicalAddressDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):

    """
    Retrieves a particular physical address
    """
    queryset = PhysicalAddress.objects.all()
    serializer_class = PhysicalAddressSerializer


class CountyView(generics.ListCreateAPIView):

    """
    Lists and creates counties

    Created ---  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    deleted -- Boolean is the record deleted
    """
    queryset = County.objects.all()
    serializer_class = CountySerializer
    ordering_fields = ('name', 'code',)
    filter_class = CountyFilter

    def get_queryset(self):
        if self.request.user.county:
            county_ids = [
                user_county.county.id for user_county in
                UserCounty.objects.filter(
                    user=self.request.user, active=True)
            ]
            return County.objects.filter(id__in=county_ids)
        elif self.request.user.constituency:
            county_ids = [
                user_con.constituency.county.id for user_con in
                UserConstituency.objects.filter(
                    user=self.request.user, active=True)
            ]
            return County.objects.filter(id__in=county_ids)
        elif self.request.user.sub_county:
            county_ids = [
                user_sub.sub_county.county.id for user_sub in
                UserSubCounty.objects.filter(
                    user=self.request.user, active=True)
            ]
            return County.objects.filter(id__in=county_ids)
        else:
            return self.queryset


class CountyDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):

    """
    Retrieves a particular county including the county boundary
    and its facility coordinates
    """
    queryset = County.objects.all()
    serializer_class = CountyDetailSerializer


class CountySlimDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):

    """
    Retrieves the primary details of a county
    """
    queryset = County.objects.all()
    serializer_class = CountySlimDetailSerializer


class WardView(generics.ListCreateAPIView):

    """
    Lists and creates wards

    county  -- A county pk
    constituency --  A constituency pk
    Created ---  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    """
    queryset = Ward.objects.all()
    serializer_class = WardSerializer
    filter_class = WardFilter
    ordering_fields = ('name', 'code', 'constituency',)

    def get_queryset(self):
        if self.request.user.constituency and self.request.user.sub_county:
            const_ids = [
                us.sub_county.id for us in
                UserSubCounty.objects.filter(
                    user=self.request.user, active=True)
            ]
            return Ward.objects.filter(sub_county_id__in=const_ids)

        if self.request.user.constituency:
            const_ids = [
                uc.constituency.id for uc in
                UserConstituency.objects.filter(
                    user=self.request.user, active=True)
            ]
            return Ward.objects.filter(constituency_id__in=const_ids)

        if self.request.user.sub_county:
            const_ids = [
                us.sub_county.id for us in
                UserSubCounty.objects.filter(
                    user=self.request.user, active=True)
            ]
            return Ward.objects.filter(sub_county_id__in=const_ids)

        if self.request.user.county:
            county_ids = [
                uc.county.id for uc in UserCounty.objects.filter(
                    user=self.request.user, active=True)
            ]
            return Ward.objects.filter(constituency__county_id__in=county_ids)
        return Ward.objects.all()


class WardDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):

    """
    Retrieves a particular ward details including ward boundaries
    and facility coordinates
    """
    queryset = Ward.objects.all()
    serializer_class = WardDetailSerializer


class WardSlimDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):

    """
    Retrieves a particular ward primary details
    """
    queryset = Ward.objects.all()
    serializer_class = WardSlimDetailSerializer


class ConstituencyView(generics.ListCreateAPIView):

    """
    Lists and creates constituencies

    county  -- A county pk
    Created ---  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    """
    queryset = Constituency.objects.all()
    serializer_class = ConstituencySerializer
    filter_class = ConstituencyFilter
    ordering_fields = ('name', 'code', 'county',)

    def get_queryset(self):
        user = self.request.user
        if user.constituency:
            con_ids = [
                user_con.constituency.id for user_con in
                UserConstituency.objects.filter(
                    user=user, active=True)
            ]
            return Constituency.objects.filter(id__in=con_ids)

        if user.county:
            county_ids = [
                uc.county.id for uc in UserCounty.objects.filter(
                    user=user, active=True)
            ]
            return Constituency.objects.filter(county_id__in=county_ids)
        if user.sub_county:
            county_ids = [
                uc.sub_county.county.id for uc in UserSubCounty.objects.filter(
                    user=user, active=True)
            ]
            return Constituency.objects.filter(county_id__in=county_ids)

        return self.queryset


class ConstituencyDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):

    """
    Retrieves a  particular constituency
    """
    queryset = Constituency.objects.all()
    serializer_class = ConstituencyDetailSerializer


class ConstituencySlimDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Constituency.objects.all()
    serializer_class = ConstituencySlimDetailSerializer


class ContactTypeListView(generics.ListCreateAPIView):

    """
    Lists and creates contact types

    Created ---  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    """
    queryset = ContactType.objects.all()
    serializer_class = ContactTypeSerializer
    ordering_fields = ('name', )
    filter_class = ContactTypeFilter


class ContactTypeDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):

    """
    Retrieves a particular contact type
    """
    queryset = ContactType.objects.all()
    serializer_class = ContactTypeSerializer


class UserCountyView(generics.ListCreateAPIView):

    """
    Lists and creates links between users and counties

    user -- A user pk
    county --  A county pk

    Created ---  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    """
    queryset = UserCounty.objects.all()
    serializer_class = UserCountySerializer
    filter_class = UserCountyFilter
    ordering_fields = ('user', 'county',)


class UserCountyDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):

    """
    Retrieves a particular link between a user and a county
    """
    queryset = UserCounty.objects.all()
    serializer_class = UserCountySerializer


class UserContactListView(generics.ListCreateAPIView):

    """
    Lists and creates user contacts

    Created ---  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    """
    queryset = UserContact.objects.all()
    serializer_class = UserContactSerializer
    filter_class = UserContactFilter
    ordering_fields = ('user', 'contact',)


class UserContactDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):

    """
    Retrieves a particular user contact
    """
    queryset = UserContact.objects.all()
    serializer_class = UserContactSerializer


class TownListView(generics.ListCreateAPIView):

    """
    Lists and creates towns

    Created ---  Date the record was Created
    Updated -- Date the record was Updated
    Created_by -- User who created the record
    Updated_by -- User who updated the record
    active  -- Boolean is the record active
    """
    queryset = Town.objects.all()
    serializer_class = TownSerializer
    filter_class = TownFilter
    ordering_fields = ('name', )


class TownDetailView(
        AuditableDetailViewMixin, CustomRetrieveUpdateDestroyView):

    """
    Retrieves a particular town detail
    """
    queryset = Town.objects.all()
    serializer_class = TownSerializer


class FilteringSummariesView(views.APIView):

    """
        Retrieves filtering summaries
    """
    serializer_cls = FilteringSummariesSerializer

    def get_counties(self):
        if self.request.user.county:
            county_ids = [
                user_county.county.id for user_county in
                UserCounty.objects.filter(
                    user=self.request.user, active=True)
            ]
            return County.objects.filter(id__in=county_ids)
        elif self.request.user.constituency:
            county_ids = [
                user_con.constituency.county.id for user_con in
                UserConstituency.objects.filter(
                    user=self.request.user, active=True)
            ]
            return County.objects.filter(id__in=county_ids)
        elif self.request.user.sub_county:
            county_ids = [
                user_sub.sub_county.county.id for user_sub in
                UserSubCounty.objects.filter(
                    user=self.request.user, active=True)
            ]
            return County.objects.filter(id__in=county_ids)
        else:
            return County.objects.all()

    def get_constituencies(self):
        user = self.request.user
        if user.constituency:
            con_ids = [
                user_con.constituency.id for user_con in
                UserConstituency.objects.filter(
                    user=user, active=True)
            ]
            return Constituency.objects.filter(id__in=con_ids)

        if user.county:
            county_ids = [
                uc.county.id for uc in UserCounty.objects.filter(
                    user=user, active=True)
            ]
            return Constituency.objects.filter(county_id__in=county_ids)
        if user.sub_county:
            county_ids = [
                uc.sub_county.county.id for uc in UserSubCounty.objects.filter(
                    user=user, active=True)
            ]
            return Constituency.objects.filter(county_id__in=county_ids)
        return Constituency.objects.all()

    def get_sub_counties(self):
        if self.request.user.sub_county:
            county_ids = [
                user_con.sub_county.county.id for user_con in
                UserSubCounty.objects.filter(user=self.request.user)
            ]
            return SubCounty.objects.filter(county_id__in=county_ids)
        if self.request.user.constituency:
            county_ids = [
                user_con.constituency.county.id for user_con in
                UserConstituency.objects.filter(user=self.request.user)
            ]
            return SubCounty.objects.filter(county_id__in=county_ids)
        if self.request.user.county:
            county_ids = [
                uc.county.id for uc in
                UserCounty.objects.filter(user=self.request.user)
            ]
            return SubCounty.objects.filter(county_id__in=county_ids)
        return SubCounty.objects.all()

    def get_wards(self):
        if self.request.user.constituency and self.request.user.sub_county:
            const_ids = [
                us.sub_county.id for us in
                UserSubCounty.objects.filter(
                    user=self.request.user, active=True)
            ]
            return Ward.objects.filter(sub_county_id__in=const_ids)

        if self.request.user.constituency:
            const_ids = [
                uc.constituency.id for uc in
                UserConstituency.objects.filter(
                    user=self.request.user, active=True)
            ]
            return Ward.objects.filter(constituency_id__in=const_ids)

        if self.request.user.sub_county:
            const_ids = [
                us.sub_county.id for us in
                UserSubCounty.objects.filter(
                    user=self.request.user, active=True)
            ]
            return Ward.objects.filter(sub_county_id__in=const_ids)

        if self.request.user.county:
            county_ids = [
                uc.county.id for uc in UserCounty.objects.filter(
                    user=self.request.user, active=True)
            ]
            return Ward.objects.filter(constituency__county_id__in=county_ids)
        return Ward.objects.all()

    def get(self, request):
        fields = request.query_params.get('fields', None)
        fields_model_mapping = {
            'county': (County, ('id', 'name', )),
            'sub_county': (SubCounty, ('id', 'name', 'county', )),
            'facility_type': (FacilityType, ('id', 'name')),
            'constituency': (Constituency, ('id', 'name', 'county', )),
            'ward': (Ward, ('id', 'name', 'constituency', 'sub_county')),
            'operation_status': (FacilityStatus, ('id', 'name')),
            'chu_status': (chu_models.Status, ('id', 'name', )),
            'service_category': (ServiceCategory, ('id', 'name')),
            'owner_type': (OwnerType, ('id', 'name')),
            'owner': (Owner, ('id', 'name', 'owner_type')),
            'service': (Service, ('id', 'name', 'category')),
            'keph_level': (KephLevel, ('id', 'name')),
            'job_title': (JobTitle, ('id', 'name'))
        }
        if fields:
            resp = {}
            for key in fields.split(","):
                if key in fields_model_mapping:
                    model, chosen_fields = fields_model_mapping[key]
                    if model == County:
                        resp[key] = self.get_counties().values(
                            *chosen_fields).distinct()
                    elif model == Constituency:
                        resp[key] = self.get_constituencies().values(
                            *chosen_fields).distinct()
                    elif model == SubCounty:
                        resp[key] = self.get_sub_counties().values(
                            *chosen_fields).distinct()
                    elif model == Ward:
                        resp[key] = self.get_wards().values(
                            *chosen_fields).distinct()
                    else:
                        resp[key] = model.objects.values(
                            *chosen_fields).distinct()
            res = self.serializer_cls(data=resp).initial_data
        else:
            res = {}
        return response.Response(res)


class UserConstituencyListView(generics.ListCreateAPIView):
    serializer_class = UserConstituencySerializer
    filter_class = UserConstituencyFilter
    queryset = UserConstituency.objects.all()
    ordering_fields = ('user', 'constituency')


class UserConstituencyDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserConstituencySerializer
    queryset = UserConstituency.objects.all()


class DocumentUploadDetailView(
        AuditableDetailViewMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DocumentUploadSerializer
    queryset = DocumentUpload.objects.all()
    parser_classes = (parsers.JSONParser, parsers.MultiPartParser, XMLParser, )


class DocumentUploadListView(generics.ListCreateAPIView):
    serializer_class = DocumentUploadSerializer
    queryset = DocumentUpload.objects.all()
    filter_class = DocumentUploadFilter
    ordering_fields = ('name', )
    parser_classes = (parsers.JSONParser, parsers.MultiPartParser, XMLParser, )


class ErrorQueueListView(generics.ListCreateAPIView):
    """
    Mainly used to list the errors that occur when undertaking async tasks
    """

    serializer_class = ErrorQueueSerializer
    filter_class = ErrorQueueFilter
    queryset = ErrorQueue.objects.all()
    ordering_fields = ('app_label', )


class ErrorQueueDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieves a single error that occurred when performing an async task
    """

    serializer_class = ErrorQueueSerializer
    queryset = ErrorQueue.objects.all()
