from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ConfiguracaoClube

@csrf_exempt
def test_media(request):
    """View para testar configurações de media"""
    
    try:
        config = ConfiguracaoClube.objects.filter(ativa=True).first()
        
        if not config:
            return HttpResponse("❌ Nenhuma configuração encontrada")
        
        html = f"""
        <h1>🔍 TESTE DE ARQUIVOS DE MEDIA</h1>
        
        <h2>Configuração Encontrada:</h2>
        <p><strong>Nome:</strong> {config.nome_clube}</p>
        <p><strong>Logo:</strong> {config.logo}</p>
        
        <h2>URLs de Media:</h2>
        <p><strong>MEDIA_URL:</strong> /media/</p>
        <p><strong>Logo URL:</strong> {config.logo.url if config.logo else 'Nenhuma logo'}</p>
        
        <h2>Teste da Logo:</h2>
        """
        
        if config.logo:
            html += f"""
            <p>Tentando carregar logo:</p>
            <img src="{config.logo.url}" alt="Logo" style="max-height: 100px; border: 1px solid #ccc;">
            <br><br>
            <p>Se a imagem não aparecer, há problema na configuração de media.</p>
            """
        else:
            html += "<p>❌ Nenhuma logo configurada</p>"
        
        html += '<p><a href="/">🏠 Voltar ao Sistema</a></p>'
        
        return HttpResponse(html)
        
    except Exception as e:
        return HttpResponse(f"""
        <h1>❌ ERRO</h1>
        <p>Erro: {str(e)}</p>
        <p><a href="/">🏠 Voltar ao Sistema</a></p>
        """)
