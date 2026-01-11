from django.urls import path
from .views import *


urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),
    
    # Ticket
    path('ticket-list/', TicketListView.as_view(), name = 'ticket_list'),
    path('ticket-create/', TicketCreateView.as_view(), name = 'ticket_create'),
    path('ticket-detail/<int:pk>/', TicketDetailView.as_view(), name = 'ticket_detail'),
    path('ticket-update/<int:pk>/', TicketUpdateView.as_view(), name = 'ticket_update'),
    path('ticket-delete/<int:pk>/', TicketDeleteView.as_view(), name = 'ticket_delete'),
    
    # Comentarios
    path('comentario-create/<int:pk>/', ComentarioCreateView.as_view(), name = 'comentario_create'),
    path('comentario-update/<int:pk>/', ComentarioUpdateView.as_view(), name = 'comentario_update'),
    path('comentario-delete/<int:pk>/', ComentarioDeleteView.as_view(), name = 'comentario_delete'),
    
    # Categorias
    path('categoria-list/', CategoriaListView.as_view(), name = 'categoria_list'),
    path('categoria-detail/<int:pk>/', CategoriaDetailView.as_view(), name = 'categoria_detail'),
    
]
