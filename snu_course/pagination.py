from django.db.models import Sum, F
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class UserToCoursePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000

    def __init__(self):
        self.total_credit = None

    def paginate_queryset(self, queryset, request, view=None):
        self.total_credit = queryset.aggregate(Sum(F('course__credit')))['course__credit__sum']
        if not self.total_credit:
            self.total_credit = 0
        return super().paginate_queryset(queryset, request, view=view)

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'total_credit': self.total_credit,
            'results': data,
        })


class CoursePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000


class ReviewPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000


class CommentPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000