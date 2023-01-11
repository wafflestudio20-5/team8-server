from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics
from .serializers import CourseListSerializer, ReviewListSerializer, ReviewDetailSerializer, CommentListSerializer, \
    CommentDetailSerializer
from .models import Course, Review, Comment


class CourseList(generics.ListAPIView):
    serializer_class = CourseListSerializer

    def get_queryset(self):
        parameters = {
            'grade': 'grade',
            'degree': 'degree',
            'college': 'college',
            'department': 'department',
            'curriculum': 'curriculum',
            'name__contains': 'keyword',
        }

        kwargs = {key: self.request.GET.get(value) for key, value in parameters.items() if self.request.GET.get(value)}
        queryset = Course.objects.filter(**kwargs)

        exception = self.request.GET.get('exception')
        if exception:
            q = Q()
            for exception_keyword in exception.split(','):
                q |= Q(name__contains=exception_keyword)
            queryset = queryset.exclude(q)

        return queryset


class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all().order_by('-created_at')
    serializer_class = ReviewListSerializer

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request.data['course'] = kwargs['id']
        request.data['created_at'] = timezone.now()

        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all().order_by('-created_at')
    serializer_class = ReviewDetailSerializer

    def get_object(self):
        return get_object_or_404(Review, id=self.kwargs['rid'])

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

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

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request.data['review'] = kwargs['rid']
        request.data['created_at'] = timezone.now()

        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentDetailSerializer

    def get_object(self):
        return get_object_or_404(Comment, id=self.kwargs['cid'])

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        request.data['review'] = kwargs['rid']
        request.data['updated_at'] = timezone.now()
        request.data['is_updated'] = True

        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
