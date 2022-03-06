import datetime
from django.db import models
from django.utils import timezone

# Create your models here.


class Name(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Information(models.Model):
    name = models.CharField(max_length=200)
    host = models.ForeignKey(Name, on_delete=models.CASCADE)
    age = models.IntegerField(default=0)
    dept = models.FloatField(default=0)
    balance = models.FloatField(default=0)
    interest = models.FloatField(default=0)
    bool = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.datetime.now())
    birthday = models.DateTimeField(default=timezone.datetime.now())
    interest_bool = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class NameHistory(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class History(models.Model):
    name = models.CharField(max_length=200)
    host = models.ForeignKey(NameHistory, on_delete=models.CASCADE)
    age = models.IntegerField(default=0)
    dept = models.FloatField(default=0)
    balance = models.FloatField(default=0)
    interest = models.FloatField(default=0)
    bool = models.BooleanField(default=False)
    current_balance = models.FloatField(default=0)
    payment = models.FloatField(default=0)
    date = models.DateTimeField()
    birthday = models.DateTimeField(default=datetime.date(2004, 5, 11))
    total = models.FloatField(default=0)

    paid_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Account(models.Model):
    User_Name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.User_Name
