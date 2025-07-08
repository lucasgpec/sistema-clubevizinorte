from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Cobranca
from django.utils import timezone
import json

@csrf_exempt
@require_POST
def webhook_bancario(request):
    """
    Endpoint para receber notificações de pagamento do banco/fintech.
    Atualiza status e data de baixa da cobrança automaticamente.
    """
    try:
        data = json.loads(request.body.decode('utf-8'))
        nosso_numero = data.get('nosso_numero')
        status = data.get('status')
        # Exemplo: status pode ser 'PAGO', 'CANCELADO', etc.
        cobranca = Cobranca.objects.filter(nosso_numero=nosso_numero).first()
        if not cobranca:
            return JsonResponse({'error': 'Cobrança não encontrada.'}, status=404)
        if status == 'PAGO':
            cobranca.status = 'PAGO'
            cobranca.data_baixa = timezone.now()
        elif status == 'CANCELADO':
            cobranca.status = 'CANCELADO'
        elif status == 'ERRO':
            cobranca.status = 'ERRO'
        cobranca.retorno_banco = json.dumps(data)
        cobranca.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
