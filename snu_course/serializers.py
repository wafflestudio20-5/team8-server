from .models import Course
from rest_framework import serializers


class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("name", "curriculum", "professor", "department", "number", "class_number", "maximum", "cart", "current", "time", "credit", "rate")