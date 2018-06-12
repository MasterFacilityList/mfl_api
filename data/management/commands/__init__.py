import os

from django.conf import settings


def _get_file_path(fname):
    return os.path.join(
        settings.BASE_DIR, "data/new_data/v2_data/users_and_groups", fname)
