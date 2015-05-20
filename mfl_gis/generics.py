from rest_framework_extensions.etag.decorators import etag
from rest_framework.generics import ListCreateAPIView


class GISListCreateAPIView(ListCreateAPIView):

    @etag()
    def get(self, request, *args, **kwargs):
        """"""
        return self.list(request, *args, **kwargs)
