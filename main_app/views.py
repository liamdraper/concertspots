from django.shortcuts import render, redirect
from django.views.generic.edit import DeleteView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Ticket, Concert
import requests
from django.contrib.auth import logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
client_id = 'client_id=MzIxMjg4OTl8MTY3Nzk0NjYzNi4zMDA4MDYz'

@login_required
def home(request):
    cart_count = Ticket.objects.filter(bought=False, user=request.user).count()
    return render(request, 'home.html', {
        'cart_count': cart_count
    })

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def about(request):
    cart_count = Ticket.objects.filter(bought=False, user=request.user).count()
    return render(request, 'about.html', {
        'cart_count': cart_count
    })

@login_required
def tickets_index(request):
    cart_count = Ticket.objects.filter(bought=False, user=request.user).count()
    tickets = Ticket.objects.all().filter(bought=True, user=request.user)
    return render(request, 'tickets/index.html', {
        'tickets': tickets, 'cart_count': cart_count
    })

@login_required
def ticket_detail(request, ticket_id):
    cart_count = Ticket.objects.filter(bought=False, user=request.user).count()
    ticket = Ticket.objects.get(id=ticket_id)
    return render(request, 'tickets/detail.html', {
        'ticket': ticket, 'cart_count': cart_count
    })

def login_view(request):
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

class TicketDelete(LoginRequiredMixin, DeleteView):
    model = Ticket
    success_url = '/tickets'

@login_required
def concerts_index(request):
    cart_count = Ticket.objects.filter(bought=False, user=request.user).count()
    concerts = Concert.objects.all()
    return render(request, 'concerts/concerts_index.html', {
        'concerts': concerts, 'cart_count': cart_count
    })

@login_required
def concerts_search(request):
    cart_count = Ticket.objects.filter(bought=False, user=request.user).count()
    concerts = []
    search = request.POST.get('name')
    response = requests.get(f'https://api.seatgeek.com/2/events?q={search}&{client_id}').json()
    if request.POST.get('sort') == 'default':
        for e in response['events']:
            concerts.append(e)
    if request.POST.get('sort') == 'asc_name':
        for e in response['events']:
            concerts.append(e)
        concerts = sorted(concerts, key=lambda x:x['title'])
    if request.POST.get('sort') == 'dsc_name':
        for e in response['events']:
            concerts.append(e)
        concerts = sorted(concerts, key=lambda x:x['title'], reverse=True)
    if request.POST.get('sort') == 'asc_price':
        for e in response['events']:
            if e['stats']['average_price'] == None:
                e['stats']['average_price'] = 100;
            concerts.append(e)
        concerts = sorted(concerts, key=lambda x:x['stats']['average_price'])
    if request.POST.get('sort') == 'dsc_price':
        for e in response['events']:
            if e['stats']['average_price'] == None:
                e['stats']['average_price'] = 100;
            concerts.append(e)
        concerts = sorted(concerts, key=lambda x:x['stats']['average_price'], reverse=True)
    return render(request, 'concerts/search.html', {
        'concerts': concerts, 'search': search, 'cart_count': cart_count
    })

@login_required
def concert_detail(request, concert_id):
    cart_count = Ticket.objects.filter(bought=False, user=request.user).count()
    concert = Concert.objects.filter(api_id=concert_id).first()
    price = 100
    if request.POST.get('price') == None:
        price = 100
    if not concert:
        concert = Concert.objects.create(
            event_name = request.POST.get('event_name'),
            price = price,
            location = request.POST.get('location'),
            date = request.POST.get('date'),
            api_id = request.POST.get('api_id')
        )
    if request.POST.get('add') == 'add':
        new_ticket = Ticket(
            event_name = concert.event_name,
            price = concert.price,
            location = concert.location,
            date = concert.date
        )
        new_ticket.concert_id = concert.id
        new_ticket.user = request.user
        new_ticket.save()
        return redirect('ticket_index')   
    return render(request, 'concerts/detail.html', {
        'concert': concert, 'cart_count': cart_count
    })

@login_required
def nav_cart(request):
    cart_count = Ticket.objects.filter(bought=False, user=request.user).count()
    return render(request, 'base.html', {
        'cart_count': cart_count
    })

@login_required
def cart(request):
    cart_count = Ticket.objects.filter(bought=False, user=request.user).count()
    items = Ticket.objects.filter(bought=False, user=request.user)
    item_id = request.POST.get('delete')
    if request.POST:
        item = Ticket.objects.filter(id=item_id)
        item.delete()
    total = 0
    for item in items:
        total += item.price
    return render(request, 'checkout/cart.html', {
        'items': items, 'cart_count': cart_count, 'total': total
    })

@login_required
def checkout(request):
    items = Ticket.objects.filter(bought=False, user=request.user)
    if request.POST.get('empty') == 'Empty Cart':
        for item in items:
            item.delete()
    if request.POST.get('buy') == 'Buy Tickets':
        for item in items:
            item.bought = True
            item.save()
    return redirect('ticket_index')
