from django.urls import path
from .views import *

urlpatterns = [
        # Logueo
    path('login-user/', CustomLoginView.as_view(), name = 'login_user'),
    path('register-user/', CustomRegisterView.as_view(), name = 'register_user'),
    path('logout-user/', CustomLogoutView.as_view(), name = 'logout_user'),
    path('perfil-detail/<int:pk>/', PerfilDetailView.as_view(), name = 'perfil_detail'),
    path('perfil-update/<int:pk>/', PerfilUpdateView.as_view(), name = 'perfil_update'),
    
]
