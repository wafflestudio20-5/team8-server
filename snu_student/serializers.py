from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import serializers

from snu_course.models import Course
from .models import User, UserToCourse


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = [
            'email',
            'name',
            'password',
            'token'
        ]
        read_only_fields = ('token',)
        extra_kwargs = {
            'name': {'required': True}
        }

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance


class UserReadonlySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'name'
        ]
        read_only_fields = ('email', 'name')


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = [
            'email',
            'name',
            'password',
            'token',
            'refresh_token'
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    last_login = serializers.CharField(max_length=255, read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = [
            'email',
            'name',
            'password',
            'token',
            'refresh_token'
        ]

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        return {
            'email': user.email,
            'last_login': user.last_login,
            'token': user.token,
            'refresh_token': user.refresh_token
        }


class UserToCourseSerializer(serializers.ModelSerializer):
    from snu_course.serializers import CourseListSerializer
    course = CourseListSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), source='course', write_only=True)

    def validate(self, attrs):
        if UserToCourse.objects.filter(course=attrs['course'], user=attrs['user']).exists():
            raise serializers.ValidationError({'course_id': 'The course is already associated with the user'})
        return attrs

    def to_representation(self, instance):
        return super().to_representation(instance)['course']

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'user': self.context['request'].user, 'sort': self.context['sort']}

    class Meta:
        model = UserToCourse
        fields = ['course', 'course_id']
