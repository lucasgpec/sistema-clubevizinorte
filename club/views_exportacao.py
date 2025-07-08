import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import AlunoEscola, FinanceiroEscola

@login_required
def exportar_alunos_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="alunos.csv"'
    writer = csv.writer(response)
    writer.writerow(['Nome', 'Escola', 'Status', 'Esportes'])
    for aluno in AlunoEscola.objects.all():
        esportes = ', '.join([h.esporte.nome for h in aluno.horarios.all()])
        writer.writerow([aluno.nome, aluno.escola.nome, aluno.get_status_display(), esportes])
    return response

@login_required
def exportar_financeiro_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="financeiro.csv"'
    writer = csv.writer(response)
    writer.writerow(['Escola', 'Aluno', 'Esporte', 'Valor Pago', 'Data Pagamento', 'Observação'])
    for pag in FinanceiroEscola.objects.select_related('escola', 'aluno', 'esporte').all():
        writer.writerow([
            pag.escola.nome,
            pag.aluno.nome,
            pag.esporte.nome,
            pag.valor_pago,
            pag.data_pagamento,
            pag.observacao
        ])
    return response
