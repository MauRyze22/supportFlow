from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Ticket
from .tasks import enviar_email_nuevo_ticket, enviar_email_cambio_estado, enviar_email_asignacion

# Variable para guardar el estado anterior
ticket_anterior = {}

@receiver(pre_save, sender=Ticket)
def guardar_estado_anterior(sender, instance, **kwargs):
    if instance.pk:
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
    if created:
        from django.contrib.auth.models import User
        staff_emails = list(User.objects.filter(is_staff=True).values_list('email', flat=True))
        staff_emails = [email for email in staff_emails if email]

        if staff_emails:
            enviar_email_nuevo_ticket.delay(
                ticket_pk=instance.pk,
                titulo=instance.titulo,
                descripcion=instance.descripcion,
                creador_username=instance.creador.username,
                prioridad=instance.get_prioridad_display(),
                staff_emails=staff_emails,
            )

    if instance.pk in ticket_anterior:
        estado_anterior = ticket_anterior[instance.pk]['estado']
        asignado_anterior = ticket_anterior[instance.pk]['asignado']

        if estado_anterior != instance.estado:
            if instance.creador and instance.creador.email:
                enviar_email_cambio_estado.delay(
                    ticket_pk=instance.pk,
                    titulo=instance.titulo,
                    estado_anterior=estado_anterior,
                    estado_nuevo=instance.estado,
                    creador_email=instance.creador.email,
                    creador_nombre=instance.creador.get_full_name() or instance.creador.username,
                )

        if asignado_anterior != instance.asignado and instance.asignado:
            if instance.asignado.email:
                enviar_email_asignacion.delay(
                    ticket_pk=instance.pk,
                    titulo=instance.titulo,
                    descripcion=instance.descripcion,
                    creador_username=instance.creador.username,
                    prioridad=instance.get_prioridad_display(),
                    estado=instance.get_estado_display(),
                    asignado_email=instance.asignado.email,
                    asignado_nombre=instance.asignado.get_full_name() or instance.asignado.username,
                )

        del ticket_anterior[instance.pk]