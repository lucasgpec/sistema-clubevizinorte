from django.http import HttpResponse
from django.contrib.auth import get_user_model

User = get_user_model()

def status_sistema(request):
    """Mostra o status do sistema"""
    
    try:
        users = User.objects.all()
        
        html = f"""
        <h1>🔍 STATUS DO SISTEMA</h1>
        <p><strong>Total de usuários:</strong> {users.count()}</p>
        <hr>
        """
        
        if users.count() == 0:
            html += """
            <h2 style="color: red;">❌ NENHUM USUÁRIO ENCONTRADO</h2>
            <p>O banco está vazio. Execute a migração para criar os usuários.</p>
            """
        else:
            html += "<h2>👥 USUÁRIOS ENCONTRADOS:</h2>"
            
            for user in users:
                html += f"""
                <div style="border: 1px solid #ccc; padding: 10px; margin: 10px 0; border-radius: 5px;">
                    <h3>👤 {user.nome_completo}</h3>
                    <p><strong>Username:</strong> {user.username}</p>
                    <p><strong>Email:</strong> {user.email}</p>
                    <p><strong>Tipo:</strong> {user.tipo_usuario}</p>
                    <p><strong>Ativo:</strong> {'✅ Sim' if user.ativo else '❌ Não'}</p>
                    <p><strong>Is_active:</strong> {'✅ Sim' if user.is_active else '❌ Não'}</p>
                    <p><strong>Staff:</strong> {'✅ Sim' if user.is_staff else '❌ Não'}</p>
                </div>
                """
        
        html += """
        <hr>
        <h3>🎯 CREDENCIAIS ESPERADAS:</h3>
        <div style="background: #f0f0f0; padding: 15px; border-radius: 5px;">
            <h4>ADMIN:</h4>
            <p>URL: <a href="/admin/">/admin/</a></p>
            <p>Username: clubeadmin</p>
            <p>Password: ClubVN2025!</p>
            
            <h4>GESTORA:</h4>
            <p>URL: <a href="/login/">/login/</a></p>
            <p>Username: gestora</p>
            <p>Password: gestora123</p>
        </div>
        
        <hr>
        <p><a href="/">🏠 Voltar ao Sistema</a></p>
        """
        
        return HttpResponse(html)
        
    except Exception as e:
        return HttpResponse(f"""
        <h1>❌ ERRO</h1>
        <p>Erro: {str(e)}</p>
        <p><a href="/">🏠 Voltar ao Sistema</a></p>
        """)
