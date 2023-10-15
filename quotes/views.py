from django.core.exceptions import ValidationError
from django.db.models import F, Value
from django.db.models.functions import Concat

from rest_framework import exceptions
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from quotes.filters import QuoteFilter
from quotes.models import (
    Buyer,
    Coverage,
    Quote,
    Rate,
    State,
)
from quotes.serializers import (
    BuyerSerializer,
    CovergeSerializer,
    QuoteSerializer,
    RateSerializer,
    StateSerializer,
)
from utilities.viewsets import BaseViewSet


class CalculatePriceOnQuoteAPI(RetrieveAPIView):
    """
    separate class specifically for running the price calculator
    allows other Quote APIs to be used without forcing price calculation
    useful if this calculation is computationally intensive
    """

    lookup_field = "uuid"
    queryset = (
        Quote.objects.all()
        .order_by("-created_at")
        .annotate(
            buyer_name=Concat(
                F("buyer__first_name"),
                Value(" "),
                F("buyer__last_name"),
            )
        )
    )
    serializer_class = QuoteSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        on retrieve, call the calculate price method
        and add to response
        """

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        try:
            # calculate price:
            data["price"] = instance.calculate_price()

        except ValidationError as exception:
            raise exceptions.ValidationError(
                detail={
                    "price": exception,
                },
            )

        # sort json response alphabetically
        sorted_data = dict(sorted(data.items()))

        return Response(sorted_data)


class BuyerViewSet(BaseViewSet):
    queryset = Buyer.objects.all().order_by("-created_at")
    serializer_class = BuyerSerializer


class CoverageViewSet(BaseViewSet):
    queryset = Coverage.objects.all().order_by("name")
    serializer_class = CovergeSerializer


class QuoteViewSet(BaseViewSet):
    queryset = (
        Quote.objects.all()
        .order_by("-created_at")
        .select_related(
            "buyer",
            "state",
        )
        .prefetch_related(
            "coverages",
        )
        .annotate(
            buyer_name=Concat(
                F("buyer__first_name"),
                Value(" "),
                F("buyer__last_name"),
            )
        )
    )
    serializer_class = QuoteSerializer
    filterset_class = QuoteFilter
    ordering_fields = [
        "created_at",
        "updated_at",
    ]


class RateViewSet(BaseViewSet):
    queryset = (
        Rate.objects.all()
        .order_by("-created_at")
        .select_related(
            "coverage",
            "state",
        )
    )
    serializer_class = RateSerializer


class StateViewSet(BaseViewSet):
    queryset = State.objects.all().order_by("code")
    serializer_class = StateSerializer
