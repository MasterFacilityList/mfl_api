from rest_framework.pagination import PageNumberPagination


class GISPageNumberPagination(PageNumberPagination):

    def get_page_size(self, request):
        """Impractically high limit; ensures we always return all boundaries"""
        return 1500000
