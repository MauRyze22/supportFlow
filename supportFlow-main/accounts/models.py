from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'perfil')
    numero = models.CharField(max_length=15, blank = True, null = True)
    email = models.EmailField(null = True, blank = True)
    biografia = models.TextField(blank = True, null =True)
    imagen = models.ImageField(null = True, blank = True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
        
    def __str__(self):
        return self.usuario.username
    
    @receiver(post_save, sender=User)
    def crear_perfil(sender, instance, created, **kwargs):
        if created:
            Perfil.objects.create(usuario = instance, email = instance.email)
            
            
    @receiver(post_save, sender=User)        
    def guardar_perfil(sender, instance, **kwargs):
        if hasattr(instance, 'perfil'):
            instance.perfil.save()
    