from django.contrib import admin
from .models import User, Data, Trip
from django.core import serializers
from django.http import HttpResponse


@admin.action(description="Export selected data")
def export_as_csv(modeladmin, request, queryset):
    response = HttpResponse(
        content_type="application/json",
        headers={"Content-Disposition": "attachment; filename=data.json"},
    )
    serializers.serialize("json", queryset, stream=response)
    return response


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "email", "created_date", "id")
    fields = ["last_name", "first_name", "email"]
    list_filter = ["id", "created_date"]
    actions = [export_as_csv]


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ("scooter_id", "created_date", "id", "trip_status","publisher")
    fields = ["scooter_id", "id", "publisher", "trip_status"]
    list_filter = ["scooter_id", "created_date", "trip_status", "publisher"]
    actions = [export_as_csv]


@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    list_display = (
        "time",
        "accel_x",
        "accel_y",
        "accel_z",
        "distance",
        "user_id",
        "trip_id",
    )
    fields = [
        ("accel_x", "accel_y", "accel_z"),
        "distance",
        "user_id",
        "trip_id",
    ]
    list_filter = ("user_id", "trip_id", "time")
    actions = [export_as_csv]
