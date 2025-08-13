from django.conf import settings
from django.core.files.storage import get_storage_class
from whitenoise.storage import CompressedManifestStaticFilesStorage
from django.contrib.staticfiles import finders
import os


class MediaFilesStorage(CompressedManifestStaticFilesStorage):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.media_root = str(settings.MEDIA_ROOT)

    def find(self, name, all=False):

        found = super().find(name, all)

        if not found and not settings.DEBUG:
            media_path = os.path.join(self.media_root, name)
            if os.path.exists(media_path):
                return media_path

        return found
