from django.shortcuts import render, redirect
from django.views.generic.edit import DeleteView
from .models import Ticket, Concert
import requests
client_id = 'client_id=MzIxMjg4OTl8MTY3Nzk0NjYzNi4zMDA4MDYz'

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

def ticket_detail(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    return render(request, 'tickets/detail.html', {
        'ticket': ticket
    })

class TicketDelete(DeleteView):
    model = Ticket
    success_url = '/tickets'

def concerts_index(request):
    concerts = Concert.objects.all()
    return render(request, 'concerts/concerts_index.html', {
        'concerts': concerts
    })

# The user search input is not getting saved because the function gets reset each time, and the variable "search" isn't saved
def concerts_search(request):
    concerts = []
    search = request.GET.get('name')
    response = requests.get(f'https://api.seatgeek.com/2/events?q={search}&{client_id}').json()
    if search:
        for e in response['events']:
            # event_name = e['title']
            # concerts.append(event_name)
            concerts.append(e)
    return render(request, 'concerts/search.html', {
        'concerts': concerts
    })

def concert_detail(request, concert_id):
    # If not in database, create(), then redner detail page
    # If in database, get concert item from api_id and render detail page
    concert = Concert.objects.filter(api_id=concert_id).first()
    if not concert:
        concert = Concert.objects.create(
            event_name = request.POST.get('event_name'),
            price = request.POST.get('price'),
            location = request.POST.get('location'),
            date = request.POST.get('date'),
            api_id = request.POST.get('api_id')
        )
    if request.POST:
        new_ticket = Ticket(
            event_name = concert.event_name,
            price = concert.price,
            location = concert.location,
            date = concert.date
        )
        new_ticket.concert_id = concert_id
        new_ticket.save()
    # If form is valid, create and associate ticket
    return render(request, 'concerts/detail.html', {
        'concert': concert
    })
