import json

from django.contrib.auth.models import Group
from django.core.management import BaseCommand
from users.models import MflUser

from . import _get_file_path


class Command(BaseCommand):

    def _dump_group_permissions(self):
        return [
            {
                "group": {"name": g.name},
                "permissions": [
                    {"codename": p.codename}
                    for p in g.permissions.all()
                ]
            }
            for g in Group.objects.all()
        ]

    def _dump_user_groups(self):
        return [
            {
                "mfluser": {"email": u.email},
                "groups": [
                    {"name": g.name}
                    for g in u.groups.all()
                ]
            }
            for u in MflUser.objects.all()
        ]

    def handle(self, *args, **options):
        with open(_get_file_path("1001_user_groups.json"), "wt") as f:
            json.dump(self._dump_user_groups(), f, indent=4)

        with open(_get_file_path("1002_group_permissions.json"), "wt") as f:
            json.dump(self._dump_group_permissions(), f, indent=4)
