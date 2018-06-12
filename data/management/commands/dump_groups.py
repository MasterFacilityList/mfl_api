import json

from django.contrib.auth.models import Group
from django.core.management import BaseCommand

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

    def handle(self, *args, **options):
        with open(_get_file_path("1002_group_permissions.json"), "wt") as f:
            json.dump(self._dump_group_permissions(), f, indent=4)
