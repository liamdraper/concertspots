from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime
# Create your models here.

class Ticket(models.Model):
    event_name =  models.CharField(max_length=200)
    price = models.IntegerField()
    location = models.CharField(max_length=200)
    date = models.DateTimeField(default=datetime.now)

    def get_absolute_url(self):
        return reverse('index')
    
    def get_absolute_url(self):
        return reverse('ticket_detail', kwargs={'pk': self.id})