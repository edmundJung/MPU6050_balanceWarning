from django.urls import path
from . import views

urlpatterns = [
    path("", views.glickoOverview, name="glicko-overview"),
    path("user-list/", views.userList, name="user-list"),
    path("user-detail/<str:pk>/", views.userDetail, name="user-detail"),
    path("user-create/", views.userCreate, name="user-create"),
    path("user-update/<str:pk>/", views.userUpdate, name="user-update"),
    path("user-delete/<str:pk>/", views.userDelete, name="user-delete"),
    path("data-list/", views.dataList, name="data-list"),
    path("data-fetch/<str:pk>/", views.dataFetch, name="data-fetch"),
    path("data-create/", views.dataCreate, name="data-create"),
    path("data-delete/<str:pk>/", views.dataDelete, name="data-delete"),
    path("trip-list/", views.tripList, name="trip-list"),
    path("trip-create/", views.tripCreate, name="trip-create"),
    path("trip-update/<str:pk>/", views.tripUpdate, name="trip-update"),
    path("trip-delete/<str:pk>/", views.tripDelete, name="trip-delete"),
]
