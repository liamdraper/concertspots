from django.shortcuts import render, redirect
from django.views.generic.edit import DeleteView
from .models import Ticket
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

# The user search input is not getting saved because the function gets reset each time, and the variable "search" isn't saved
def concerts(request):
    global current_search
    concerts = None
    search = request.GET.get('name')
    choice = request.GET.get('choice')
    response = requests.get(f'https://api.seatgeek.com/2/events?q={search}&{client_id}').json()
    if search:
        concerts = []
        for e in response['events']:
            # event_name = e['title']
            # concerts.append(event_name)
            concerts.append(e)
    if choice:
        # current_search = response['events'][int(choice)]
        current_search = response['events'][int(choice)]
        return redirect('ticket_create')
    return render(request, 'main_app/concerts.html', {
        'concerts': concerts
        })



def add_ticket(request):
    concert = current_search['title']
    # Still need to figure out how to access price and date info from API
    # new_ticket = Ticket(
    #     event_name = current_search['title'],
    #     price = 100,
    #     location = current_search['venue']['address'],
    #     date = current_search['datetime_utc']
    # )
    # new_ticket.save()
    return render(request, 'main_app/ticket_form.html', {
        'concert': concert
        })
    # return redirect('tickets/detail.html')