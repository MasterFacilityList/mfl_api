from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission
from users.models import MflUser


def get_particular_type_of_permission(perm_type, perms):
    matching_perms = []
    for perm in perms:
        if perm.codename.find(perm_type) and perm not in matching_perms:
            matching_perms.append(perm)
    return matching_perms


class Command(BaseCommand):

    def handle(self, *args, **options):
        chrio = Group.objects.get(
            name="County Health Records Information Officer")

        schrio = Group.objects.get(
            name="Sub County Health Records Information Officer")

        national = Group.objects.get(
            name="National Administrators")
        county_admins = Group.objects.get(
            **{"name": "County Administrators"})

        public = Group.objects.get(
            name="Public Users")

        publishers = Group.objects.get(
            name="Publishers")

        regulator_makers = Group.objects.get(
            name="Regulators (makers)")

        regulator_approvers = Group.objects.get(
            name="Regulators (Approvers)")

        for perm in Permission.objects.all():
            national.permissions.add(perm.id)

        user_permisssions = Permission.objects.filter(
            content_type__app_label='user')
        auth_permissions = Permission.objects.filter(
            content_type__app_label='auth')
        facilities_permissions = Permission.objects.filter(
            content_type__app_label='facilities')
        town_permissions = Permission.objects.filter(
            content_type__model='town')
        service_rating_perms = Permission.objects.filter(
            content_type__model='facilityservicerating')
        facility_approval_perms = Permission.objects.filter(
            content_type__model='facilityapproval')
        facility_op_status_perms = Permission.objects.filter(
            content_type__model='facilityapproval')
        gis_perms = Permission.objects.filter(
            content_type__app_label='mfl_gis')
        common_perms = Permission.objects.filter(
            content_type__app_label='common_perms')
        facility_reg_status_perms = Permission.objects.filter(
            content_type__model='facilityregulationstatus')
        facility_unit_reg_status_perms = Permission.objects.filter(
            content_type__model='facilityunitregulation')

        # county admin perms
        # towns CRUD
        # users CRUD and Groups

        [county_admins.permissions.add(perm.id)for perm in auth_permissions]
        [county_admins.permissions.add(perm.id)for perm in town_permissions]
        [county_admins.permissions.add(perm.id)for perm in user_permisssions]

        # chrios permissions
        [chrio.permissions.add(perm.id)for perm in facilities_permissions]
        [chrio.permissions.add(perm.id)for perm in facility_approval_perms]
        [county_admins.permissions.add(perm.id)for
            perm in facility_op_status_perms]

        # public permissions
        [public.permissions.add(perm.id)for
            perm in get_particular_type_of_permission(
            'view', facilities_permissions)]

        [public.permissions.add(perm.id) for
            perm in get_particular_type_of_permission(
            'add', service_rating_perms)]

        [public.permissions.add(perm.id)for
            perm in get_particular_type_of_permission(
            'view', service_rating_perms)]

        [public.permissions.add(perm.id)for perm
            in get_particular_type_of_permission('view', common_perms)]

        [public.permissions.add(perm.id)for
            perm in get_particular_type_of_permission('view', gis_perms)]

        # publishers
        [publishers.permissions.add(perm.id) for
            perm in get_particular_type_of_permission(
            'view', facilities_permissions)]
        [publishers.permissions.add(perm.id) for
            perm in get_particular_type_of_permission(
            'publish', facilities_permissions)]

        # regulators makers
        [regulator_makers.permissions.add(perm.id) for
            perm in get_particular_type_of_permission(
            'view', facilities_permissions)]
        [regulator_makers.permissions.add(perm.id) for
            perm in facility_unit_reg_status_perms]
        [regulator_makers.permissions.add(perm.id) for
            perm in facility_reg_status_perms]

        # regulators approvers
        [regulator_approvers.permissions.add(perm.id) for
            perm in get_particular_type_of_permission(
            'view', facilities_permissions)]
        [regulator_approvers.permissions.add(perm.id) for
            perm in facility_unit_reg_status_perms]

        # schrio
        [schrio.permissions.add(perm.id) for
            perm in facilities_permissions]

        for user in MflUser.objects.all():
            if user.regulator:
                user.groups.add(regulator_makers.id)
                user.groups.add(regulator_approvers.id)
                continue
            elif user.is_staff and not user.county:
                user.groups.add(national.id)
                continue
            elif user.constituency:
                user.groups.add(schrio.id)
                continue
            elif user.county and not user.is_staff:
                user.groups.add(chrio.id)
                continue
            elif user.county and user.is_staff:
                user.groups.add(county_admins.id)
                continue
            elif user.is_national and not user.is_staff and not user.regulator:
                user.groups.add(publishers.id)
            else:
                user.groups.add(public.id)
