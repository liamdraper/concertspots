from django.shortcuts import render, redirect
from django.views.generic.edit import DeleteView
from django.contrib.auth import logout
from .models import Ticket, Concert
import requests
from django.contrib.auth import logout
client_id = 'client_id=MzIxMjg4OTl8MTY3Nzk0NjYzNi4zMDA4MDYz'

# Create your views here.
def home(request):
    cart_count = Ticket.objects.filter(bought=False).count()
    return render(request, 'home.html', {
        'cart_count': cart_count
    })

def logout_view(request):
    logout(request)
    return redirect('home')

def about(request):
    cart_count = Ticket.objects.filter(bought=False).count()
    return render(request, 'about.html', {
        'cart_count': cart_count
    })

def tickets_index(request):
    cart_count = Ticket.objects.filter(bought=False).count()
    tickets = Ticket.objects.all().filter(bought=True)
    return render(request, 'tickets/index.html', {
        'tickets': tickets, 'cart_count': cart_count
    })

def ticket_detail(request, ticket_id):
    cart_count = Ticket.objects.filter(bought=False).count()
    ticket = Ticket.objects.get(id=ticket_id)
    return render(request, 'tickets/detail.html', {
        'ticket': ticket, 'cart_count': cart_count
    })

def logout_view(request):
    logout(request)
    return redirect('home')

class TicketDelete(DeleteView):
    model = Ticket
    success_url = '/tickets'

def concerts_index(request):
    cart_count = Ticket.objects.filter(bought=False).count()
    concerts = Concert.objects.all()
    return render(request, 'concerts/concerts_index.html', {
        'concerts': concerts, 'cart_count': cart_count
    })

# The user search input is not getting saved because the function gets reset each time, and the variable "search" isn't saved
def concerts_search(request):
    cart_count = Ticket.objects.filter(bought=False).count()
    concerts = []
    search = request.GET.get('name')
    response = requests.get(f'https://api.seatgeek.com/2/events?q={search}&{client_id}').json()
    if search:
        for e in response['events']:
            # event_name = e['title']
            # concerts.append(event_name)
            concerts.append(e)
    return render(request, 'concerts/search.html', {
        'concerts': concerts, 'search': search, 'cart_count': cart_count
    })

def concert_detail(request, concert_id):
    cart_count = Ticket.objects.filter(bought=False).count()
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
        new_ticket.concert_id = concert.id
        new_ticket.save()
    return render(request, 'concerts/detail.html', {
        'concert': concert, 'cart_count': cart_count
    })

def add_ticket():
    pass

def nav_cart(request):
    cart_count = Ticket.objects.filter(bought=False).count()
    return render(request, 'base.html', {
        'cart_count': cart_count
    })

def cart(request):
    cart_count = Ticket.objects.filter(bought=False).count()
    items = Ticket.objects.filter(bought=False)
    return render(request, 'checkout/cart.html', {
        'items': items, 'cart_count': cart_count
    })

def checkout(request):
    items = Ticket.objects.filter(bought=False)
    for item in items:
        item.bought = True
        item.save()
    return redirect('ticket_index')
