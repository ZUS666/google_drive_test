from rest_framework import serializers


class DriveSerializer(serializers.Serializer):
    """
    Сериализатор ввода данных для создания файла.
    """
    name = serializers.CharField(write_only=True)
    data = serializers.CharField(write_only=True)
