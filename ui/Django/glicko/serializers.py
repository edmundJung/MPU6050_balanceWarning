from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Data, User, Trip


class DataSerializers(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = [
            "accel_x",
            "accel_y",
            "accel_z",
            "distance",
            "time",
            "user_id",
            "trip_id",
        ]

        read_only_fields = [
            "time",
        ]

    # def create(self, validated_data):
    #     id = validated_data["user_id"]
    #     user = User.objects.get(id)
    #     Data.objects.create(publisher=user, **validated_data)


class UserSerializers(serializers.ModelSerializer):
    # data = DataSerializers(many=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "id",
            "created_date",
        ]

        read_only_fields = [
            "id",
            "created_date",
        ]

        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(), fields=["first_name", "last_name", "email"]
            )
        ]


class TripUserSerializers(serializers.ModelSerializer):
    # data = DataSerializers(many=True)

    class Meta:
        model = Trip
        fields = [
            "scooter_id",
            "trip_status",
            "publisher",
            "id",
            "created_date",
        ]

        read_only_fields = [
            "created_date",
        ]

    # def create(self, validated_data):
    #     data = validated_data.pop("data")
    #     user = User.objects.create(**validated_data)
    #     for _ in data:
    #         Data.objects.create(publisher=user, **_)
    #     return user


# class UserDataSerializers(serializers.ModelSerializer):
#     data = DataSerializers(many=True)
#     user = UserSerializers(many=True)

#     class Meta:
#         model = UserData
#         fields = [

#         ]


#     def create(self, validated_data):
#         data = validated_data.pop("data")
