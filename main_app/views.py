from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Ticket

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
