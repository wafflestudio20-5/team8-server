from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response

from .pagination import CoursePagination, ReviewPagination, CommentPagination
from .permissions import IsSafeOrAuthorizedUser, IsCreator, IsSafeOrAdminUser
from .serializers import CourseListSerializer, ReviewListSerializer, ReviewDetailSerializer, CommentListSerializer, \
    CommentDetailSerializer, CourseDetailSerializer
from .models import Course, Review, Comment


class CourseListCreateView(generics.ListCreateAPIView):
    SEARCH_PARAMETERS = {
        'grade': 'grade',
        'degree': 'degree',
        'college': 'college',
        'department': 'department',
        'curriculum': 'curriculum',
        'keyword': 'name__contains',
        'exception': None,
    }

    serializer_class = CourseListSerializer
    permission_classes = [IsSafeOrAuthorizedUser]
    pagination_class = CoursePagination

    def get_queryset(self):
        kwargs = {key: self.request.GET.get(attr)
                  for attr, key in self.SEARCH_PARAMETERS.items()
                  if self.request.GET.get(attr)
                  if key}
        queryset = Course.objects.filter(**kwargs)

        exception = self.request.data.get('exception')
        if exception:
            q = Q()
            for exception_keyword in exception.split(','):
                q |= Q(name__contains=exception_keyword)
            queryset = queryset.exclude(q)

        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data.update({attr: self.request.GET.get(attr)
                              for attr in self.SEARCH_PARAMETERS
                              if self.request.GET.get(attr)})
        return response


class CourseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = [IsSafeOrAdminUser]

    def get_object(self):
        obj = get_object_or_404(Course, id=self.kwargs['id'])
        self.check_object_permissions(self.request, obj)
        return obj


class ReviewListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsSafeOrAuthorizedUser]
    queryset = Review.objects.all().order_by('-created_at')
    serializer_class = ReviewListSerializer
    pagination_class = ReviewPagination

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        for serialized_review in serializer.data:
            if request.user.is_anonymous or serialized_review['created_by'] != request.user.name:
                serialized_review['created_by'] = None

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        request.data['course'] = kwargs['id']
        request.data['created_at'] = timezone.now()

        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all().order_by('-created_at')
    serializer_class = ReviewDetailSerializer
    permission_classes = [IsCreator]

    def get_object(self):
        obj = get_object_or_404(Review, id=self.kwargs['rid'])
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        serialized_review = serializer.data

        if request.user.is_anonymous or serialized_review['created_by'] != request.user.name:
            serialized_review['created_by'] = None

        return Response(serialized_review)

    def update(self, request, *args, **kwargs):
        request.data['course'] = kwargs['id']
        request.data['updated_at'] = timezone.now()
        request.data['is_updated'] = True

        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentListSerializer
    permission_classes = [IsSafeOrAuthorizedUser]
    pagination_class = CommentPagination

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        for serialized_comment in serializer.data:
            if request.user.is_anonymous:
                serialized_comment['created_by'] = None
            elif serialized_comment['created_by'] != request.user.name:
                serialized_comment['created_by'] = None

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        request.data['review'] = kwargs['rid']
        request.data['created_at'] = timezone.now()

        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentDetailSerializer
    permission_classes = [IsCreator]

    def get_object(self):
        obj = get_object_or_404(Comment, id=self.kwargs['cid'])
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        serialized_comment = serializer.data

        if request.user.is_anonymous or serialized_comment['created_by'] != request.user.name:
            serialized_comment['created_by'] = None

        return Response(serialized_comment)

    def update(self, request, *args, **kwargs):
        request.data['review'] = kwargs['rid']
        request.data['updated_at'] = timezone.now()
        request.data['is_updated'] = True

        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
