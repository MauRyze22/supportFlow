from django.shortcuts import render, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import generic
from django.contrib.auth.models import User
from .forms import UserCustomForm, PerfilForm
from .models import Perfil

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'registration/login_register.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        messages.success(self.request, 'Ha iniciado sesion de manera exitosa')
        return reverse_lazy('home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'login'
        return context
    
        
class CustomRegisterView(generic.CreateView):
    model = User
    form_class = UserCustomForm
    template_name = 'registration/login_register.html'
    
    def get_success_url(self):
        return reverse_lazy('login_user')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Se ha registrado correctamente')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Hay datos erroneos ')
        return super().form_invalid(form)
    
    
class CustomLogoutView(LogoutView):
    def get_success_url(self):
        return reverse_lazy('login_user')
    
    
class PerfilDetailView(LoginRequiredMixin, generic.DetailView):
    model = Perfil
    template_name = 'registration/perfil_detail.html'
    context_object_name = 'perfil_user'
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Perfil.objects.select_related('usuario').all()
        return Perfil.objects.select_related('usuario').filter(usuario = self.request.user)
    
    
    
class PerfilUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Perfil
    template_name = 'registration/perfil_update.html'
    form_class = PerfilForm
    
    def get_success_url(self):
        return reverse_lazy('perfil_detail', kwargs = {'pk':self.kwargs['pk']})
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Perfil.o-bjects.all()
        return Perfil.objects.filter(usuario = self.request.user)
    