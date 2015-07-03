import os
import json

from django.db import transaction
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand
from users.models import MflUser


class Command(BaseCommand):

    def _load_group_permissions(self, group_permissions):
        with transaction.atomic():
            for gp in group_permissions:
                g = Group.objects.get(**gp["group"])
                for p in gp["permissions"]:
                    g.permissions.add(Permission.objects.get(**p))

    def _load_user_groups(self, user_groups):
        with transaction.atomic():
            for ug in user_groups:
                u = MflUser.objects.get(**ug["mfluser"])
                for g in ug["groups"]:
                    u.groups.add(Group.objects.get(**g))

    def _get_file(self, fname):
        return os.path.join(settings.BASE_DIR, "data/data", fname)

    def handle(self, *args, **options):

        with open(self._get_file("1001_user_groups.json"), "rt") as f:
            self._load_user_groups(json.load(f))

        with open(self._get_file("1002_group_permissions.json"), "rt") as f:
            self._load_group_permissions(json.load(f))
