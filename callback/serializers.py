from rest_framework import serializers


class PostSerializer(serializers.Serializer):
    object = serializers.JSONField()
    event_id = serializers.CharField()
