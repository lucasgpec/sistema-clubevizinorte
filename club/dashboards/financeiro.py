from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from club.models import LancamentoFinanceiro, CategoriaFinanceira
from datetime import datetime, timedelta

class FinanceiroDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'club/financeiro/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hoje = datetime.now().date()
        inicio_mes = hoje.replace(day=1)
        # Totais do mês
        receitas = LancamentoFinanceiro.objects.filter(
            categoria__tipo='RECEITA', data__gte=inicio_mes, data__lte=hoje
        ).aggregate(total=Sum('valor'))['total'] or 0
        despesas = LancamentoFinanceiro.objects.filter(
            categoria__tipo='DESPESA', data__gte=inicio_mes, data__lte=hoje
        ).aggregate(total=Sum('valor'))['total'] or 0
        saldo = receitas - despesas
        context['receitas'] = receitas
        context['despesas'] = despesas
        context['saldo'] = saldo
        # Gráfico de receitas/despesas dos últimos 6 meses
        meses = []
        receitas_meses = []
        despesas_meses = []
        for i in range(5, -1, -1):
            ref = (hoje - timedelta(days=30*i)).replace(day=1)
            label = ref.strftime('%b/%Y')
            meses.append(label)
            receitas_meses.append(LancamentoFinanceiro.objects.filter(
                categoria__tipo='RECEITA', data__month=ref.month, data__year=ref.year
            ).aggregate(total=Sum('valor'))['total'] or 0)
            despesas_meses.append(LancamentoFinanceiro.objects.filter(
                categoria__tipo='DESPESA', data__month=ref.month, data__year=ref.year
            ).aggregate(total=Sum('valor'))['total'] or 0)
        context['grafico_meses'] = meses
        context['grafico_receitas'] = receitas_meses
        context['grafico_despesas'] = despesas_meses
        return context
