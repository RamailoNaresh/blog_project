from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "size"
    max_page_size = 100


def paginate(queryset, request):
    paginate = Pagination()
    paginated_queryset = paginate.paginate_queryset(queryset, request)
    page_info = {
        "count" : paginate.page.paginator.count,
        "page" : paginate.page.number,
        "pages" : paginate.page.paginator.num_pages,
        "next" : paginate.get_next_link(),
        "previous" : paginate.get_previous_link()
    }

    return paginated_queryset, page_info