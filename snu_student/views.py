from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.naver.views import NaverOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.serializers import SocialLoginSerializer
from rest_auth.registration.views import SocialLoginView
from rest_framework import generics, status, mixins
from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .backends import JWTAuthentication
from .serializers import UserSerializer, RegistrationSerializer, LoginSerializer
from .models import User
from rest_framework import generics, status
from .models import User, UserToCourse
from .serializers import UserSerializer, RegistrationSerializer, LoginSerializer, UserToCourseSerializer
from rest_framework import serializers
from django.shortcuts import get_object_or_404

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
        print(token)
        serializer = self.get_serializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

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
                                 course__number=self.request.data['number'],
                                 course__class_number=self.request.data['class_number'],
                                 sort=self.sort)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class InterestCourseAPIView(BaseCourseAPIView):
    sort = 'I'


class CartCourseAPIView(BaseCourseAPIView):
    sort = 'C'


class RegisteredCourseAPIView(BaseCourseAPIView):
    sort = 'R'
