
from __future__ import absolute_import
from storages.backends.s3boto import S3BotoStorage


class PrefixedStorage(S3BotoStorage):
    """
    This class defines a new storage that adds additional headers to the
    files uploaded to Amazon S3.
    """

    def __init__(self, *args, **kwargs):
        kwargs['location'] = 'media'
        kwargs['acl'] = 'private'
        return super(PrefixedStorage, self).__init__(*args, **kwargs)
