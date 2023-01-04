from django.db.models import Avg

from snu_student.serializers import UserSerializer, UserReadonlySerializer
from .models import Course, Review, Comment, TimeInfo
from rest_framework import serializers


class CourseListSerializer(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField()

    def get_rate(self, obj):
        return obj.review_set.all().aggregate(Avg('rate'))['rate__avg']

    class Meta:
        model = Course
        fields = (
            "name", "curriculum", "professor", "department", "number", "class_number", "maximum",
            "cart", "current", "time", "credit", "rate")


class CourseDetailSerializer(serializers.ModelSerializer):
    parsed_time = serializers.SerializerMethodField()
    rate = serializers.SerializerMethodField()

    def get_rate(self, obj):
        return obj.review_set.all().aggregate(Avg('rate'))['rate__avg']

    def get_parsed_time(self, obj):
        return obj.timeinfo_set.values("day", "start_time", "end_time")

    class Meta:
        model = Course
        fields = (
            "name", "curriculum", "professor", "department", "number", "class_number", "maximum",
            "cart", "current", "time", "credit", "rate", "parsed_time")


class ReviewListSerializer(serializers.ModelSerializer):
    CONTENT_LENGTH_LIMIT = 300
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = UserReadonlySerializer(read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if len(representation['content']) > self.CONTENT_LENGTH_LIMIT:
            representation['content'] = representation['content'][0:self.CONTENT_LENGTH_LIMIT]
        return representation

    class Meta:
        model = Review
        fields = ['id', 'title', 'content', 'created_by', 'created_at',
                  'is_updated', 'updated_at', 'rate', 'course', 'semester']


class ReviewDetailSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = UserReadonlySerializer(read_only=True)
    course = CourseListSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'title', 'content', 'created_by', 'created_at',
                  'is_updated', 'updated_at', 'rate', 'course', 'semester']


class CommentListSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = UserReadonlySerializer(read_only=True)
    CONTENT_LENGTH_LIMIT = 300

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if len(representation['content'])>self.CONTENT_LENGTH_LIMIT:
            representation['content'] = representation['content'][0:self.CONTENT_LENGTH_LIMIT]
        return representation

    class Meta:
        model = Comment
        fields = ['id', 'created_by', 'content', 'review', 'created_at', 'is_updated']


class CommentDetailSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = UserReadonlySerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'created_by', 'content', 'review', 'created_at', 'is_updated', 'updated_at']

