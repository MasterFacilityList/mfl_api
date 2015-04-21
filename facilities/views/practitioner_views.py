from rest_framework import generics

from ..models import (
    PracticeType,
    Speciality,
    Qualification,
    Practitioner,
    PractitionerQualification,
    PractitionerContact,
    PractitionerFacility
)


from ..serializers import (
    PracticeTypeSerializer,
    SpecialitySerializer,
    QualificationSerializer,
    PractitionerSerializer,
    PractitionerQualificationSerializer,
    PractitionerContactSerializer,
    PractitionerFacilitySerializer,
)


from ..filters import (
    PracticeTypeFilter,
    SpecialityFilter,
    QualificationFilter,
    PractitionerFilter,
    PractitionerQualificationFilter,
    PractitionerContactFilter,
    PractitionerFacilityFilter
)


class PracticeTypeListView(generics.ListCreateAPIView):
    queryset = PracticeType.objects.all()
    serializer_class = PracticeTypeSerializer
    filter_class = PracticeTypeFilter
    ordering_fields = ('name', 'description', )


class PracticeTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PracticeType.objects.all()
    serializer_class = PracticeTypeSerializer


class SpecialityListView(generics.ListCreateAPIView):
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer
    filter_class = SpecialityFilter
    ordering_fields = ('name', 'practice_type',)


class SpecialityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer


class QualificationListView(generics.ListCreateAPIView):
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializer
    filter_class = QualificationFilter
    ordering_fields = ('name', 'description', )


class QualificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializer


class PractitionerListView(generics.ListCreateAPIView):
    queryset = Practitioner.objects.all()
    serializer_class = PractitionerSerializer
    filter_class = PractitionerFilter
    ordering_fields = ('name', 'registration_number', )


class PractitionerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Practitioner.objects.all()
    serializer_class = PractitionerSerializer


class PractitionerQualificationListView(generics.ListCreateAPIView):
    queryset = PractitionerQualification.objects.all()
    serializer_class = PractitionerQualificationSerializer
    filter_class = PractitionerQualificationFilter
    ordering_fields = ('practitioner', 'qualification')


class PractitionerQualificationDetailView(
        generics.RetrieveUpdateDestroyAPIView):
    queryset = PractitionerQualification.objects.all()
    serializer_class = PractitionerQualificationSerializer


class PractitionerContactListView(generics.ListCreateAPIView):
    queryset = PractitionerContact.objects.all()
    serializer_class = PractitionerContactSerializer
    filter_class = PractitionerContactFilter
    ordering_fields = ('practitioner', 'contact',)


class PractitionerContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PractitionerContact.objects.all()
    serializer_class = PractitionerContactSerializer


class PractitionerFacilityListView(generics.ListCreateAPIView):
    queryset = PractitionerFacility.objects.all()
    filter_class = PractitionerFacilityFilter
    ordering_fields = ('practitioner', 'facility', )
    serializer_class = PractitionerFacilitySerializer


class PractitionerFacilityDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PractitionerFacility.objects.all()
    serializer_class = PractitionerFacilitySerializer
