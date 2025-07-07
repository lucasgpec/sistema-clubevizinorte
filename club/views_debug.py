from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()

@csrf_exempt
def debug_users(request):
    """View para debugar usuários"""
    
    if request.method == 'POST' and request.POST.get('secret') == 'debug_users_123':
        try:
            users = User.objects.all()
            
            html = "<h1>🔍 USUÁRIOS NO SISTEMA</h1>"
            html += f"<p><strong>Total de usuários:</strong> {users.count()}</p><hr>"
            
            for user in users:
                html += f"""
                <div style="border: 1px solid #ccc; padding: 10px; margin: 10px 0;">
                    <h3>👤 {user.nome_completo}</h3>
                    <p><strong>Username:</strong> {user.username}</p>
                    <p><strong>Email:</strong> {user.email}</p>
                    <p><strong>Tipo:</strong> {user.tipo_usuario}</p>
                    <p><strong>Ativo:</strong> {'✅ Sim' if user.ativo else '❌ Não'}</p>
                    <p><strong>Staff:</strong> {'✅ Sim' if user.is_staff else '❌ Não'}</p>
                    <p><strong>Superuser:</strong> {'✅ Sim' if user.is_superuser else '❌ Não'}</p>
                    <p><strong>Data criação:</strong> {user.data_criacao}</p>
                </div>
                """
            
            html += '<p><a href="/">🏠 Voltar ao Sistema</a></p>'
            return HttpResponse(html)
            
        except Exception as e:
            return HttpResponse(f"""
            <h1>❌ ERRO</h1>
            <p>Erro: {str(e)}</p>
            <p><a href="/">🏠 Voltar ao Sistema</a></p>
            """)
    
    return HttpResponse("""
    <h1>🔍 Debug de Usuários</h1>
    <form method="post">
        <label>Código Secreto:</label><br>
        <input type="password" name="secret" placeholder="Digite o código secreto"><br><br>
        <button type="submit">Ver Usuários</button>
    </form>
    <p><strong>Código:</strong> debug_users_123</p>
    """)

@csrf_exempt
def fix_user(request):
    """View para corrigir usuário específico"""
    
    if request.method == 'POST':
        secret = request.POST.get('secret')
        username = request.POST.get('username')
        new_password = request.POST.get('new_password', 'gestora123')
        
        if secret == 'fix_user_123' and username:
            try:
                user = User.objects.get(username=username)
                user.set_password(new_password)
                user.ativo = True
                user.is_active = True
                user.save()
                
                return HttpResponse(f"""
                <h1>✅ USUÁRIO CORRIGIDO!</h1>
                <p><strong>Username:</strong> {user.username}</p>
                <p><strong>Nova senha:</strong> {new_password}</p>
                <p><strong>Status:</strong> Ativo</p>
                <hr>
                <p><a href="/login/">🔗 Testar Login</a></p>
                <p><a href="/">🏠 Voltar ao Sistema</a></p>
                """)
                
            except User.DoesNotExist:
                return HttpResponse(f"""
                <h1>❌ USUÁRIO NÃO ENCONTRADO</h1>
                <p>Username '{username}' não existe</p>
                <p><a href="/">🏠 Voltar ao Sistema</a></p>
                """)
            except Exception as e:
                return HttpResponse(f"""
                <h1>❌ ERRO</h1>
                <p>Erro: {str(e)}</p>
                <p><a href="/">🏠 Voltar ao Sistema</a></p>
                """)
    
    return HttpResponse("""
    <h1>🔧 Corrigir Usuário</h1>
    <form method="post">
        <label>Código Secreto:</label><br>
        <input type="password" name="secret" placeholder="fix_user_123"><br><br>
        
        <label>Username:</label><br>
        <input type="text" name="username" placeholder="Digite o username"><br><br>
        
        <label>Nova Senha (opcional):</label><br>
        <input type="text" name="new_password" placeholder="Deixe vazio para 'gestora123'"><br><br>
        
        <button type="submit">Corrigir Usuário</button>
    </form>
    <p><strong>Código:</strong> fix_user_123</p>
    """)
