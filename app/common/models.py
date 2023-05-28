from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    date_of_creation = models.DateTimeField(default=timezone.localtime)
    date_of_update = models.DateTimeField(null=True)

    # soft delete, чтобы не терять данные
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.date_of_update = timezone.localtime()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
