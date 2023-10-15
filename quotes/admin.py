from django.contrib import admin
from django.contrib.auth.models import (
    Group,
    User,
)

from quotes.models import Buyer, Coverage, Rate, Quote, State


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "first_name",
        "last_name",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "first_name",
        "last_name",
        "uuid",
    ]


@admin.register(Coverage)
class CoverageAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "name",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "name",
        "uuid",
    ]


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    autocomplete_fields = [
        "buyer",
        "coverages",
        "state",
    ]
    list_display = [
        "uuid",
        "buyer",
        "coverage_type",
        "state",
        "include_pet_premium",
        "created_at",
        "updated_at",
    ]
    list_filter = [
        "state",
        "coverage_type",
    ]
    search_fields = [
        "buyer__first_name",
        "buyer__last_name",
        "state__name",
        "uuid",
    ]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related(
                "buyer",
                "state",
            )
            .prefetch_related(
                "coverages",
            )
        )


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    autocomplete_fields = [
        "coverage",
        "state",
    ]
    list_display = [
        "uuid",
        "coverage",
        "state",
        "rate_increase_percent",
        "created_at",
        "updated_at",
    ]
    list_filter = [
        "coverage",
        "state",
    ]
    search_fields = [
        "coverage__name",
        "state__name",
        "uuid",
    ]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related(
                "coverage",
                "state",
            )
        )


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "code",
        "name",
        "tax_rate",
    ]
    search_fields = [
        "code",
        "name",
        "uuid",
    ]


admin.site.unregister(Group)
admin.site.unregister(User)
