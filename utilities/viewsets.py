from rest_framework import viewsets

from django_filters import rest_framework as filters

from utilities.ordering import CustomOrderingFilter


class BaseViewSet(viewsets.ModelViewSet):
    """
    base viewset, includes some customization
    """

    lookup_field = "uuid"
    filter_backends = (
        filters.DjangoFilterBackend,
        CustomOrderingFilter,
    )
