from rest_framework import serializers

from published_events_deploy.apps.multimedia.models import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"
