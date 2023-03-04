from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Ticket(models.Model):
    price = models.IntegerField()
    seat = models.CharField(max_length=5)
    number = models.IntegerField()

    def get_absolute_url(self):
        return reverse('index')