import json
import os
import logging

from django.db import transaction
from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand
from django.conf import settings
from users.models import CustomGroup, MflUser

from . import _get_file_path

Logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def _load_group_permissions(self, group_permissions):
        with transaction.atomic():
            for gp in group_permissions:

                g = Group.objects.get(**gp["group"])
                g.permissions.clear()
                for perm in gp["permissions"]:
                    g.permissions.add(Permission.objects.get(**perm))

    def _annotate_groups_with_booleans(self):
        file_path = 'data/data/v2_data/0102_group_booleans'
        full_file_path = os.path.join(settings.BASE_DIR, file_path)
        with open(full_file_path) as data_file:
            data = data_file.read()
            data = json.loads(data)
            for record in data:
                record['group'] = Group.objects.get(name=record['group'])
                CustomGroup.objects.get_or_create(**record)

    def _assign_user_groups(self):
        file_path = 'data/data/v2_data/users_and_groups/1001_user_groups.json'
        full_file_path = os.path.join(settings.BASE_DIR, file_path)
        with open(full_file_path) as data_file:
            data = data_file.read()
            data = json.loads(data)
            for record in data:
                user_email = record.get('mfluser').get('email')
                try:
                    user = MflUser.objects.get(email=user_email)
                    groups = record.get('groups')
                    for group in groups:
                        group_obj = Group.objects.get(name=group.get('name'))
                        user.groups.add(group_obj)
                except MflUser.DoesNotExist:
                    continue
                Logger.info("User with email {} does not exist".format(
                    user_email))

    def handle(self, *args, **options):
        with open(_get_file_path("1002_group_permissions.json"), "rt") as f:
            self._load_group_permissions(json.load(f))

        self._annotate_groups_with_booleans()
        self._assign_user_groups()
