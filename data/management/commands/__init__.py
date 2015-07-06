import os

from django.conf import settings


def _get_file_path(fname):
    return os.path.join(settings.BASE_DIR, "data/data", fname)
