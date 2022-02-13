from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class ExtraUser(models.Model):
    photo = models.ImageField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Travel(models.Model):
    title = models.CharField(max_length=50)
    date_start = models.DateField()
    date_end = models.DateField()
    active = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class BackpackItem(models.Model):
    name = models.CharField(max_length=50)
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE)


class Route(models.Model):
    address = models.CharField(max_length=100)
    date = models.DateField(max_length=50)
    hour = models.TimeField(max_length=50)
    price = models.CharField(max_length=50, blank=True)
    notes = models.CharField(max_length=50, blank=True)
    type_card = models.CharField(max_length=50)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE)


class Accommodation(models.Model):
    address = models.CharField(max_length=100)
    check_in_date = models.DateField(max_length=50)
    check_in_hour = models.TimeField(max_length=50)
    check_out_date = models.DateField(max_length=50)
    check_out_hour = models.TimeField(max_length=50)
    price = models.CharField(max_length=50)
    type_card = models.CharField(max_length=50)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE)


class Ticket(models.Model):
    address = models.CharField(max_length=100)
    check_in_date = models.DateField(max_length=50)
    check_in_hour = models.TimeField(max_length=50)
    seat = models.CharField(max_length=50, blank=True)
    boarding_gate = models.CharField(max_length=50, blank=True)
    price = models.CharField(max_length=50, blank=True)
    type_card = models.CharField(max_length=50)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE)
