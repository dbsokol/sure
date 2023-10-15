import django_filters

from quotes.models import Quote


class QuoteFilter(django_filters.FilterSet):
    class Meta:
        model = Quote
        fields = {
            "buyer__first_name": [
                "icontains",
            ],
            "buyer__last_name": [
                "icontains",
            ],
            "uuid": [
                "exact",
                "in",
            ],
        }
