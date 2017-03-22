import mimetypes
import os

from django.conf import settings
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from minio import Minio
from minio.error import ResponseError, InvalidXMLError, InvalidEndpointError
from urllib3.exceptions import MaxRetryError


def setting(name, default=None):
    """
    Helper function to get a Django setting by name or (optionally) return
    a default (or else ``None``).
    """
    return getattr(settings, name, default)


@deconstructible
class MinioStorage(Storage):
    # TODO: Log errors caused by exceptions
    server = setting('MINIO_SERVER')
    access_key = setting('MINIO_ACCESSKEY')
    secret_key = setting('MINIO_SECRET')
    bucket = setting('MINIO_BUCKET')
    secure = setting('MINIO_SECURE')

    def __init__(self, *args, **kwargs):
        super(MinioStorage, self).__init__(*args, **kwargs)
        self._connection = None

    @property
    def connection(self):
        if not self._connection:
            try:
                self._connection = Minio(
                    self.server, self.access_key, self.secret_key, self.secure)
            except InvalidEndpointError:
                self._connection = None
        return self._connection

    def _bucket_has_object(self, name):
        if self.connection:
            try:
                # TODO: Check for file by hashed name, not original
                self.connection.get_object(self.bucket, name.encode('utf8'))
                return True
            except (ResponseError, MaxRetryError):
                # ResponseError rises when file not found.
                # MaxRetryError rises when service is not available.
                pass
        return False

    def _save(self, name, content):
        if hasattr(content.file, 'content_type'):
            content_type = content.file.content_type
        else:
            content_type = mimetypes.guess_type(name)[0]
        if self.connection:
            if not self.connection.bucket_exists(self.bucket):
                self.connection.make_bucket(self.bucket)
            try:
                self.connection.put_object(
                    self.bucket, name, content, content.file.size, content_type=content_type
                )
            except InvalidXMLError:
                pass
            except MaxRetryError:
                pass
        return name  # TODO: Do not return name if saving was unsuccessful

    def url(self, name):
        if self.connection:
            try:
                if self.connection.bucket_exists(self.bucket):
                    return self.connection.presigned_get_object(self.bucket, name)
                else:
                    return "image_not_found"  # TODO: Find a better way of returning errors
            except MaxRetryError:
                return "image_not_found"
        return "could_not_establish_connection"

    def exists(self, name):
        return self._bucket_has_object(name)

    def size(self, name):
        info = self.connection.stat_object(self.bucket, name)
        return info.size