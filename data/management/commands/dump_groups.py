import os
import json

from django.db import transaction
from django.conf import settings
from django.contrib.auth.models import Group
from django.core.management import BaseCommand
from users.models import MflUser


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

    def _get_file(self, fname):
        return os.path.join(settings.BASE_DIR, "data/data", fname)

    def handle(self, *args, **options):
        with open(self._get_file("1001_user_groups.json"), "wt") as f:
            json.dump(self._dump_user_groups(), f, indent=4)

        with open(self._get_file("1002_group_permissions.json"), "wt") as f:
            json.dump(self._dump_group_permissions(), f, indent=4)
