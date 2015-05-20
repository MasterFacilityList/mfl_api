import xlsxwriter
import json

from django.conf import settings
from common.utilities.search_utils import default


from rest_framework import renderers


def remove_keys(sample_list):
    """
    Removes keys that should not be in excel
    """
    for key in sample_list:
        if key in settings.EXCEL_EXCEPT_FIELDS:
            key_index = sample_list.index(key)
            del sample_list[key_index]
    return sample_list


def _write_excel_file(data):
        data = json.loads(json.dumps(data, default=default))
        result = data.get('results')

        work_book_name = 'download.xlsx'
        workbook = xlsxwriter.Workbook(work_book_name)
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

            worksheet.set_row(0, 70)
            worksheet.set_column('A:A', 30)
            worksheet.set_column('A:B', 30)
            worksheet.set_column('A:C', 30)
            worksheet.set_column('A:D', 30)
            worksheet.set_column('A:E', 30)
            worksheet.set_column('A:F', 30)
            worksheet.set_column('A:G', 30)
            worksheet.set_column('A:H', 30)
            worksheet.set_column('A:I', 30)
            worksheet.set_column('A:J', 30)
            worksheet.set_column('A:K', 30)

            row = 0
            col = 0
            if len(work_sheet_data) > 1:
                example_dict = work_sheet_data[0]
                sample_keys = example_dict.keys()

                # remove columns that should not be excel
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
                            worksheet.write(row, col, data_dict.get(key))
                            col = col + 1
                        else:
                            _add_data_to_worksheet(
                                data.get(key)) if data.get(key) else None

                    col = 0
                    row = row + 1

            else:
                # the count is zero thus do not write the excel file
                pass

        _add_data_to_worksheet(result)
        workbook.close()

        return work_book_name


class ExcelRenderer(renderers.BaseRenderer):
    media_type = 'text/plain'  # noqa
    format = 'excel'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        file_name = _write_excel_file(data)
        return file_name
