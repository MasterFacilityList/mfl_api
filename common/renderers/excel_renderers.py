import xlsxwriter

from rest_framework import renderers


class ExcelRenderer(renderers.BaseRenderer):
    media_type = 'application/excel'
    format = 'excel'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if data is None:
            return ''
        else:
            self._write_excel(data)

    def _write_excel(self, data):
        result = data.get('result')
        work_book_name = 'excel_files/human.xlsx'
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

        return work_book_name
