from django.db import models
from datetime import datetime, timedelta, timezone


def file_directory_path(instance, filename):
    extension = filename.split('.')[-1]
    dtnow = datetime.now(timezone.utc)
    dtstr = dtnow.strftime('%Y/%m/%d')
    return 'files/{0}/{1}/{2}'.format(extension, dtstr, filename)


class Files(models.Model):
    file = models.FileField(upload_to=file_directory_path)
    name = models.CharField(max_length=100, unique=True)


class Images(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(default='media/default_image.jpeg')
