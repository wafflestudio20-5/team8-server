from django.db import models
from datetime import datetime, timedelta, timezone


def file_directory_path(instance, filename):
    extension = filename.split('.')[-1]
    dtnow = datetime.now(timezone.utc)
    dtstr = dtnow.strftime('%Y/%m/%d')
    return 'files/{0}/{1}/{2}'.format(extension, dtstr, filename)


def mnist_directory_path(instance, filename):
    return 'files/mnist/{0}'.format(filename)


class Files(models.Model):
    file = models.FileField(upload_to=file_directory_path)
    name = models.CharField(max_length=100, unique=True)


class Mnist(models.Model):
    name = models.CharField(max_length=10)
    image = models.ImageField(upload_to=mnist_directory_path)
    label = models.IntegerField(default=0)