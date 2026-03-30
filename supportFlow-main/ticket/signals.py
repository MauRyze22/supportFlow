from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from decouple import config
from django.conf import settings
from .models import Ticket
import resend

resend.api_key= config('RESEND_API_KEY')

# Variable para guardar el estado anterior
ticket_anterior = {}

@receiver(pre_save, sender=Ticket)
def guardar_estado_anterior(sender, instance, **kwargs):
    """Guarda el estado anterior del ticket antes de actualizar"""
    if instance.pk:  # Solo si el ticket ya existe
        try:
            ticket_viejo = Ticket.objects.get(pk=instance.pk)
            ticket_anterior[instance.pk] = {
                'estado': ticket_viejo.estado,
                'asignado': ticket_viejo.asignado,
            }
        except Ticket.DoesNotExist:
            pass


@receiver(post_save, sender=Ticket)
def notificar_cambios_ticket(sender, instance, created, **kwargs):
    """Envía emails cuando se crea o actualiza un ticket"""
    if created:
        from django.contrib.auth.models import User
        staff_emails = User.objects.filter(is_staff=True).values_list('email', flat=True)
        staff_emails = [email for email in staff_emails if email]  # Filtrar vacíos
        
        if staff_emails:
            resend.Emails.send({
                "subject":f'🎫 Nuevo Ticket #{instance.pk}: {instance.titulo}',
                "text":f"""
                        Hola equipo de soporte,
                            Se ha creado un nuevo ticket:
                            📋 Ticket: #{instance.pk}
                            🎯 Título: {instance.titulo}
                            📝 Descripción: {instance.descripcion[:200]}...
                            👤 Creado por: {instance.creador.username}
                            ⚡ Prioridad: {instance.get_prioridad_display()}
                                SupportFlow - Sistema de Tickets """,
                "from":"SupportFlow <onboarding@resend.dev>",
                "to":list(staff_emails),
            })
        else:
            return  # Salir aquí para tickets nuevos
    
    if instance.pk in ticket_anterior:
        estado_anterior = ticket_anterior[instance.pk]['estado']
        asignado_anterior = ticket_anterior[instance.pk]['asignado']

        if estado_anterior != instance.estado:
            if instance.creador and instance.creador.email:
                resend.Emails.send({
                    "subject":f'🔔 Actualización de Ticket #{instance.pk}',
                    "text":f"""
                            Hola {instance.creador.get_full_name() or instance.creador.username},

                            El estado de tu ticket ha sido actualizado:

                            📋 Ticket: #{instance.pk}
                            🎯 Título: {instance.titulo}
                            🔄 Estado anterior: {estado_anterior.upper()}
                            🔄 Estado nuevo: {instance.estado.upper()}
                            ---
                            SupportFlow - Sistema de Tickets
                            """,
                    "from":"SupportFlow <onboarding@resend.dev>",
                    "to":[instance.creador.email],
                })
    
        if asignado_anterior != instance.asignado and instance.asignado:
            if instance.asignado.email:
                resend.Emails.send({
                        "subject":f'📌 Te han asignado el Ticket #{instance.pk}',
                        "text":f"""
                                Hola {instance.asignado.get_full_name() or instance.asignado.username},

                                Se te ha asignado un nuevo ticket:

                                📋 Ticket: #{instance.pk}
                                🎯 Título: {instance.titulo}
                                📝 Descripción: {instance.descripcion[:200]}...
                                👤 Creado por: {instance.creador.username}
                                ⚡ Prioridad: {instance.get_prioridad_display()}
                                🏷️  Estado: {instance.get_estado_display()}
                                ---
                                SupportFlow - Sistema de Tickets
                                                        """,
                        "from":"SupportFlow <onboarding@resend.dev>",
                        "to":[instance.asignado.email],
                    })
        del ticket_anterior[instance.pk]