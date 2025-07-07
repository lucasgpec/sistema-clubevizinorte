from .models import ConfiguracaoClube

def club_settings(request):
    """Context processor para disponibilizar configurações do clube em todos os templates"""
    try:
        config_clube = ConfiguracaoClube.objects.filter(ativa=True).first()
        if not config_clube:
            # Se não houver configuração, criar uma padrão
            config_clube = ConfiguracaoClube.objects.create(
                nome_clube='Clube Vizinho Norte',
                cor_primaria='#231f1e',
                cor_secundaria='#304097',
                cor_terciaria='#3a9ed2',
                ativa=True
            )
    except:
        # Em caso de erro, usar valores padrão
        config_clube = type('obj', (object,), {
            'nome_clube': 'Clube Vizinho Norte',
            'logo': None,
            'cor_primaria': '#231f1e',
            'cor_secundaria': '#304097',
            'cor_terciaria': '#3a9ed2',
        })()
    
    return {
        'config_clube': config_clube
    }
