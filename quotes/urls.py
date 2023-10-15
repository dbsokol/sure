from django.urls import include, path

from rest_framework import routers

from quotes import views


router = routers.DefaultRouter()
router.register("buyers", views.BuyerViewSet)
router.register("coverages", views.CoverageViewSet)
router.register("quotes", views.QuoteViewSet)
router.register("rates", views.RateViewSet)
router.register("states", views.StateViewSet)


urlpatterns = [
    path(
        "",
        include(router.urls),
    ),
    path(
        "quotes/<uuid:uuid>/calculate-price/",
        views.CalculatePriceOnQuoteAPI.as_view(),
        name="calculate-price",
    ),
]
