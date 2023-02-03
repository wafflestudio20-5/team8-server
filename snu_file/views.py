from django.shortcuts import render, get_object_or_404
from django.template import Template, Context
from rest_framework import generics
from rest_framework.response import Response

from .permissions import *
from .models import *
from .serializers import *
from django.utils import timezone
from django.core.files import File
from django.http import HttpResponse
from rest_framework.decorators import api_view
from team8_server.settings import BASE_DIR, MEDIA_ROOT


class FileListView(generics.ListCreateAPIView):
    permission_classes = []
    queryset = Files.objects.all()
    serializer_class = FileListSerializer

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class FileDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FileDetailSerializer
    permission_classes = []

    def get_object(self):
        obj = get_object_or_404(Files, name=self.kwargs['name'])
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        path_to_file = serializer.data['file']#[serializer.data['file'].find('/files') + 1:]

        f = open(path_to_file, 'rb')
        file = File(f)
        response = HttpResponse(file.read())
        response['Content-Disposition'] = 'attachment; filename="%s"' % serializer.data['name']
        return response
