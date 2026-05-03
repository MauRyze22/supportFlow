from django.test import TestCase, override_settings
from .models import Ticket, Comentario, Categoria
from django.contrib.auth.models import User
from unittest.mock import patch

# Create your tests here.

class TestTicker(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username = 'testuser',
            password = 'testpassword',
            email = 'amaurymperez22@gmail.com'
        )

        self.staff = User.objects.create_user(
            username = 'testuser1',
            password = 'testpassword2',
            email = 'amaurymperez22@gmail.com',
            is_staff = True
        )

        self.ticket = Ticket.objects.create(
            titulo = 'Test titulo',
            descripcion = 'Test Descripcion',
            prioridad = 'baja',
            estado = 'nuevo',
            creador = self.user
        )

        self.comentario = Comentario.objects.create(
            descripcion = 'Test Comentario',
            creador = self.user,
            ticket = self.ticket
        )

        self.categoria = Categoria.objects.create(
            nombre = 'CategoriaTest',
            descripcion = 'DescripcionTest'
        )


    def authenticate_user_staff(self):
        self.client.login(username='testuser1', password='testpassword2')

        
    def authenticate_user(self):
        self.client.login(username='testuser', password='testpassword')


    def test_listar_ticket_con_authentication(self):
        self.authenticate_user()
        response = self.client.get('/ticket-list/')
        self.assertEqual(response.status_code, 200)


    def test_listar_ticket_sin_authentication(self):
        response = self.client.get('/ticket-list/')
        self.assertEqual(response.status_code, 302)


    def test_crear_ticket_sin_authentication(self):
        response = self.client.post('/ticket-create/')
        self.assertEqual(response.status_code, 302)

    
    def test_crear_ticket_con_authentication(self):
        self.authenticate_user()
        response = self.client.post('/ticket-create/', {
            'titulo':'Test titulo',
            'descripcion': 'Test Descripcion',
            'prioridad':'baja'
        })

        self.assertEqual(response.status_code, 302)

    def test_crear_ticket_de_otro_usuario(self):
        self.authenticate_user()
        usuario2 = User.objects.create_user(
            username = 'testuser2',
            password = 'testpassword2'
        )
        response = self.client.post('/ticket-create/',{
            'titulo':'Test titulo',
            'descripcion': 'Test Descripcion',
            'prioridad':'baja',
            'creador': usuario2.id
        })

        self.assertEqual(response.status_code, 302)

    def test_ver_ticket_de_otro_usuario(self):
        self.authenticate_user()
        usuario2 = User.objects.create_user(
            username = 'testuser2',
            password = 'testpassword2'
        )
        ticket = Ticket.objects.create(
            titulo = 'Test titulo',
            descripcion = 'Test Descripcion',
            prioridad = 'baja',
            creador = usuario2
        )

        response = self.client.get(f'/ticket-detail/{ticket.id}/')
        self.assertEqual(response.status_code, 404)


    def test_actualizar_ticket_con_authenticate(self):
        self.authenticate_user()
        response = self.client.post(f'/ticket-update/{self.ticket.id}/',{
            'titulo': 'Ticket actualizado',
            'descripcion': 'Descripcion actualizada',
            'prioridad': 'baja',
            'creador': self.user.id
        })
        self.assertEqual(response.status_code, 302)


    def test_actualizar_ticket_sin_authenticate(self):
        response = self.client.post(f'/ticket-update/{self.ticket.id}/',{
            'titulo': 'Ticket actualizado',
            'descripcion': 'Descripcion actualizada',
            'prioridad': 'baja',
            'creador': self.user.id
        })
        self.assertEqual(response.status_code, 302)


    def test_eliminar_ticket(self):
        self.authenticate_user()
        response = self.client.post(f'/ticket-delete/{self.ticket.id}/')
        self.assertEqual(response.status_code, 302)

    
    def test_ver_categorias_con_authenticate(self):
        self.authenticate_user()
        response = self.client.get('/categoria-list/')
        self.assertEqual(response.status_code, 200)


    def test_ver_categorias_sin_authenticate(self):
        response = self.client.get('/categoria-list/')
        self.assertEqual(response.status_code, 302)


    def test_ver_categoria_con_authentication(self):
        self.authenticate_user()
        response = self.client.get(f'/categoria-detail/{self.categoria.id}/')
        self.assertEqual(response.status_code, 200)


    def test_ver_categoria_sin_authentication(self):
        response = self.client.get(f'/categoria-detail/{self.categoria.id}/')
        self.assertEqual(response.status_code, 302)


    def test_crear_comentario_con_authenticate(self):
        self.authenticate_user()
        response = self.client.post(f'/comentario-create/{self.ticket.id}/',{
            'descripcion': 'Test Comentario',
            'ticket': self.ticket.id,
            'creador': self.user.id
        })
        self.assertEqual(response.status_code, 302)

    def test_crear_comentario_sin_authenticate(self):
        response = self.client.post(f'/comentario-create/{self.ticket.id}/',{
            'descripcion': 'Test Comentario',
            'ticket': self.ticket.id,
            'creador': self.user.id
        })
        self.assertEqual(response.status_code, 302)

    
    def test_actualizar_comentario_sin_authenticate(self):
        response = self.client.post(f'/comentario-update/{self.ticket.id}/',{
            'descripcion': 'Test Comentario Actualizado',
            'ticket': self.ticket.id,
            'creador': self.user.id
        })
        self.assertEqual(response.status_code, 302)


    def test_actualizar_comentario_de_otro_usuario(self):
        usuario2 = User.objects.create_user(
            username = 'testuser3',
            password = 'testpassword3'
        )
        self.client.force_login(usuario2)
        response = self.client.post(f'/comentario-update/{self.comentario.id}/',{
            'descripcion': 'Test comentario q no puede ser actualizado por este usuario',
            'ticket': self.ticket.id,
            'creador': usuario2.id
        })
        # Debe darr 404 porque el usuario no es el creador del comentario y el queryset esta echo para 
        # mostrar solo los comentarios del usuario autenticado
        self.assertEqual(response.status_code, 404)

    
    def test_eliminar_comentario_sin_authenticate(self):
        response = self.client.post(f'/comentario-delete/{self.comentario.id}/')
        self.assertEqual(response.status_code, 302)


    def test_eliminar_comentario_con_authenticate(self):
        self.authenticate_user()
        response = self.client.post(f'/comentario-delete/{self.comentario.id}/')
        self.assertEqual(response.status_code, 302)


    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_enviar_email_nuevo_ticket_celery(self):
        self.authenticate_user_staff()
        with patch('ticket.signals.enviar_email_nuevo_ticket.delay') as mock_email:
            Ticket.objects.create(
                titulo = 'Ticket actualizado1',
                descripcion = 'Descripcion actualizada1',
                prioridad = 'baja',
                creador = self.staff
            )
            self.assertTrue(mock_email.called)


    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)    
    def test_enviar_email_cambio_estado_celery(self):
        self.authenticate_user_staff()
        with patch('ticket.signals.enviar_email_cambio_estado.delay') as mock_email:
            self.ticket.estado = 'abierto'
            self.ticket.save()
            self.assertTrue(mock_email.called)


    @override_settings(CELERY_TASK_ALWAYS_EAGER=True) 
    def test_enviar_email_asignacion_celery(self):
        self.authenticate_user_staff()
        with patch('ticket.signals.enviar_email_asignacion.delay') as mock_email:
            self.ticket.asignado = self.user
            self.ticket.save()
            self.assertTrue(mock_email.called)
