from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from club.models import LancamentoFinanceiro
from datetime import date, timedelta
from django.shortcuts import redirect

class ConciliacaoBancariaView(LoginRequiredMixin, TemplateView):
    template_name = 'club/financeiro/conciliacao.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hoje = date.today()
        inicio = hoje - timedelta(days=30)
        # Lançamentos não conciliados dos últimos 30 dias
        context['lancamentos'] = LancamentoFinanceiro.objects.filter(
            conciliado=False, data__gte=inicio
        ).order_by('data')
        return context

    def post(self, request, *args, **kwargs):
        lancamento_id = request.POST.get('lancamento_id')
        if lancamento_id:
            LancamentoFinanceiro.objects.filter(id=lancamento_id).update(conciliado=True)
        return redirect('conciliacao_bancaria')
