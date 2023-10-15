from django.utils import timezone as django_timezone
from django.db import models

from datetime import datetime, timezone
from uuid import uuid4


class BaseModel(models.Model):
    """Extension of base model class"""

    uuid = models.UUIDField(unique=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(editable=False, default=django_timezone.now)
    updated_at = models.DateTimeField(editable=False, default=django_timezone.now)

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        # set created at field:
        if not self.id:
            self.created_at = datetime.now(timezone.utc)

        # set updated at field:
        self.updated_at = datetime.now(timezone.utc)

        super(BaseModel, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.uuid)
