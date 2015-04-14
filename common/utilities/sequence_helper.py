import logging

from django.db import connection

LOGGER = logging.getLogger(__name__)


class SequenceGenerator(object):

    def __init__(self, model):
        options = model._meta
        self.sequence_name = options.app_label + "_" + options.model_name \
            + "_document_code_seq"

    def next(self):
        query = "SELECT nextval('%s')" % self.sequence_name
        with connection.cursor() as cur:
            cur.execute(query)
            row = cur.fetchone()
            return row[0]
