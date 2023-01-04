from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics

from .permissions import IsSafeOrAuthorizedUser, IsCreator, IsSafeOrAdminUser
from .serializers import CourseListSerializer, ReviewListSerializer, ReviewDetailSerializer, CommentListSerializer, \
    CommentDetailSerializer, CourseDetailSerializer
from .models import Course, Review, Comment


class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all().prefetch_related('review_set').order_by('name')
    serializer_class = CourseListSerializer
    permission_classes = [IsSafeOrAdminUser]


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
    permission_classes = [IsCreator]

    def get_object(self):
        obj = get_object_or_404(Review, id=self.kwargs['rid'])
        self.check_object_permissions(self.request, obj)
        return obj

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
    permission_classes = [IsSafeOrAuthorizedUser]

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
    permission_classes = [IsCreator]

    def get_object(self):
        obj = get_object_or_404(Comment, id=self.kwargs['cid'])
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        request.data['review'] = kwargs['rid']
        request.data['updated_at'] = timezone.now()
        request.data['is_updated'] = True

        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
