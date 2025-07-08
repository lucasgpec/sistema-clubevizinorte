from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Escola, AlunoEscola, Esporte, FinanceiroEscola

@login_required
def relatorio_alunos(request):
    if not request.user.pode_gerenciar_escolas and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return render(request, 'club/relatorios/erro.html')
    escolas = Escola.objects.all()
    esportes = Esporte.objects.all()
    status = request.GET.get('status')
    escola_id = request.GET.get('escola')
    esporte_id = request.GET.get('esporte')
    responsavel_id = request.GET.get('responsavel')
    alunos = AlunoEscola.objects.all()
    if status:
        alunos = alunos.filter(status=status)
    if escola_id:
        alunos = alunos.filter(escola_id=escola_id)
    if esporte_id:
        alunos = alunos.filter(horarios__esporte_id=esporte_id).distinct()
    if responsavel_id:
        alunos = alunos.filter(escola__responsavel_id=responsavel_id)
    return render(request, 'club/relatorios/alunos.html', {
        'alunos': alunos,
        'escolas': escolas,
        'esportes': esportes,
        'status_selected': status,
        'escola_selected': escola_id,
        'esporte_selected': esporte_id,
        'responsavel_selected': responsavel_id,
    })

@login_required
def relatorio_financeiro(request):
    if not request.user.pode_gerenciar_escolas and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return render(request, 'club/relatorios/erro.html')
    escolas = Escola.objects.all()
    esportes = Esporte.objects.all()
    escola_id = request.GET.get('escola')
    esporte_id = request.GET.get('esporte')
    pagamentos = FinanceiroEscola.objects.all()
    if escola_id:
        pagamentos = pagamentos.filter(escola_id=escola_id)
    if esporte_id:
        pagamentos = pagamentos.filter(esporte_id=esporte_id)
    return render(request, 'club/relatorios/financeiro.html', {
        'pagamentos': pagamentos,
        'escolas': escolas,
        'esportes': esportes,
        'escola_selected': escola_id,
        'esporte_selected': esporte_id,
    })
