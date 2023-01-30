from rest_framework import generics, status, mixins
from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from team8_server.constants import Periods, CourseSorts
from team8_server.permissions import IsPeriod
from .backends import JWTAuthentication
from .models import User
from rest_framework import generics, status
from .models import User, UserToCourse
from .serializers import *
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from snu_course.pagination import UserToCoursePagination

# Create your views here.


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RefreshApiView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    Auth_class = JWTAuthentication

    def post(self, request, *args, **kwargs):
        user, token = self.Auth_class.refresh_credentials(request.data['refresh_token'])
        serializer = self.get_serializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        serializer_data = request.data
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class BaseCourseAPIView(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserToCourseSerializer
    pagination_class = UserToCoursePagination
    sort = None

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['sort'] = self.sort
        return context

    def get_queryset(self):
        user = self.request.user.id
        return UserToCourse.objects.filter(user=user, sort=self.sort)

    def get_object(self):
        user = self.request.user.id
        return get_object_or_404(UserToCourse,
                                 user=user,
                                 course__id=self.request.data['id'],
                                 sort=self.sort)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class InterestCourseAPIView(BaseCourseAPIView):
    sort = CourseSorts.INTEREST
    serializer_class = InterestSerializer


class CartCourseAPIView(BaseCourseAPIView):
    sort = CourseSorts.CART
    permission_classes = BaseCourseAPIView.permission_classes + [IsPeriod(Periods.CART)]
    serializer_class = CartSerializer


class RegisteredCourseAPIView(BaseCourseAPIView):
    sort = CourseSorts.REGISTERED
    permission_classes = BaseCourseAPIView.permission_classes + [IsPeriod(Periods.REGISTRATION)]
    serializer_class = RegisteredSerializer


class PendingListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserToCourseSerializer
    pagination_class = UserToCoursePagination

    def get_queryset(self):
        user = self.request.user.id
        return UserToCourse.objects.filter(user=user, course__pending=True, sort=CourseSorts.CART)


class TimeTableCourseAPIView(BaseCourseAPIView):
    sort_list = CourseSorts.TIME_TABLE
    permission_classes = BaseCourseAPIView.permission_classes
    serializer_class = TimeTableSerializer

    def get_sort(self):
        self.sort = self.kwargs['num']
        if self.sort not in self.sort_list:
            raise serializers.ValidationError('유효하지 않은 시간표 번호입니다.')

    def get(self, request, *args, **kwargs):
        self.get_sort()
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.get_sort()
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.get_sort()
        return self.destroy(request, *args, **kwargs)


class TimeTableInsertAPIView(BaseCourseAPIView):
    serializer_class = CartSerializer
    http_method_names = ['post']
    sort = CourseSorts.CART
    sort_list = CourseSorts.TIME_TABLE

    def get_queryset(self):
        user = self.request.user.id
        return UserToCourse.objects.filter(user=user, sort=self.kwargs['num'])

    def create(self, request_data, *args, **kwargs):
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

    def post(self, request, *args, **kwargs):
        if self.kwargs['num'] not in self.sort_list:
            raise serializers.ValidationError('유효하지 않은 시간표 번호입니다.')

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        user = self.request.user.id
        UserToCourse.objects.filter(user=user, sort=CourseSorts.CART).delete()

        for data in serializer.data:
            self.create(data, *args, **kwargs)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
