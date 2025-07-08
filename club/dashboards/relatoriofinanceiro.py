from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from club.models import LancamentoFinanceiro, CategoriaFinanceira
from datetime import datetime, timedelta
from django.http import HttpResponse
import csv

class RelatorioFinanceiroView(LoginRequiredMixin, TemplateView):
    template_name = 'club/financeiro/relatorio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filtros
        mes = self.request.GET.get('mes')
        ano = self.request.GET.get('ano')
        qs = LancamentoFinanceiro.objects.all()
        if mes and ano:
            qs = qs.filter(data__month=mes, data__year=ano)
        context['lancamentos'] = qs.order_by('-data')
        context['mes'] = mes
        context['ano'] = ano
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.GET.get('export') == 'csv':
            return self.export_csv(context['lancamentos'])
        return super().render_to_response(context, **response_kwargs)

    def export_csv(self, lancamentos):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="relatorio_financeiro.csv"'
        writer = csv.writer(response)
        writer.writerow(['Data', 'Categoria', 'Conta', 'Valor', 'Tipo', 'Conciliado', 'Descrição'])
        for l in lancamentos:
            writer.writerow([
                l.data.strftime('%d/%m/%Y'), l.categoria.nome, l.conta, l.valor,
                l.categoria.get_tipo_display(), 'Sim' if l.conciliado else 'Não', l.descricao
            ])
        return response
