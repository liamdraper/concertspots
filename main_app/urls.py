from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('tickets/', views.tickets_index, name='index'),
    path('tickets/<int:ticket_id>', views.ticket_detail, name='detail'),
    path('tickets/<int:pk>/delete/', views.TicketDelete.as_view(), name='ticket_delete'),
    path('tickets/create/', views.add_ticket, name='ticket_create'),
    path('concerts/', views.concerts, name='concerts'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout')
]