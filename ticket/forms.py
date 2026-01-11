from django import forms
from .models import Ticket, Comentario

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'
        exclude = ['creador', 'estado', 'asignado']
        

class TicketAsignadoForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'
        exclude = ['asignado']
        

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = '__all__'
        exclude = ['creador','ticket']
        
        