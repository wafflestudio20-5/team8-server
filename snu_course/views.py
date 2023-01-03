from django.utils import timezone
from rest_framework import generics
from .serializers import CourseListSerializer, ReviewListSerializer
from .models import Course, Review


class CourseList(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer


class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all().order_by('-created_at')
    serializer_class = ReviewListSerializer
    queryset = Review.objects.all().order_by('-created_at')

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request.data['created_by'] = request.user.id
        request.data['created_at'] = timezone.now()
        request.data['updated_at'] = timezone.now()
        request.data['course'] = kwargs['rid']

        return super().post(request, *args, **kwargs)
