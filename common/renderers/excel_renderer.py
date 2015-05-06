import xlsxwriter
from six import StringIO
import os
from django.conf import settings


from rest_framework import renderers


class ExcelRenderer(renderers.BaseRenderer):
    media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  # noqa
    format = 'excel'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        file_name = self._write_excel(data)
        in_mem_file = StringIO()
        file_path = os.path.join(settings.BASE_DIR, file_name)
        with open(file_path, 'r') as excel_file:
            file_data = excel_file.read()
            in_mem_file.write(file_data)
        return in_mem_file.getvalue()

    def _write_excel(self, data):
        result = data.get('results')
        work_book_name = 'human.xlsx'
        workbook = xlsxwriter.Workbook(work_book_name)
        worksheet = workbook.add_worksheet()
        row = 0
        col = 0
        data_dict = result[0]
        data_keys = data_dict.keys()
        for key in data_keys:
            worksheet.write(row, col, key)
            col = col + 1
        row = 1
        col = 0
        for data_dict in result:
            for key in data_keys:
                worksheet.write(row, col, data_dict[key])
                col = col + 1
            row = row + 1
        workbook.close()
        return work_book_name
