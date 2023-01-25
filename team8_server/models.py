from django.db import models

from team8_server.constants import Periods


class ServerState(models.Model):
    period = models.CharField(max_length=1, choices=Periods.choices())

    @classmethod
    def object(cls):
        return cls._default_manager.all().first()

    def save(self, *args, **kwargs):
        self.pk = self.id = 1
        return super().save(*args, **kwargs)

