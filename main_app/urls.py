from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('about/', views.about, name='about'),
    path('tickets/', views.tickets_index, name='ticket_index'),
    path('tickets/<int:ticket_id>', views.ticket_detail, name='ticket_detail'),
    path('tickets/<int:pk>/delete/', views.TicketDelete.as_view(), name='ticket_delete'),
    path('tickets/create/', views.add_ticket, name='ticket_create'),
    path('concerts/', views.concerts, name='concerts'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout')
    path('concerts/', views.concerts_search, name='search'),
    path('concerts/index', views.concerts_index, name='concerts_index'),
    path('concerts/<int:concert_id>', views.concert_detail, name='concert_detail'),
]