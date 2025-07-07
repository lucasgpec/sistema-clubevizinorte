from django.urls import path
from . import views
from .views_admin import create_emergency_admin
from .views_debug import debug_users, fix_user
from .views_setup import setup_sistema

app_name = 'club'

urlpatterns = [
    # Página inicial - Login
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # SETUP COMPLETO: Configurar sistema do zero
    path('setup-sistema/', setup_sistema, name='setup_sistema'),
    
    # EMERGÊNCIA: Criar superusuário
    path('emergency-admin-create/', create_emergency_admin, name='emergency_admin'),
    
    # DEBUG: Ver e corrigir usuários
    path('debug-users/', debug_users, name='debug_users'),
    path('fix-user/', fix_user, name='fix_user'),
    
    # Dashboard principal
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Gestão de usuários (apenas para gestora)
    path('usuarios/', views.usuarios_list, name='usuarios_list'),
    path('usuarios/novo/', views.usuario_create, name='usuario_create'),
    path('usuarios/<int:pk>/editar/', views.usuario_edit, name='usuario_edit'),
    path('usuarios/<int:pk>/toggle/', views.usuario_toggle, name='usuario_toggle'),
    
    # Módulos do sistema
    path('socios/', views.socios_list, name='socios_list'),
    path('financeiro/', views.financeiro_dashboard, name='financeiro_dashboard'),
    path('locacoes/', views.locacoes_list, name='locacoes_list'),
    path('escolas/', views.escolas_list, name='escolas_list'),
    path('dayuse/', views.dayuse_list, name='dayuse_list'),
]
