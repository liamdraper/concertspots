from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime
# Create your models here.

class Concert(models.Model):
    event_name = models.CharField(max_length=200)
    price = models.IntegerField()
    location = models.CharField(max_length=200)
    date = models.DateTimeField(default=datetime.now)
    api_id = models.IntegerField()

    def __str__(self):
        return f'{self.event_name} ({self.id})'

class Ticket(models.Model):
    event_name =  models.CharField(max_length=200)
    price = models.IntegerField()
    location = models.CharField(max_length=200)
    date = models.DateTimeField(default=datetime.now)

    concert = models.ForeignKey(Concert, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.event_name} ({self.id})'