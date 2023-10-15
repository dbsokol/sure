import factory
from factory.django import DjangoModelFactory

from quotes.models import (
    Buyer,
    Coverage,
    Quote,
    Rate,
    State,
)


class BuyerFactory(DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    class Meta:
        model = Buyer


class CoverageFactory(DjangoModelFactory):
    class Meta:
        model = Coverage


class QuoteFactory(DjangoModelFactory):
    class Meta:
        model = Quote


class RateFactory(DjangoModelFactory):
    class Meta:
        model = Rate


class StateFactory(DjangoModelFactory):
    class Meta:
        model = State
