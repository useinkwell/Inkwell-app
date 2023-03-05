from rest_framework.pagination import PageNumberPagination

class PostPaginationConfig(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 50

class CommentPaginationConfig(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000
    