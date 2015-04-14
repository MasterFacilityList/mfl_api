import logging

from django.db import connection

LOGGER = logging.getLogger(__name__)


class SequenceGenerator(object):

    def __init__(self, app_label, model_name):
        self.sequence_name = app_label + "_" + model_name + "_code_seq"

    def next(self):
        query = "SELECT nextval('%s')" % self.sequence_name
        with connection.cursor() as cur:
            cur.execute(query)
            row = cur.fetchone()
            return row[0]
