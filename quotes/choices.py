from django.db import models


class CoverageTypeChoices(models.TextChoices):
    BASIC = "BASIC"
    PREMIUM = "PREMIUM"
