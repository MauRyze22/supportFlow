from celery import shared_task
from decouple import config
import resend
from resend.exceptions import ResendError

resend.api_key = config('RESEND_API_KEY')

@shared_task
def enviar_email_nuevo_ticket(ticket_pk, titulo, descripcion, creador_username, prioridad, staff_emails):
    try:
        resend.Emails.send({
            "subject": f'🎫 Nuevo Ticket #{ticket_pk}: {titulo}',
            "text": f"""
                    Hola equipo de soporte,
                        Se ha creado un nuevo ticket:
                        📋 Ticket: #{ticket_pk}
                        🎯 Título: {titulo}
                        📝 Descripción: {descripcion[:200]}...
                        👤 Creado por: {creador_username}
                        ⚡ Prioridad: {prioridad}
                            SupportFlow - Sistema de Tickets """,
            "from": "SupportFlow <onboarding@resend.dev>",
            "to": list(staff_emails),
        })
    except ResendError as e:
        print(f'[DEBUG] Atributos del error: {e.__dict__}')
        print(f'[DEBUG] str(e): {str(e)}')


@shared_task
def enviar_email_cambio_estado(ticket_pk, titulo, estado_anterior, estado_nuevo, creador_email, creador_nombre):
    try:
        resend.Emails.send({
            "subject": f'🔔 Actualización de Ticket #{ticket_pk}',
            "text": f"""
                    Hola {creador_nombre},

                    El estado de tu ticket ha sido actualizado:

                    📋 Ticket: #{ticket_pk}
                    🎯 Título: {titulo}
                    🔄 Estado anterior: {estado_anterior.upper()}
                    🔄 Estado nuevo: {estado_nuevo.upper()}
                    ---
                    SupportFlow - Sistema de Tickets
                    """,
            "from": "SupportFlow <onboarding@resend.dev>",
            "to": [creador_email],
        })
    except ResendError as e:
        print(f'[DEBUG] Atributos del error: {e.__dict__}')
        print(f'[DEBUG] str(e): {str(e)}')


@shared_task
def enviar_email_asignacion(ticket_pk, titulo, descripcion, creador_username, prioridad, estado, asignado_email, asignado_nombre):
    try:
        resend.Emails.send({
            "subject": f'📌 Te han asignado el Ticket #{ticket_pk}',
            "text": f"""
                    Hola {asignado_nombre},

                    Se te ha asignado un nuevo ticket:

                    📋 Ticket: #{ticket_pk}
                    🎯 Título: {titulo}
                    📝 Descripción: {descripcion[:200]}...
                    👤 Creado por: {creador_username}
                    ⚡ Prioridad: {prioridad}
                    🏷️  Estado: {estado}
                    ---
                    SupportFlow - Sistema de Tickets
                    """,
            "from": "SupportFlow <onboarding@resend.dev>",
            "to": [asignado_email],
        })
    except ResendError as e:
        print(f'[DEBUG] Atributos del error: {e.__dict__}')
        print(f'[DEBUG] str(e): {str(e)}')
