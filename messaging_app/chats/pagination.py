from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"  # optionally allow clients to change up to a max
    max_page_size = 100
