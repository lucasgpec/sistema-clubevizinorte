from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum
from club.models import DayUse
from datetime import datetime, timedelta

class DayUseDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'club/dashboards/dayuse_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hoje = datetime.now()
        # Utilização diária/mensal (últimos 6 meses)
        meses = []
        uso_mensal = []
        receita_mensal = []
        for i in range(5, -1, -1):
            ref = (hoje - timedelta(days=30*i)).replace(day=1)
            label = ref.strftime('%b/%Y')
            meses.append(label)
            uso = DayUse.objects.filter(data_utilizacao__month=ref.month, data_utilizacao__year=ref.year).count()
            receita = DayUse.objects.filter(data_utilizacao__month=ref.month, data_utilizacao__year=ref.year, pago=True).aggregate(s=Sum('valor'))['s'] or 0
            uso_mensal.append(uso)
            receita_mensal.append(float(receita))
        context['meses'] = meses
        context['uso_mensal'] = uso_mensal
        context['receita_mensal'] = receita_mensal
        # Picos de utilização (dias com maior uso no mês atual)
        dias = DayUse.objects.filter(data_utilizacao__month=hoje.month, data_utilizacao__year=hoje.year).values('data_utilizacao').annotate(qtd=Count('id')).order_by('-qtd')[:7]
        context['picos'] = [{'dia': d['data_utilizacao'].strftime('%d/%m'), 'qtd': d['qtd']} for d in dias]
        # Clientes recorrentes
        recorrentes = DayUse.objects.values('cliente__nome_completo').annotate(freq=Count('id')).filter(freq__gte=2).order_by('-freq')[:5]
        context['recorrentes'] = recorrentes
        return context
