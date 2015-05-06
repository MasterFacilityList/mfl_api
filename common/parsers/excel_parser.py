import xlsxwriter

from rest_framework.parsers import BaseParser


class ExcelParser(BaseParser):
    """

    """

    media_type = 'file/excel'

    def parse(self, stream, media_type=None, parser_context=None):

        return stream.read()
