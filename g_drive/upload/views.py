from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from upload.serializers import DriveSerializer
from upload.services import send_file_to_drive


class DriveAPIView(CreateAPIView):
    """
    Представление для создания текстового файла в Google Drive.
    name: название файла.
    data: создержание файла
    """
    serializer_class = DriveSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = send_file_to_drive(serializer.validated_data)
        return Response({'message': result}, status=status.HTTP_200_OK)
