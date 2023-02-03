import os
from rest_framework import serializers
from .views import *

class ImagesSerializer(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Images
        fields = ('name', 'image')


class FileListSerializer(serializers.ModelSerializer):

#    file = serializers.FileField(write_only=True)

    def to_internal_value(self, data):
        if 'file' not in data:
            raise serializers.ValidationError('file is required')
        data['name'] = data['file'].name
        return super().to_internal_value(data)


    class Meta:
        model = Files
        fields = [
            'id',
            'name',
            'file',
        ]
        read_only_fields = ['id']


class FileDetailSerializer(serializers.ModelSerializer):
    read_only_fields = ['id']
    allowed_methods = ['GET', 'PUT', 'DELETE']
    file = serializers.FileField()

    def to_internal_value(self, data):
        if 'file' not in data:
            raise serializers.ValidationError('file is required')
        data['name'] = data['file'].name
        return super().to_internal_value(data)

    class Meta:
        model = Files
        fields = [
            'id',
            'name',
            'file',
        ]
