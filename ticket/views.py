from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from .forms import TicketForm, TicketAsignadoForm, ComentarioForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Ticket, Comentario, Categoria
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponseForbidden
from datetime import datetime, date
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

class HomeView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'ticket/home.html'
    login_url = '/accounts/login-user/'
    
    def get_context_data(self, **kwargs):
        tickets = Ticket.objects.filter(Q(creador = self.request.user)|
                                        Q(asignado = self.request.user))
        
        comentarios = Comentario.objects.filter(creador = self.request.user)
        context = super().get_context_data(**kwargs)
        context['total_tickets'] = tickets.count()
        context['tickets_sin_asignar'] = tickets.filter(asignado = None)[0:5]
        context['tickets_asignado'] = tickets.count()
        
        if self.request.user.is_staff:
            context['total_tickets_admin'] = Ticket.objects.all().count()
            context['total_comentarios_admin'] = Comentario.objects.all().count()
                                                              
        context['tickets_en_progreso'] = tickets.select_related('creador', 'asignado')\
                                            .filter(estado__icontains = 'en_progreso')\
                                            .order_by('-created')[0:5]
                                            
        context['tickets_abiertos'] = tickets.select_related('creador', 'asignado')\
                                            .filter(estado__icontains = 'abierto')\
                                            .order_by('-created')[0:5]
                                            
        context['tickets_cerrados'] = tickets.select_related('creador', 'asignado')\
                                            .filter(estado__icontains = 'cerrado')\
                                            .order_by('-created')[0:5]
                                            
        context['tickets_nuevos'] = tickets.select_related('creador', 'asignado')\
                                            .filter(estado__icontains = 'nuevo')\
                                            .order_by('-created')[0:5]
                                            
        context['comentarios_recientes'] = comentarios.select_related('creador').order_by('-created')[0:5]
        context['total_comentarios'] = comentarios.count()
        
        return context
      

class TicketListView(LoginRequiredMixin, generic.ListView):
    model = Ticket
    template_name = 'ticket/ticket_list.html'
    context_object_name = 'tickets'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
                    
        q = self.request.GET.get('q')
        
        if self.request.user.is_staff:
            queryset = Ticket.objects.all() 
        else:
            queryset = Ticket.objects.filter(Q(creador = self.request.user)|
                                         Q(asignado = self.request.user)).distinct()
        
        # Filtros avanzados
        
        estado = self.request.GET.get('estado')
        categoria = self.request.GET.get('categoria')
        prioridad = self.request.GET.get('prioridad')
        asignado = self.request.GET.get('asignado')
        
        if estado:
            queryset = queryset.filter(estado = estado)
        if categoria:
            queryset = queryset.filter(categoria=categoria)
        if prioridad:
            queryset = queryset.filter(prioridad = prioridad)
        if asignado:
            queryset = queryset.filter(asignado = asignado)
            
        fecha_desde = self.request.GET.get('fecha_desde')
        fecha_hasta = self.request.GET.get('fecha_hasta')
        
        if fecha_desde:
            try:
                fecha = datetime.strptime(fecha_desde, '%Y-%m-%d')
                queryset = queryset.filter(created__date__gte = fecha)
            except ValueError:
                pass
            
        if fecha_hasta:
            try:
                fecha = datetime.strptime(fecha_hasta, '%Y-%m-%d')
                queryset = queryset.filter(created__date__lte = fecha)
            except ValueError:
                pass
            
        if q:
            queryset = queryset.filter((Q(creador = self.request.user)|Q(asignado=self.request.user)) &
                                   (Q(estado__icontains = q)|
                                   Q(prioridad__icontains = q)|
                                   Q(titulo__icontains = q))).distinct()
            
        return queryset
    
    def get_context_data(self, **kwargs):
        tickets = Ticket.objects.all()
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['estados'] = Ticket.ESTADOS
        context['prioridades'] = Ticket.PRIORIDADES
        context['filtro_actual'] = self.request.GET
        context['fecha_desde_actual'] = self.request.GET.get('fecha_desde')
        context['fecha_hasta_actual'] = self.request.GET.get('fecha_hasta')
        
        return context
        
        
