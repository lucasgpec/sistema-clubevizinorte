from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()

@csrf_exempt
def create_emergency_admin(request):
    """View de emergência para criar superusuário"""
    
    if request.method == 'POST' and request.POST.get('secret') == 'create_admin_now_123':
        try:
            username = 'clubeadmin'
            email = 'admin@clubevizinhorte.com'
            password = 'ClubVN2025!'
            
            # Remove usuário existente se houver
            if User.objects.filter(username=username).exists():
                User.objects.filter(username=username).delete()
            
            # Cria novo usuário
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                nome_completo='Administrador do Clube',
                cpf='000.000.000-00',
                tipo_usuario='ADMIN'
            )
            user.is_superuser = True
            user.is_staff = True
            user.save()
            
            return HttpResponse(f"""
            <h1>✅ SUPERUSUÁRIO CRIADO COM SUCESSO!</h1>
            <h2>Credenciais:</h2>
            <p><strong>Usuário:</strong> {username}</p>
            <p><strong>Senha:</strong> {password}</p>
            <p><strong>Email:</strong> {email}</p>
            <hr>
            <p><a href="/admin/">🔗 Acessar Admin</a></p>
            <p><a href="/">🏠 Voltar ao Sistema</a></p>
            """)
            
        except Exception as e:
            return HttpResponse(f"""
            <h1>❌ ERRO AO CRIAR USUÁRIO</h1>
            <p>Erro: {str(e)}</p>
            <p><a href="/">🏠 Voltar ao Sistema</a></p>
            """)
    
    return HttpResponse("""
    <h1>🔧 Criação de Emergência do Admin</h1>
    <form method="post">
        <label>Código Secreto:</label><br>
        <input type="password" name="secret" placeholder="Digite o código secreto"><br><br>
        <button type="submit">Criar Superusuário</button>
    </form>
    <p><strong>Código:</strong> create_admin_now_123</p>
    """)
