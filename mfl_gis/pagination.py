from rest_framework.pagination import PageNumberPagination


class GISPageNumberPagination(PageNumberPagination):
    page_size = 1500  # Show all wards at once
