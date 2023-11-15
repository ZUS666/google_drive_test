import io

from django.conf import settings
from google.auth.exceptions import GoogleAuthError
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload
from rest_framework.exceptions import ValidationError


def send_file_to_drive(validated_data):
    """
    Создание и отправка текстового файла Google Drive.
    """
    name = validated_data.get('name')
    data = validated_data.get('data')
    credentials = get_credentials()
    try:
        service = build("drive", "v3", credentials=credentials)
        file_metadata = {"name": name}
        with io.BytesIO() as ghost_file:
            ghost_file.write(data.encode('utf-8'))
            media = MediaIoBaseUpload(ghost_file, mimetype='text/plain')
            file = (
                service.files()
                .create(body=file_metadata, media_body=media, fields='id')
                .execute()
            )
            result = f'file id: {file.get("id")}'
    except (HttpError, GoogleAuthError) as error:
        raise ValidationError(f'An error occurred: {error}')
    return result


def get_credentials():
    """
    Получение учетных данных Google Drive.
    """
    credentials = Credentials(
        'token',
        refresh_token=settings.API_REFRESH_TOKEN,
        token_uri='https://accounts.google.com/o/oauth2/token',
        client_id=settings.API_CLIENT_ID,
        client_secret=settings.API_CLIENT_SECRET
    )
    return credentials
