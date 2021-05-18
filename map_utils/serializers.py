from rest_framework import serializers
from .models import MapData


class MapDataSerializer(serializers.ModelSerializer):
    """
    Serializer to map the model instance into JSON
    """

    class Meta:
        """
        Meta class to map serializer's fields with
        the model fields.
        """
        model = MapData
        fields = ('id', 'name', 'date_created', 'date_modified')
        read_only_fields = ('date_created', 'date_modified')
