from rest_framework.response import Response
from rest_framework.decorators import api_view

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django.shortcuts import render
from django.views.generic import View

from .serializers import DataSerializers, UserSerializers, TripUserSerializers
from .models import Data, User, Trip


class HomeView(View):
    def get(self, request, *args, **kwargs):
        users = User.objects.count()
        trips = Trip.objects.count()
        return render(request, "index.html")


@api_view(["GET"])
def glickoOverview(request):
    api_urls = {
        "User": {
            "List": "/user-list/",
            "Detail View": "/user-detail/<str:pk>/",
            "Create": "/user-create/",
            "Update": "/user-update/<str:pk>/",
            "Delete": "/user-delete/<str:pk>/",
        },
        "Data": {
            "List": "/data-list/",
            "Create": "/data-create/",
            "Delete": "/data-delete/<str:pk>/",
        },
        "Trip": {
            "List": "/trip-list/",
            "Create": "/trip-create/",
            "Delete": "/trip-delete/<str:pk>/",
        },
    }
    return Response(api_urls)


@api_view(["GET"])
def userList(request):
    tasks = User.objects.all()
    serializer = UserSerializers(tasks, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def userDetail(request, pk):
    tasks = User.objects.get(id=pk)
    serializer = UserSerializers(tasks, many=False)
    return Response(serializer.data)


@swagger_auto_schema(
    method="post",
    manual_parameters=[
        openapi.Parameter(
            "first_name",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="first name",
        ),
        openapi.Parameter(
            "last_name",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="last name",
        ),
        openapi.Parameter(
            "email",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="email",
        ),
    ],
)
@api_view(["POST"])
def userCreate(request):
    serializer = UserSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
def userUpdate(request, pk):
    task = User.objects.get(id=pk)
    serializer = UserSerializers(instance=task, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(["DELETE"])
def userDelete(request, pk):
    task = User.objects.get(id=pk)
    task.delete()
    return Response("Item successfully deleted")


@api_view(["GET"])
def dataList(request):
    tasks = Data.objects.all()
    serializer = DataSerializers(tasks, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method="get",
    manual_parameters=[
        openapi.Parameter(
            "user_id",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="user id",
        ),
        openapi.Parameter(
            "trip_id",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="trip id",
        ),
    ],
)
@api_view(["GET"])
def dataFetch(request, pk):
    args = pk.split(";")
    tasks = Data.objects.filter(user_id=args[0], trip_id=args[1])
    serializer = DataSerializers(tasks, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def dataCreate(request):
    serializer = DataSerializers(data=request.data)
    if (
        serializer.is_valid()
        and User.objects.filter(id=request.data["user_id"]).count() > 0
        and Trip.objects.filter(id=request.data["trip_id"]).count() > 0
    ):
        serializer.save()
        return Response(serializer.data)
    else:
        return Response("Id not found, please enter correct user Id")


@api_view(["DELETE"])
def dataDelete(request, pk):
    task = Data.objects.get(id=pk)
    task.delete()
    return Response("Item successfully deleted")


@api_view(["GET"])
def tripList(request):
    tasks = Trip.objects.all()
    serializer = TripUserSerializers(tasks, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def tripCreate(request):
    serializer = TripUserSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
def tripUpdate(request, pk):
    task = Trip.objects.get(id=pk)
    serializer = TripUserSerializers(instance=task, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(["DELETE"])
def tripDelete(request, pk):
    task = Trip.objects.get(id=pk)
    task.delete()
    return Response("Item successfully deleted")
