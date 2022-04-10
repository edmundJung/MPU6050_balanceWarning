from django.contrib import admin
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from glicko import views

schema_view = get_schema_view(
    openapi.Info(
        title="Glicko API", default_version="v1", description="Glicko api description",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", views.HomeView.as_view()),
    path("admin/", admin.site.urls),
    path("api/", include("glicko.urls")),
    path("doc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc-ui"),
]
