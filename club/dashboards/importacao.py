import csv
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from club.models import LancamentoFinanceiro, ContaBancaria, CategoriaFinanceira
from datetime import datetime
from decimal import Decimal

class ImportarExtratoView(LoginRequiredMixin, TemplateView):
    template_name = 'club/financeiro/importar_extrato.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('extrato')
        if not file:
            return render(request, self.template_name, {'erro': 'Selecione um arquivo.'})
        lancamentos = []
        decoded = file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded)
        for row in reader:
            data = datetime.strptime(row['Data'], '%d/%m/%Y').date()
            valor = Decimal(row['Valor'].replace(',', '.'))
            descricao = row.get('Descrição', '')
            categoria, _ = CategoriaFinanceira.objects.get_or_create(nome=row.get('Categoria', 'Importado'), tipo='DESPESA' if valor < 0 else 'RECEITA')
            conta = ContaBancaria.objects.first()
            lancamentos.append(LancamentoFinanceiro(
                categoria=categoria,
                conta=conta,
                usuario=request.user,
                data=data,
                valor=abs(valor),
                descricao=descricao,
                conciliado=False
            ))
        LancamentoFinanceiro.objects.bulk_create(lancamentos)
        return render(request, self.template_name, {'sucesso': f'{len(lancamentos)} lançamentos importados com sucesso!'})
