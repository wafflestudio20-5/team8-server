from rest_framework import serializers

from team8_server.models import ServerState


class ServerStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerState
        fields = ['period']
