from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import serializers

from snu_course.models import Course
from django.shortcuts import get_object_or_404

from .models import User, UserToCourse
from team8_server.constants import CourseSorts


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


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'email',
            'name',
            'student_id',
            'college',
            'department',
            'program',
            'academic_year',
            'year_of_entrance'
        ]
        read_only_fields = ('email',
            'name',
            'student_id',
            'college',
            'department',
            'program',
            'academic_year',
            'year_of_entrance'
        )

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
            'student_id',
            'college',
            'department',
            'program',
            'academic_year',
            'year_of_entrance',
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


class UserToCourseValidator:
    @staticmethod
    def is_same_course(attrs):
        user, course, sort = attrs['user'], attrs['course'], attrs['sort']
        if UserToCourse.objects.filter(user=user, course=course, sort=sort).exists():
            raise serializers.ValidationError(
                {'course': '이미 등록한 강좌입니다.'})

    @staticmethod
    def is_same_course_num(attrs):
        user, course, sort = attrs['user'], attrs['course'], attrs['sort']
        if UserToCourse.objects.filter(user=user, course__number=course.number, sort=sort).exists():
            raise serializers.ValidationError(
                {'course': '같은 교과목의 분반이 다른 강좌를 이미 등록하였습니다.'})

    @staticmethod
    def is_exceed_cart(attrs):
        user, course = attrs['user'], attrs['course']
        if user.cart_credits + course.credit > 21:
            raise serializers.ValidationError(
                {'course': '장바구니 신청 가능 학점 수(21)를 초과하였습니다.'})
        
    @staticmethod
    def is_valid_timetable(attrs):
        sort = attrs['sort']
        if sort not in CourseSorts.TIME_TABLE:
            raise serializers.ValidationError(
                {'course': '유효하지 않은 시간표 번호입니다'})

    @staticmethod
    def is_exceed_timetable(attrs):
        user, course, sort = attrs['user'], attrs['course'], attrs['sort']
        if user.timetable_credits(sort) + course.credit > 21:
            raise serializers.ValidationError(
                {'course': '시간표 신청 가능 학점 수(21)를 초과하였습니다.'})

    @staticmethod
    def is_exceed_registration(attrs):
        user, course = attrs['user'], attrs['course']
        if user.registration_credits + course.credit > 21:
            raise serializers.ValidationError(
                {'course': '수강신청 가능 학점 수(21)를 초과하였습니다.'})

    @staticmethod
    def can_insert(attrs):
        user, course, sort = attrs['user'], attrs['course'], attrs['sort']
        if not course.can_insert_into(UserToCourse.objects.filter(user=user, sort=sort).values_list('course')):
            raise serializers.ValidationError(
                {'course': '이미 등록한 강좌 중 수업시간이 겹치는 강좌가 있습니다.'})

    @staticmethod
    def is_exceed_max_registrations(attrs):
        user, course = attrs['user'], attrs['course']
        if course.current >= course.maximum:
            raise serializers.ValidationError(
                {'course': '수강 정원을 초과하였습니다.'})
    

class UserToCourseSerializer(serializers.ModelSerializer):
    from snu_course.serializers import CourseListSerializer
    course = CourseListSerializer(read_only=True)
    id = serializers.IntegerField(write_only=True)

    validators = []

    def validate(self, attrs):
        for validator in self.validators:
            validator(attrs)
        return attrs

    def to_representation(self, instance):
        return super().to_representation(instance)['course']

    def to_internal_value(self, data):
        course = get_object_or_404(Course, id=data['id'])
        return {'user': self.context['request'].user, 'course': course, 'sort': self.context['sort']}

    class Meta:
        model = UserToCourse
        fields = ['course', 'id']


class InterestSerializer(UserToCourseSerializer):
    validators = [UserToCourseValidator.is_same_course]


class CartSerializer(UserToCourseSerializer):
    validators = [
        UserToCourseValidator.is_same_course,
        UserToCourseValidator.is_same_course_num,
        UserToCourseValidator.is_exceed_cart,
        UserToCourseValidator.can_insert
    ]


class RegisteredSerializer(UserToCourseSerializer):
    validators = [
        UserToCourseValidator.is_same_course,
        UserToCourseValidator.is_same_course_num,
        UserToCourseValidator.is_exceed_registration,
        UserToCourseValidator.is_exceed_max_registrations,
        UserToCourseValidator.can_insert
    ]


class TimeTableSerializer(UserToCourseSerializer):
    validators = [
        UserToCourseValidator.is_same_course,
        UserToCourseValidator.is_same_course_num,
        UserToCourseValidator.is_exceed_timetable,
        UserToCourseValidator.can_insert
    ]


