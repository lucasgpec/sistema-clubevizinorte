from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum
from club.models import Locacao, Espaco
from datetime import datetime, timedelta

class LocacoesDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'club/dashboards/locacoes_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Locações mensais por espaço (últimos 6 meses)
        hoje = datetime.now()
        meses = []
        locacoes_por_espaco = {}
        espacos = Espaco.objects.all()
        for espaco in espacos:
            locacoes_por_espaco[espaco.nome] = []
        for i in range(5, -1, -1):
            ref = (hoje - timedelta(days=30*i)).replace(day=1)
            label = ref.strftime('%b/%Y')
            meses.append(label)
            for espaco in espacos:
                count = Locacao.objects.filter(espaco=espaco, data_agendamento__month=ref.month, data_agendamento__year=ref.year).count()
                locacoes_por_espaco[espaco.nome].append(count)
        context['meses'] = meses
        context['locacoes_por_espaco'] = locacoes_por_espaco
        # Receita de locações (gráfico temporal)
        receita = []
        for i in range(5, -1, -1):
            ref = (hoje - timedelta(days=30*i)).replace(day=1)
            total = Locacao.objects.filter(data_agendamento__month=ref.month, data_agendamento__year=ref.year).aggregate(s=Sum('espaco__valor_locacao'))['s'] or 0
            receita.append(float(total))
        context['receita'] = receita
        # Ocupação dos espaços (calendário visual simplificado)
        ocupacao = {}
        for espaco in espacos:
            dias = Locacao.objects.filter(espaco=espaco, data_agendamento__month=hoje.month, data_agendamento__year=hoje.year).values_list('data_agendamento', flat=True)
            ocupacao[espaco.nome] = [d.strftime('%Y-%m-%d') for d in dias]
        context['ocupacao'] = ocupacao
        # Tipos de eventos mais frequentes (campo tipo_evento pode ser adicionado no futuro)
        # context['tipos_evento'] = ...
        return context
