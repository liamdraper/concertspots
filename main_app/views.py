from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Ticket
import requests


# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def tickets_index(request):
    tickets = Ticket.objects.all()
    return render(request, 'tickets/index.html', {
        'tickets': tickets
    })

class TicketCreate(CreateView):
    model = Ticket
    fields = ['seat', 'number', 'price']

def concerts(request):
    api = requests.get('https://api.seatgeek.com/2/events/801255?client_id=MzIxMjg4OTl8MTY3Nzk0NjYzNi4zMDA4MDYz').json()
    concert = api
    return render(request, 'main_app/concerts.html', {
        'concert': concert
    })