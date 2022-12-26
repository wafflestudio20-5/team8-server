from django.shortcuts import render
from .serializers import UserSerializer
from .models import User
from rest_framework import generics


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer