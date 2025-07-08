from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cobranca, AlunoEscola, ConfiguracaoIntegracaoFinanceira
from .finance_api_service import FinanceAPIService
from django.utils import timezone
from .forms import CobrancaForm
from django.db.models import Q

@login_required
def cobrancas_list(request):
    """Painel de cobranças: lista todas as cobranças do sistema"""
    cobrancas = Cobranca.objects.select_related('aluno').order_by('-data_emissao')
    return render(request, 'club/financeiro/cobrancas_list.html', {'cobrancas': cobrancas})

@login_required
def cobranca_detail(request, pk):
    cobranca = get_object_or_404(Cobranca, pk=pk)
    return render(request, 'club/financeiro/cobranca_detail.html', {'cobranca': cobranca})

@login_required
def cobranca_create(request):
    if request.method == 'POST':
        form = CobrancaForm(request.POST)
        if form.is_valid():
            cobranca = form.save(commit=False)
            cobranca.status = 'PENDENTE'
            cobranca.save()
            messages.success(request, 'Cobrança criada com sucesso!')
            return redirect('club:cobrancas_list')
    else:
        form = CobrancaForm()
    return render(request, 'club/financeiro/cobranca_form.html', {'form': form})

@login_required
def cobranca_emitir(request, pk):
    cobranca = get_object_or_404(Cobranca, pk=pk)
    config = ConfiguracaoIntegracaoFinanceira.objects.filter(ativo=True).first()
    if not config:
        messages.error(request, 'Configuração de integração financeira não encontrada.')
        return redirect('club:cobrancas_list')
    service = FinanceAPIService(config.__dict__)
    resultado = service.emitir_cobranca(
        aluno_id=cobranca.aluno.id,
        valor=float(cobranca.valor),
        vencimento=cobranca.vencimento,
        descricao=f'Cobrança para {cobranca.aluno.nome}'
    )
    cobranca.linha_digitavel = resultado.get('linha_digitavel', '')
    cobranca.nosso_numero = resultado.get('nosso_numero', '')
    cobranca.codigo_barras = resultado.get('codigo_barras', '')
    cobranca.retorno_banco = resultado.get('retorno_banco', '')
    cobranca.save()
    messages.success(request, 'Cobrança emitida com sucesso!')
    return redirect('club:cobranca_detail', pk=cobranca.pk)

@login_required
def configuracao_integracao(request):
    config = ConfiguracaoIntegracaoFinanceira.objects.first()
    if request.method == 'POST':
        # Simples: só um config ativo
        for field in ['banco', 'client_id', 'client_secret', 'webhook_url', 'ambiente', 'ativo']:
            setattr(config, field, request.POST.get(field, getattr(config, field)))
        config.save()
        messages.success(request, 'Configuração salva!')
        return redirect('club:configuracao_integracao')
    return render(request, 'club/financeiro/configuracao_integracao.html', {'config': config})

@login_required
def relatorio_cobrancas(request):
    cobrancas = Cobranca.objects.select_related('aluno').all()
    status = request.GET.get('status')
    aluno = request.GET.get('aluno')
    inicio = request.GET.get('inicio')
    fim = request.GET.get('fim')
    if status:
        cobrancas = cobrancas.filter(status=status)
    if aluno:
        cobrancas = cobrancas.filter(aluno__nome__icontains=aluno)
    if inicio:
        cobrancas = cobrancas.filter(vencimento__gte=inicio)
    if fim:
        cobrancas = cobrancas.filter(vencimento__lte=fim)
    return render(request, 'club/financeiro/relatorio_cobrancas.html', {'cobrancas': cobrancas})
