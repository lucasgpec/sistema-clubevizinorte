from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from .models import ConfiguracaoClube

User = get_user_model()

@csrf_exempt
def setup_sistema(request):
    """Setup completo do sistema"""
    
    if request.method == 'POST' and request.POST.get('secret') == 'setup_sistema_123':
        try:
            # 1. Criar Admin
            admin_username = 'clubeadmin'
            admin_email = 'admin@clubevizinhorte.com'
            admin_password = 'ClubVN2025!'
            
            if User.objects.filter(username=admin_username).exists():
                User.objects.filter(username=admin_username).delete()
            
            admin_user = User.objects.create_user(
                username=admin_username,
                email=admin_email,
                password=admin_password,
                nome_completo='Administrador do Clube',
                cpf='000.000.000-00',
                tipo_usuario='ADMIN'
            )
            admin_user.is_superuser = True
            admin_user.is_staff = True
            admin_user.is_active = True
            admin_user.ativo = True
            admin_user.save()
            
            # 2. Criar Gestora
            gestora_username = 'gestora'
            gestora_email = 'gestora@clubevizinhorte.com'
            gestora_password = 'gestora123'
            
            if User.objects.filter(username=gestora_username).exists():
                User.objects.filter(username=gestora_username).delete()
            
            gestora_user = User.objects.create_user(
                username=gestora_username,
                email=gestora_email,
                password=gestora_password,
                nome_completo='Gestora do Clube',
                cpf='111.111.111-11',
                tipo_usuario='GESTORA'
            )
            gestora_user.is_active = True
            gestora_user.ativo = True
            gestora_user.pode_gerenciar_socios = True
            gestora_user.pode_gerenciar_financeiro = True
            gestora_user.pode_gerenciar_locacoes = True
            gestora_user.pode_gerenciar_escolas = True
            gestora_user.pode_gerenciar_dayuse = True
            gestora_user.save()
            
            # 3. Criar Configuração do Clube
            if not ConfiguracaoClube.objects.filter(ativa=True).exists():
                config = ConfiguracaoClube.objects.create(
                    nome_clube='Clube Vizinho Norte',
                    cor_primaria='#231f1e',
                    cor_secundaria='#304097',
                    cor_terciaria='#3a9ed2',
                    ativa=True
                )
            
            return HttpResponse(f"""
            <h1>✅ SISTEMA CONFIGURADO COM SUCESSO!</h1>
            
            <h2>👨‍💼 ADMINISTRADOR:</h2>
            <p><strong>URL:</strong> <a href="/admin/">/admin/</a></p>
            <p><strong>Usuário:</strong> {admin_username}</p>
            <p><strong>Senha:</strong> {admin_password}</p>
            <p><strong>Email:</strong> {admin_email}</p>
            
            <h2>👩‍💼 GESTORA:</h2>
            <p><strong>URL:</strong> <a href="/login/">/login/</a></p>
            <p><strong>Usuário:</strong> {gestora_username}</p>
            <p><strong>Senha:</strong> {gestora_password}</p>
            <p><strong>Email:</strong> {gestora_email}</p>
            
            <hr>
            <h3>🎯 PRÓXIMOS PASSOS:</h3>
            <ol>
                <li><a href="/admin/">Acessar Admin</a> e configurar logo</li>
                <li><a href="/login/">Testar Login da Gestora</a></li>
                <li><a href="/">Voltar ao Sistema</a></li>
            </ol>
            
            <p><strong>⚠️ IMPORTANTE:</strong> Altere as senhas após o primeiro acesso!</p>
            """)
            
        except Exception as e:
            return HttpResponse(f"""
            <h1>❌ ERRO NO SETUP</h1>
            <p>Erro: {str(e)}</p>
            <p><a href="/">🏠 Voltar ao Sistema</a></p>
            """)
    
    return HttpResponse("""
    <h1>🚀 Setup Completo do Sistema</h1>
    <p>Este comando criará:</p>
    <ul>
        <li>✅ Usuário Administrador</li>
        <li>✅ Usuário Gestora</li>
        <li>✅ Configuração do Clube</li>
    </ul>
    
    <form method="post">
        <label>Código Secreto:</label><br>
        <input type="password" name="secret" placeholder="Digite o código secreto"><br><br>
        <button type="submit" style="background: #304097; color: white; padding: 10px 20px; border: none; border-radius: 5px;">
            🚀 Configurar Sistema
        </button>
    </form>
    <p><strong>Código:</strong> setup_sistema_123</p>
    """)
