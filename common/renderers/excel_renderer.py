import xlsxwriter
import string
import cStringIO
import uuid

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


def _build_name_from_list(name_list):
    """
    Given a list joins the items in the list together
    and returns a space separated string
    """
    if len(name_list) == 1:
        return name_list[0]
    else:
        return " ".join(name_list)


def sanitize_field_names(sample_keys):
    """
    Creates user friendly names for inlined serializer fields.

    For example:
        1. A name such as regulatory_status_name the name part is
           stripped and 'regulatory status' will be used instead
        2. For name such as is_approved the is part is removed
           and approved left
    """
    key_map = []
    for key in sample_keys:
        new_name = key.split('_')
        if new_name[len(new_name) - 1] == 'name' and key != "name":
            mapping_name = _build_name_from_list(new_name[0:len(new_name) - 1])
            key_map.append({
                "actual": key,
                "preferred": mapping_name
            })
        elif new_name[0].lower() == 'is':
            mapping_name = _build_name_from_list(new_name[1:len(new_name)])
            key_map.append({
                "actual": key,
                "preferred": mapping_name
            })
        else:
            key_map.append({
                "actual": key,
                "preferred": key
            })
    return key_map


def _write_excel_file(data):  # noqa
    mem_file = cStringIO.StringIO()
    workbook = xlsxwriter.Workbook(mem_file)
    format = workbook.add_format(
        {
            'bold': True,
            'font_color': 'black',
            'font_size': 12
        })

    def _add_data_to_worksheet(work_sheet_data):
        worksheet = workbook.add_worksheet()
        chars = string.ascii_uppercase

        # format the column titles
        worksheet.set_row(0, 50)
        [worksheet.set_column('A:{}'.format(char), 30) for char in chars]

        row = 0
        col = 0
        if len(work_sheet_data) >= 1:
            example_dict = work_sheet_data[0]
            sample_keys = example_dict.keys()

            # remove columns that should not be in excel
            sample_keys = remove_keys(sample_keys)

            # find uuid fields and remove them from data
            data = work_sheet_data[0]
            reject_keys = []
            cleaned_fields = []
            for key in sample_keys:
                try:
                    uuid.UUID(str(data.get(key)))
                    reject_keys.append(key)
                except ValueError:
                    cleaned_fields.append(key)

            sample_keys = cleaned_fields

            # remove data with uuid fields
            for data in work_sheet_data:
                for key in reject_keys:
                    del data[key]

            # write the excel column names
            sample_keys_map = sanitize_field_names(sample_keys)
            for key in sample_keys_map:
                worksheet.write(
                    row, col, key.get("preferred").capitalize(), format)
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
                            cell_data = data_dict.get(key)

                            if cell_data is True:
                                cell_data = "Yes"

                            if cell_data is False:
                                cell_data = "No"
                            try:
                                worksheet.write(
                                    row,
                                    col,
                                    cell_data.encode(
                                        "utf-8").strip().decode("utf-8"))
                            except AttributeError:
                                worksheet.write(
                                    row,
                                    col,
                                    str(cell_data).decode("utf-8"))
                        col = col + 1
                    else:
                        # write sheets to new work sheets
                        col = col + 1

                col = 0
                row = row + 1

        else:
            # the count is zero thus do not write the excel file
            pass

    _add_data_to_worksheet(data)
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
        is_list = self.check_list_output(data, renderer_context)
        if is_list is not True:
            return is_list

        return _write_excel_file(data['results'])
