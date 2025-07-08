from django.urls import path
from . import views
from .views_admin import create_emergency_admin
from .views_debug import debug_users, fix_user
from .views_setup import setup_sistema
from .views_status import status_sistema
from .views_media import test_media
from .views_escolas import escolas_list, escola_create, escola_edit, escola_delete
from .views_alunos_escola import alunos_escola_list, aluno_escola_create, aluno_escola_edit, aluno_escola_delete
from .views_esportes import esportes_list, esporte_create, esporte_edit, esporte_delete
from .views_horarios_esporte import horarios_aluno_list, horario_create, horario_edit, horario_delete
from .views_financeiro_escola import financeiro_escola_list, financeiro_escola_create, financeiro_escola_edit, financeiro_escola_delete
from .views_relatorios import relatorio_alunos, relatorio_financeiro, relatorio_cobrancas
from .views_exportacao import exportar_alunos_csv, exportar_financeiro_csv
from .views_cobrancas import cobrancas_list, cobranca_detail, cobranca_create, cobranca_emitir, configuracao_integracao
from .views_webhook import webhook_bancario

app_name = 'club'

urlpatterns = [
    # Página inicial - Login
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # STATUS: Ver status do sistema
    path('status/', status_sistema, name='status_sistema'),
    
    # TESTE: Testar arquivos de media
    path('test-media/', test_media, name='test_media'),
    
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
    path('socios/cliente/novo/', views.cliente_create, name='cliente_create'),
    path('socios/cliente/<int:pk>/', views.cliente_detail, name='cliente_detail'),
    path('socios/cliente/<int:pk>/editar/', views.cliente_edit, name='cliente_edit'),
    path('socios/cliente/<int:pk>/excluir/', views.cliente_delete, name='cliente_delete'),
    path('socios/socio/novo/', views.socio_create, name='socio_create'),
    path('socios/socio/<int:pk>/', views.socio_detail, name='socio_detail'),
    path('socios/socio/<int:pk>/editar/', views.socio_edit, name='socio_edit'),
    path('socios/socio/<int:pk>/excluir/', views.socio_delete, name='socio_delete'),
    
    path('financeiro/', views.financeiro_dashboard, name='financeiro_dashboard'),
    
    path('locacoes/', views.locacoes_list, name='locacoes_list'),
    path('locacoes/nova/', views.locacao_create, name='locacao_create'),
    path('locacoes/espaco/novo/', views.espaco_create, name='espaco_create'),
    
    path('escolas/', escolas_list, name='escolas_list'),
    path('escolas/nova/', escola_create, name='escola_create'),
    path('escolas/<int:pk>/editar/', escola_edit, name='escola_edit'),
    path('escolas/<int:pk>/excluir/', escola_delete, name='escola_delete'),
    path('escolas/<int:escola_pk>/alunos/', alunos_escola_list, name='alunos_escola_list'),
    path('escolas/<int:escola_pk>/alunos/novo/', aluno_escola_create, name='aluno_escola_create'),
    path('escolas/<int:escola_pk>/alunos/<int:pk>/editar/', aluno_escola_edit, name='aluno_escola_edit'),
    path('escolas/<int:escola_pk>/alunos/<int:pk>/excluir/', aluno_escola_delete, name='aluno_escola_delete'),
    
    path('dayuse/', views.dayuse_list, name='dayuse_list'),
    path('dayuse/novo/', views.dayuse_create, name='dayuse_create'),
    
    path('esportes/', esportes_list, name='esportes_list'),
    path('esportes/novo/', esporte_create, name='esporte_create'),
    path('esportes/<int:pk>/editar/', esporte_edit, name='esporte_edit'),
    path('esportes/<int:pk>/excluir/', esporte_delete, name='esporte_delete'),
    
    path('alunos/<int:aluno_pk>/horarios/', horarios_aluno_list, name='horarios_aluno_list'),
    path('alunos/<int:aluno_pk>/horarios/novo/', horario_create, name='horario_create'),
    path('alunos/<int:aluno_pk>/horarios/<int:pk>/editar/', horario_edit, name='horario_edit'),
    path('alunos/<int:aluno_pk>/horarios/<int:pk>/excluir/', horario_delete, name='horario_delete'),
    
    path('escolas/<int:escola_pk>/financeiro/', financeiro_escola_list, name='financeiro_escola_list'),
    path('escolas/<int:escola_pk>/financeiro/novo/', financeiro_escola_create, name='financeiro_escola_create'),
    path('escolas/<int:escola_pk>/financeiro/<int:pk>/editar/', financeiro_escola_edit, name='financeiro_escola_edit'),
    path('escolas/<int:escola_pk>/financeiro/<int:pk>/excluir/', financeiro_escola_delete, name='financeiro_escola_delete'),
    
    path('relatorios/alunos/', relatorio_alunos, name='relatorio_alunos'),
    path('relatorios/financeiro/', relatorio_financeiro, name='relatorio_financeiro'),
    path('relatorios/alunos/exportar/', exportar_alunos_csv, name='exportar_alunos_csv'),
    path('relatorios/financeiro/exportar/', exportar_financeiro_csv, name='exportar_financeiro_csv'),
    
    path('financeiro/cobrancas/', cobrancas_list, name='cobrancas_list'),
    path('financeiro/cobrancas/nova/', cobranca_create, name='cobranca_create'),
    path('financeiro/cobrancas/<int:pk>/', cobranca_detail, name='cobranca_detail'),
    path('financeiro/cobrancas/<int:pk>/emitir/', cobranca_emitir, name='cobranca_emitir'),
    path('financeiro/integracao/', configuracao_integracao, name='configuracao_integracao'),
    path('financeiro/webhook/', webhook_bancario, name='webhook_bancario'),
    path('financeiro/relatorio-cobrancas/', relatorio_cobrancas, name='relatorio_cobrancas'),
]
