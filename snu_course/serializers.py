from .models import Course, Review, Comment
from rest_framework import serializers


class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (
            "name", "curriculum", "professor", "department", "number", "class_number", "maximum", "cart", "current", "time",
            "credit", "rate")


class ReviewListSerializer(serializers.ModelSerializer):
    from snu_student.serializers import UserSerializer
    CONTENT_LENGTH_LIMIT = 300
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = UserSerializer(read_only=True)

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
    from snu_student.serializers import UserSerializer
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = UserSerializer(read_only=True)
    course = CourseListSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'title', 'content', 'created_by', 'created_at',
                  'is_updated', 'updated_at', 'rate', 'course', 'semester']


class CommentListSerializer(serializers.ModelSerializer):
    from snu_student.serializers import UserSerializer
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = UserSerializer(read_only=True)
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
    from snu_student.serializers import UserSerializer
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'created_by', 'content', 'review', 'created_at', 'is_updated', 'updated_at']
