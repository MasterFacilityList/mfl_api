import xlsxwriter
import json

from common.utilities.search_utils import default


from rest_framework import renderers


def _write_excel_file(data):
        data = json.loads(json.dumps(data, default=default))
        result = data.get('results')

        work_book_name = 'download.xlsx'
        workbook = xlsxwriter.Workbook(work_book_name)

        def _add_data_to_worksheet(work_sheet_data):
            worksheet = workbook.add_worksheet()
            row = 0
            col = 0
            if len(work_sheet_data) > 1:
                example_dict = work_sheet_data[0]
                sample_keys = example_dict.keys()
                for key in sample_keys:
                    worksheet.write(row, col, key)
                    col = col + 1
                row = 1
                col = 0
                for data_dict in work_sheet_data:
                    data_keys = data_dict.keys()
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
