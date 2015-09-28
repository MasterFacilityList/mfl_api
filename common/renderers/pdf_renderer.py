from django.template import loader, Context
from django.http import HttpResponse
from rest_framework import renderers
from .shared import DownloadMixin

from weasyprint import HTML
import cStringIO


class PDFRenderer(DownloadMixin, renderers.BaseRenderer):
    media_type = ('application/pdf')
    format = 'pdf'
    render_style = 'binary'
    extension = 'pdf'

    def render(self, data, media_type, renderer_context):
        self.update_download_headers(renderer_context)
        template = loader.get_template('pdf/pdf.html')

        context = Context({
            "data": data,
            "title": self.fname.split('.')[0],

        })

        mem_file = cStringIO.StringIO()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename={}.pdf'.format(
            mem_file
        )
        HTML(string=template.render(context)).write_pdf(response)
        return response
