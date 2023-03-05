from django.shortcuts import render, redirect
from django.views.generic.edit import DeleteView
from .models import Ticket
import requests
client_id = 'client_id=MzIxMjg4OTl8MTY3Nzk0NjYzNi4zMDA4MDYz'
current_search = 'placeholder'

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
    success_url = '/pokemon'

def concerts(request):
    global current_search
    concert = 'no concerts yet'
    search = request.GET.get('name')
    if search:
        response = requests.get(f'https://api.seatgeek.com/2/events?q={search}&{client_id}').json()
        concert = response['events'][0]['title']
        current_search = response
    return render(request, 'main_app/concerts.html', {
        'concert': concert
    })

def add_ticket(request):
    concert = current_search['events'][0]['title']
    new_ticket = Ticket(
        event_name = current_search['events'][0]['title'],
        price = current_search['events'][0]['stats']['average_price'],
        location = current_search['events'][0]['venue']['address'],
        date = current_search['events'][0]['datetime_utc']
    )
    new_ticket.save()
    return render(request, 'main_app/ticket_form.html', {
        'concert': concert
        })
    # return redirect('tickets/detail.html')