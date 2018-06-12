from mock import patch
from requests.exceptions import ConnectionError
from django.test import TestCase
from django.test.utils import override_settings

from ..tasks import backup_db, refresh_material_views


class S3BucketMock(object):
    pass


class S3Mock(object):
    def __init__(self, *args, **kwargs):
        super(S3Mock, self).__init__(*args, **kwargs)

    def create_bucket(self, *args, **kwargs):
        return S3BucketMock()


@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.dummy.EmailBackend')
class TestCommonCeleryTasks(TestCase):
    def test_db_backup_success(self):
        with patch('fabfile.S3Connection') as s3_mock:
            s3_mock.return_value = S3Mock()

            with patch('fabfile.local') as fabric_local_mock:
                fabric_local_mock.return_value = None
                fabric_local_mock.side_effect = None
                backup_db()

    def test_db_backup_failure(self):
        with patch('fabfile.S3Connection') as s3_mock:
            s3_mock.return_value = S3Mock()
            s3_mock.side_effect = ConnectionError

            with patch('fabfile.local') as fabric_local_mock:
                fabric_local_mock.return_value = None
                fabric_local_mock.side_effect = None
                backup_db()

    def test_refresh_material_view(self):
        # The test is just for coverage purpose only
        refresh_material_views()
