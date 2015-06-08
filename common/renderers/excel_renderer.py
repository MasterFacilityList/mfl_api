import xlsxwriter
import string
import cStringIO
import uuid
import json

from django.conf import settings

from rest_framework import renderers

from .shared import DownloadMixin


def remove_keys(sample_list):
    """
    Removes keys that should not be in excel e.g PKs and audit fields
    """
    return [
        item for item in sample_list
        if item not in settings.EXCEL_EXCEPT_FIELDS]


def _write_excel_file(data):
    result = data.get('results')
    mem_file = cStringIO.StringIO()
    workbook = xlsxwriter.Workbook(mem_file)
    format = workbook.add_format(
        {
            'bold': True,
            'font_color': 'black',
            'font_size': 15
        })
    format.set_align('center')
    format.set_align('vcenter')

    def _add_data_to_worksheet(work_sheet_data):
        worksheet = workbook.add_worksheet()
        chars = string.ascii_uppercase

        # format the column titles
        worksheet.set_row(0, 50)
        [worksheet.set_column('A:{}'.format(char), 30) for char in chars]

        row = 0
        col = 0
        if len(work_sheet_data) > 1:
            example_dict = work_sheet_data[0]
            sample_keys = example_dict.keys()

            # remove columns that should not be in excel
            sample_keys = remove_keys(sample_keys)

            for key in sample_keys:
                key = key.replace('_', " ")
                worksheet.write(row, col, key, format)
                col = col + 1
            row = 1
            col = 0
            for data_dict in work_sheet_data:
                data_keys = data_dict.keys()
                # remove colums that should not be in excel
                data_keys = remove_keys(data_keys)

                for key in data_keys:
                    if not isinstance(data_dict.get(key), list):
                        try:
                            uuid.UUID(str(data_dict.get(key)))
                        except ValueError:
                            worksheet.write(row, col, str(data_dict.get(key)))
                        col = col + 1
                    else:
                        # write sheets to new work sheets
                        col = col + 1

                col = 0
                row = row + 1

        else:
            # the count is zero thus do not write the excel file
            pass

    _add_data_to_worksheet(result)
    workbook.close()
    mem_file_contents = mem_file.getvalue()
    mem_file.close()

    return mem_file_contents


class ExcelRenderer(DownloadMixin, renderers.BaseRenderer):
    media_type = ('application/vnd.openxmlformats'
                  '-officedocument.spreadsheetml.sheet')
    format = 'excel'
    render_style = 'binary'
    extension = 'xlsx'

    def render(self, data, media_type, renderer_context):
        self.update_download_headers(renderer_context)
        resullt_key = data.get('results', None)
        if resullt_key:
            return _write_excel_file(data)
        else:
            # For now we will just support list endpoints.
            return json.dumps({
                "detail": "malformed payload. It should be a list endpoint"
            })
