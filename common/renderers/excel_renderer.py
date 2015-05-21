import xlsxwriter
import json
import string
import cStringIO
import uuid

from django.conf import settings
from rest_framework import renderers
from rest_framework_csv import renderers as csv_renderers
from common.utilities.search_utils import default


def remove_keys(sample_list):
    """
    Removes keys that should not be in excel e.d ids and audit fields
    """
    new_set = set(sample_list) - set(settings.EXCEL_EXCEPT_FIELDS)
    return [item for item in new_set]


def _write_excel_file(data):
    data = json.loads(json.dumps(data, default=default))
    result = data.get('results')

    # work_book_name = 'download.xlsx'
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
                            uuid.UUID(data_dict.get(key))
                        except:
                            worksheet.write(row, col, data_dict.get(key))
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


class ExcelRenderer(renderers.BaseRenderer):
    media_type = ('application/vnd.openxmlformats'
                  '-officedocument.spreadsheetml.sheet')
    format = 'excel'
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        view = renderer_context.get('view', None)
        if view is not None:
            fname = view.get_view_name() or 'download'
            view.response._headers['content-disposition'] = (
                'Content-Disposition',
                'attachment; filename="{}.xlsx"'.format(fname)
            )

        return _write_excel_file(data)


class CSVRenderer(csv_renderers.CSVRenderer):
    """Subclassed just to add content-disposition header"""

    def render(self, data, media_type=None, renderer_context=None):
        view = renderer_context.get('view', None)
        if view is not None:
            fname = view.get_view_name() or 'download'
            view.response._headers['content-disposition'] = (
                'Content-Disposition',
                'attachment; filename="{}.csv"'.format(fname)
            )
        return super(CSVRenderer, self).render(
            data['results'], media_type=media_type, renderer_context=renderer_context
        )
