import xlsxwriter
import os
from django.conf import settings


from rest_framework import renderers


def _write_excel_file(data):
        result = data.get('results')
        work_book_name = 'download.xlsx'
        workbook = xlsxwriter.Workbook(work_book_name)

        def _add_data_to_worksheet(work_sheet_data):
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
                    if not isinstance(data[key], list):
                        worksheet.write(row, col, data_dict[key])
                        col = col + 1
                    else:
                        # wirte the nested lists to their own sheets
                        _add_data_to_worksheet(data[key])

                row = row + 1
        workbook.close()
        _add_data_to_worksheet(result)

        return work_book_name


class ExcelRenderer(renderers.BaseRenderer):
    media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'  # noqa
    format = 'excel'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        file_name = _write_excel_file(data)
        file_path = os.path.join(settings.BASE_DIR, file_name)
        with open(file_path, 'r') as excel_file:
            file_data = excel_file.read()
        return file_data