class TicketCreateView(LoginRequiredMixin, generic.CreateView):
    model = Ticket
    template_name = 'ticket/ticket_form.html'
    form_class = TicketForm
    
    def form_valid(self, form):
        form.instance.creador = self.request.user
        form.instance.estado = 'nuevo'
        ticket = form.save()
        
        staff_emails = User.objects.filter(is_staff = True).values_list('email', flat = True)
        
        if staff_emails:
            send_mail(
                subject=f'Nuevo ticket #{ticket.pk}: {ticket.titulo}',
                message=f"El usuario: {self.request.user.username} creó un nuevo ticket.\n\n"
                        f"Título: {ticket.titulo}\n"
                        f"Descripción: {ticket.descripcion[:300]}...\n"
                        f"Ver: http://localhost:8000{ticket.get_absolute_url()}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=list(staff_emails),
                fail_silently=False,
            )              
        messages.success(self.request, 'Ticket creado correctamente')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('ticket_list')
    
    
class TicketDetailView(LoginRequiredMixin, generic.DetailView):
    model = Ticket
    template_name = 'ticket/ticket_detail.html'
    context_object_name = 'ticket'
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Ticket.objects.select_related('creador', 'asignado', 'categoria').all()
        return Ticket.objects.select_related('creador', 'asignado', 'categoria').filter(Q(creador = self.request.user)|
                                                                         Q(asignado = self.request.user))
        
        
    def get_context_data(self, **kwargs):
        ticket = get_object_or_404(Ticket, pk = self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['comentarios'] = Comentario.objects.select_related('creador').filter(ticket = ticket)
        return context
    
class TicketUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Ticket
    template_name = 'ticket/ticket_form.html'
    form_class = TicketForm
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.filter(Q(creador = self.request.user)|
                                     Q(asignado = self.request.user))
    
    def get_form_class(self):
        if self.request.user.is_staff or self.object.asignado == self.request.user:
            return TicketAsignadoForm
        return TicketForm
    
    def get_success_url(self):
        return reverse_lazy('ticket_list')

    
class TicketDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Ticket
    template_name = 'ticket/delete.html'
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.filter(creador = self.request.user)
    
    def get_success_url(self):
        messages.success(self.request, 'Ticket eliminado correctamente')
        return reverse_lazy('ticket_list')

        
class ComentarioCreateView(LoginRequiredMixin, generic.CreateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'ticket/ticket_detail.html'
    
    def get_success_url(self):
        messages.success(self. request,'Comentario creado correctamente')
        return reverse_lazy('ticket_detail', kwargs = {'pk': self.kwargs['pk']})
    
    def form_valid(self, form):
        form.instance.creador = self.request.user
        form.instance.ticket = get_object_or_404(Ticket, pk = self.kwargs['pk'])
        return super().form_valid(form)
    
class ComentarioUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'ticket/comentario_update.html'
    
    def get_success_url(self):
        comentario = get_object_or_404(Comentario, pk = self.kwargs['pk'])
        messages.success(self.request, 'Comentario actualizado correctamente')
        return reverse_lazy('ticket_detail', kwargs = {'pk':comentario.ticket.id})
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Comentario.objects.all()
        return Comentario.objects.filter(creador=self.request.user)   

class ComentarioDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Comentario
    template_name = 'ticket/delete.html'
     
    def get_queryset(self):
        if self.request.user.is_staff:
            return Comentario.objects.all()
        return Comentario.objects.filter(creador = self.request.user)
    
    def get_success_url(self):
        comentario = get_object_or_404(Comentario, pk = self.kwargs['pk'])
        messages.success(self.request, 'Mensaje eliminado correctamente')
        return reverse_lazy('ticket_detail', kwargs = {'pk': comentario.ticket.id})
    
    
class CategoriaListView(LoginRequiredMixin, generic.ListView):
    model = Categoria
    template_name = 'ticket/categoria_list.html'
    context_object_name = 'categorias'
    queryset = Categoria.objects.all()
    
    
class CategoriaDetailView(LoginRequiredMixin, generic.DetailView):
    model = Categoria
    template_name = 'ticket/categoria_detail.html'
    queryset = Categoria.objects.all()
    context_object_name = 'categoria'