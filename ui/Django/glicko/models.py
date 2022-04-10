from django.db import models
from uuid import uuid4


class User(models.Model):
    first_name = models.CharField(max_length=50, help_text="First name")
    last_name = models.CharField(max_length=50, help_text="Last name")
    email = models.EmailField(max_length=254, null=True, help_text="username@email.com")
    created_date = models.DateTimeField(auto_now=True)
    id = models.UUIDField(primary_key=True, default=uuid4)


class Trip(models.Model):
    publisher = models.CharField(max_length=200)
    trip_status = models.CharField(max_length=50, default="Progressing")
    scooter_id = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now=True)
    id = models.UUIDField(primary_key=True, default=uuid4)


class Data(models.Model):
    accel_x = models.FloatField(max_length=50, default=0)
    accel_y = models.FloatField(max_length=50, default=0)
    accel_z = models.FloatField(max_length=50, default=0)
    distance = models.FloatField(max_length=50, default=0)
    time = models.DateTimeField(auto_now=True)
    user_id = models.CharField(max_length=200)
    trip_id = models.CharField(max_length=200)

    class Meta:
        ordering = ["user_id"]


# class UserData(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
#     data = models.ForeignKey(Data, on_delete=models.CASCADE, related_name="data")

#     class Meta:
#         unique_together = ["user_id", "id"]
#         ordering = ["user_id"]


def __str__(self):
    return self.title
