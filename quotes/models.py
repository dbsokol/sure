from django.db import models

from quotes.choices import CoverageTypeChoices
from quotes.mixins import QuoteMixin
from utilities.models import BaseModel


class Buyer(BaseModel):
    """
    simple buyer model
    """

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Coverage(BaseModel):
    """
    coverage model, represents a type of coverage (i.e. flood)
    """

    name = models.CharField(
        max_length=255,
        unique=True,
    )

    class Meta:
        ordering = [
            "name",
        ]

    def __str__(self):
        return self.name


class Quote(BaseModel, QuoteMixin):
    """
    quote model, used to calculate quotes for customers
    """

    buyer = models.ForeignKey(
        "quotes.Buyer",
        on_delete=models.CASCADE,
        related_name="quotes",
    )
    coverages = models.ManyToManyField(
        "quotes.Coverage",
        related_name="quotes",
    )
    coverage_type = models.CharField(
        max_length=7,
        choices=CoverageTypeChoices.choices,
    )
    include_pet_premium = models.BooleanField(
        default=False,
    )
    state = models.ForeignKey(
        "quotes.State",
        on_delete=models.CASCADE,
        related_name="quotes",
    )


class Rate(BaseModel):
    """
    rate model, for tracking coverage rates per state
    """

    state = models.ForeignKey(
        "quotes.State",
        on_delete=models.CASCADE,
        related_name="rates",
    )
    coverage = models.ForeignKey(
        "quotes.Coverage",
        on_delete=models.CASCADE,
        related_name="rates",
    )
    rate_increase_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "state",
                    "coverage",
                ],
                name="single-coverage-per-state",
            )
        ]

    def __str__(self):
        return f"{self.state} - {self.coverage}"


class State(BaseModel):
    """
    state model, allows adding of states without code
    """

    code = models.CharField(
        max_length=2,
        unique=True,
    )
    name = models.CharField(
        max_length=13,
        unique=True,
    )
    tax_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
    )

    class Meta:
        ordering = [
            "code",
        ]

    def __str__(self):
        return self.code
