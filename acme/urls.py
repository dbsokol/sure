from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Acme Insurance API",
        default_version="v1",
        description="Acme Insurance API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),
    path(
        "api/",
        include("quotes.urls"),
    ),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path(
        "__debug__/",
        include("debug_toolbar.urls"),
    ),
    path(
        "",
        lambda x: JsonResponse({"status": 200}),
    ),  # health check
]
