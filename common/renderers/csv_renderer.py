from rest_framework_csv import renderers as csv_renderers

from .shared import DownloadMixin


class CSVRenderer(DownloadMixin, csv_renderers.CSVRenderer):

    """Subclassed just to add content-disposition header"""

    extension = 'csv'

    def render(self, data, media_type=None, renderer_context=None):
        self.update_download_headers(renderer_context)
        is_list = self.check_list_output(data, renderer_context)
        if is_list is not True:
            return is_list

        return super(CSVRenderer, self).render(
            data['results'], media_type=media_type,
            renderer_context=renderer_context
        )
