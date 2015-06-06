from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission
from users.models import MflUser


class Command(BaseCommand):

    def handle(self, *args, **options):
        chrio, created = Group.objects.get_or_create(
            name="County Health Records Information Officer")

        schrio, created = Group.objects.get_or_create(
            name="Sub County Health Records Information Officer")
        national, created = Group.objects.get_or_create(
            name="National Users")
        for perm in Permission.objects.all():
            national.permissions.add(perm.id)

        national_user = MflUser.objects.get(
            email='national@mfltest.slade360.co.ke')
        national_user.groups.add(national)
        chrio_user = MflUser.objects.get(
            email='chrio@mfltest.slade360.co.ke')
        chrio_user.groups.add(chrio)
        schrio_user = MflUser.objects.get(
            email='schrio@mfltest.slade360.co.ke')
        schrio_user.groups.add(schrio)
        mombasa_user = MflUser.objects.get(
            email='mombasa@mfltest.slade360.co.ke')
        mombasa_user.groups.add(chrio)
        kilifi_user = MflUser.objects.get(
            email='kilifi@mfltest.slade360.co.ke')
        kilifi_user.groups.add(chrio)
        tanriver_user = MflUser.objects.get(
            email='tanariver@mfltest.slade360.co.ke')
        tanriver_user.groups.add(chrio)
        narok_user = MflUser.objects.get(
            email='narok@mfltest.slade360.co.ke')
        narok_user.groups.add(chrio)
        nairobi_user = MflUser.objects.get(
            email='nairobi@mfltest.slade360.co.ke')
        nairobi_user.groups.add(chrio)
