from rest_framework import generics
from .serializers import CourseListSerializer
from .models import Course


class CourseList(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
