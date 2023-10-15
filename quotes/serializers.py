from rest_framework import serializers

from quotes.models import (
    Buyer,
    Coverage,
    Quote,
    Rate,
    State,
)


class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = [
            "first_name",
            "last_name",
            "uuid",
        ]


class CovergeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coverage
        fields = [
            "created_at",
            "name",
            "updated_at",
            "uuid",
        ]


class QuoteSerializer(serializers.ModelSerializer):
    buyer = serializers.SlugRelatedField(
        "uuid",
        queryset=Buyer.objects.all(),
        write_only=True,
    )
    buyer_name = serializers.CharField(
        read_only=True,
    )
    coverages = serializers.SlugRelatedField(
        "name",
        many=True,
        queryset=Coverage.objects.all(),
    )
    state = serializers.SlugRelatedField(
        "code",
        queryset=State.objects.all(),
    )

    class Meta:
        model = Quote
        fields = [
            "buyer",
            "buyer_name",
            "coverages",
            "coverage_type",
            "created_at",
            "include_pet_premium",
            "state",
            "updated_at",
            "uuid",
        ]


class RateSerializer(serializers.ModelSerializer):
    coverage = serializers.SlugRelatedField(
        "name",
        queryset=Coverage.objects.all(),
    )
    state = serializers.SlugRelatedField(
        "code",
        queryset=State.objects.all(),
    )

    class Meta:
        model = Rate
        fields = [
            "coverage",
            "created_at",
            "rate_increase_percent",
            "state",
            "updated_at",
            "uuid",
        ]


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = [
            "code",
            "name",
            "tax_rate",
            "uuid",
        ]
