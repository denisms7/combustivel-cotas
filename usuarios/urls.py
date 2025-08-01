from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import UsuarioEdit, UsuarioDetailView, alterar_usuario

urlpatterns = [
    path('perfil/', UsuarioDetailView.as_view(), name='perfil'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),

    path('senha/', UsuarioEdit.as_view(), name='alterar_senha'),
    path('usuario/', alterar_usuario, name='alterar_usuario'),

    # path('reset/', include('django.contrib.auth.urls')),
]