from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'password']
        extra_kwargs = {
            'username': {'required': True},
            'name': {'required': True}
        }