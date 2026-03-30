# apps.py
from django.apps import AppConfig

class TicketConfig(AppConfig):  # 'TicketConfig' no 'TicketsConfig'
    name = 'ticket'  # 'ticket' no 'tickets'
    
    def ready(self):

        import ticket.signals 
 