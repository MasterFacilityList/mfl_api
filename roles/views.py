from rest_framework import generics

from common.views import FilterViewMixin

from .models import (
    Role, Permission, RolePermissions, UserRoles)

from .serializers import(
    PermissionSerializer, RoleSerializer, RolePermissionPostSerializer,
    UserRolesSerializer)


class RolesList(FilterViewMixin, generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class RoleDetailView(FilterViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    lookup_field = 'id'


class PermissionsList(FilterViewMixin, generics.ListCreateAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class PermissionDetailView(
        FilterViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    lookup_field = 'id'


class RolePermissionsList(FilterViewMixin, generics.ListCreateAPIView):
    queryset = RolePermissions.objects.all()
    serializer_class = RolePermissionPostSerializer
    filter_fields = ('role',)


class RolePermissionDetailView(
        FilterViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = RolePermissions.objects.all()
    serializer_class = RolePermissionPostSerializer
    lookup_field = 'id'


class UserRolesList(FilterViewMixin, generics.ListCreateAPIView):
    queryset = UserRoles.objects.all()
    serializer_class = UserRolesSerializer
    filter_fields = ('user', 'role',)


class UserRoleDetailView(
        FilterViewMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = UserRoles.objects.all()
    serializer_class = UserRolesSerializer
    lookup_field = 'id'
