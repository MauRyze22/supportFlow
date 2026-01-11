from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, null = False, blank = False)
    descripcion = models.TextField()
    color = models.CharField(max_length=7, default='#007bff')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created']
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        
    def __str__(self):
        return self.nombre
    

class Ticket(models.Model):
    PRIORIDADES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('critica', 'Critica')
    ]
    
    ESTADOS = [
        ('abierto', 'Abierto'),
        ('cerrado', 'Cerrado'),
        ('en_progreso', 'En_progreso'),
        ('nuevo', 'Nuevo')
    ]
    
    titulo = models.CharField(max_length=50, blank = False, null = False)
    descripcion = models.TextField()
    prioridad = models.CharField(max_length = 20, choices=PRIORIDADES)
    categoria = models.ForeignKey('Categoria', on_delete=models.SET_NULL, null = True, blank = True)
    estado = models.CharField(max_length = 20, choices=ESTADOS, null = True, blank = True)
    creador = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)
    asignado = models.ForeignKey(User, on_delete=models.SET_NULL, null = True, blank = True, related_name='asignado')
    created = models.DateTimeField(auto_now_add=True)
    updated =  models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created']
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
        
    def get_absolute_url(self):
        return reverse('ticket_detail', kwargs={'pk': self.pk})
    
    def __str__(self):
        return self.titulo

    
class Comentario(models.Model):
    descripcion = models.TextField()
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE, related_name='comentarios')
    creador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comentarios_creador')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created']
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
    
    def __str__(self):
        return f'Comentario de: {self.creador}'
    
    
