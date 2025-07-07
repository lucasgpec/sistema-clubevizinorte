from django.db import migrations
from django.contrib.auth import get_user_model

def criar_usuarios_iniciais(apps, schema_editor):
    User = get_user_model()
    ConfiguracaoClube = apps.get_model('club', 'ConfiguracaoClube')
    
    # Criar Administrador
    if not User.objects.filter(username='clubeadmin').exists():
        admin = User.objects.create_user(
            username='clubeadmin',
            email='admin@clubevizinhorte.com',
            password='ClubVN2025!',
            nome_completo='Administrador do Clube',
            cpf='000.000.000-00',
            tipo_usuario='ADMIN'
        )
        admin.is_superuser = True
        admin.is_staff = True
        admin.is_active = True
        admin.ativo = True
        admin.save()
    
    # Criar Gestora
    if not User.objects.filter(username='gestora').exists():
        gestora = User.objects.create_user(
            username='gestora',
            email='gestora@clubevizinhorte.com',
            password='gestora123',
            nome_completo='Gestora do Clube',
            cpf='111.111.111-11',
            tipo_usuario='GESTORA'
        )
        gestora.is_active = True
        gestora.ativo = True
        gestora.pode_gerenciar_socios = True
        gestora.pode_gerenciar_financeiro = True
        gestora.pode_gerenciar_locacoes = True
        gestora.pode_gerenciar_escolas = True
        gestora.pode_gerenciar_dayuse = True
        gestora.save()
    
    # Criar Configuração do Clube
    if not ConfiguracaoClube.objects.filter(ativa=True).exists():
        ConfiguracaoClube.objects.create(
            nome_clube='Clube Vizinho Norte',
            cor_primaria='#231f1e',
            cor_secundaria='#304097',
            cor_terciaria='#3a9ed2',
            ativa=True
        )

def reverter_usuarios_iniciais(apps, schema_editor):
    User = get_user_model()
    ConfiguracaoClube = apps.get_model('club', 'ConfiguracaoClube')
    
    User.objects.filter(username__in=['clubeadmin', 'gestora']).delete()
    ConfiguracaoClube.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('club', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(criar_usuarios_iniciais, reverter_usuarios_iniciais),
    ]
