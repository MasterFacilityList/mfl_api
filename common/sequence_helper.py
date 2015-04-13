import logging

from django.db import connection

LOGGER = logging.getLogger(__name__)


def next_value_in_sequence(sequence_name):
    query = "SELECT nextval('%s')" % sequence_name
    with connection.cursor() as cur:
        cur.execute(query)
        row = cur.fetchone()
        return row[0]
