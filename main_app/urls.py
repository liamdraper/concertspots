from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('tickets/', views.tickets_index, name='index'),
    path('tickets/create/', views.TicketCreate.as_view(), name='tickets_create'),
    path('concerts/', views.concerts, name='concerts')
]