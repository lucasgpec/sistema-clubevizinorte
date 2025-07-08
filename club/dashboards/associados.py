from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum, Q
from club.models import Socio, Mensalidade
from datetime import datetime, timedelta

class AssociadosDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'club/dashboards/associados_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # --- Cards principais ---
        socios_qs = Socio.objects.all()
        context['total_socios'] = socios_qs.count()
        context['socios_ativos'] = socios_qs.filter(status='ATIVO').count()
        context['socios_inativos'] = socios_qs.exclude(status='ATIVO').count()

        # --- Mensalidades ---
        mensalidades_qs = Mensalidade.objects.all()
        context['mensalidades_pagas'] = mensalidades_qs.filter(status='PAGO').count()
        context['mensalidades_pendentes'] = mensalidades_qs.filter(status='PENDENTE').count()

        # --- Gráfico de barras: mensalidades pagas/pendentes por mês ---
        meses = []
        pagas = []
        pendentes = []
        hoje = datetime.now()
        for i in range(5, -1, -1):
            ref = (hoje - timedelta(days=30*i)).replace(day=1)
            label = ref.strftime('%b/%Y')
            meses.append(label)
            pagas.append(mensalidades_qs.filter(status='PAGO', mes_referencia__month=ref.month, mes_referencia__year=ref.year).count())
            pendentes.append(mensalidades_qs.filter(status='PENDENTE', mes_referencia__month=ref.month, mes_referencia__year=ref.year).count())
        context['grafico_meses'] = meses
        context['grafico_pagas'] = pagas
        context['grafico_pendentes'] = pendentes

        # --- Gráfico de evolução mensal de associações ---
        evolucao = []
        for i in range(5, -1, -1):
            ref = (hoje - timedelta(days=30*i)).replace(day=1)
            evolucao.append(socios_qs.filter(cliente__data_criacao__month=ref.month, cliente__data_criacao__year=ref.year).count())
        context['grafico_evolucao'] = evolucao

        # --- Indicadores de inadimplência ---
        # Considera apenas mensalidades dos últimos 6 meses para o indicador
        meses_recentes = [(hoje - timedelta(days=30*i)).replace(day=1) for i in range(5, -1, -1)]
        filtro_meses = Q()
        for ref in meses_recentes:
            filtro_meses |= Q(mes_referencia__month=ref.month, mes_referencia__year=ref.year)
        total_periodo = mensalidades_qs.filter(filtro_meses).count() or 1
        inadimplencia = mensalidades_qs.filter(filtro_meses, status='PENDENTE').count() / total_periodo * 100
        context['inadimplencia'] = round(inadimplencia, 1)

        return context
