from snu_student.serializers import UserSerializer
from .models import Course, Review
from rest_framework import serializers


class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("name", "curriculum", "professor", "department", "number", "class_number", "maximum", "cart", "current", "time", "credit", "rate")


class ReviewListSerializer(serializers.ModelSerializer):
    CONTENT_LENGTH_LIMIT = 300
    id = serializers.PrimaryKeyRelatedField(read_only=True)

#    def to_internal_value(self, data):
#        internal_value = super().to_internal_value(data)
#        return {**internal_value, 'created_by': self.context['request'].user}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if len(representation['content']) > self.CONTENT_LENGTH_LIMIT:
            representation['content'] = representation['content'][0:self.CONTENT_LENGTH_LIMIT]
        return representation

    class Meta:
        model = Review
        fields = ['id', 'title', 'content', 'created_by', 'created_at', 'updated_at', 'rate', 'course', 'semester']
