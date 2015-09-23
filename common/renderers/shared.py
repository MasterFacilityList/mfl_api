import json

from rest_framework.status import HTTP_406_NOT_ACCEPTABLE

"""
Objects that are shared among the renderers
"""


class DownloadMixin(object):
    extension = None

    def check_list_output(self, data, renderer_context):
        if isinstance(data.get('results', None), (list, )):
            return True

        # For now we will just support list endpoints.
        renderer_context['response'].status_code = HTTP_406_NOT_ACCEPTABLE
        return json.dumps({
            "detail": "Excel format are only used in list endpoints"
        })

    def update_download_headers(self, renderer_context):
        view = renderer_context.get('view')
        fname = view.get_view_name() or 'download'

        fname = "{}.{}".format(fname, self.extension)
        view.response._headers['content-disposition'] = (
            'Content-Disposition',
            'attachment; filename="{}"'.format(fname)
        )
