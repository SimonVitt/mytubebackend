from rest_framework.pagination import PageNumberPagination

class VideosPageNumberPagination(PageNumberPagination):
    page_size = 4
