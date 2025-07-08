from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum
from club.models import EscolaEsporte, AlunoEscola, MensalidadeEscola, Esporte

class EscolasDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'club/dashboards/escolas_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Clientes ativos/inativos por escola
        escolas = EscolaEsporte.objects.all()
        escolas_data = []
        for escola in escolas:
            total = AlunoEscola.objects.filter(escola=escola).count()
            ativos = AlunoEscola.objects.filter(escola=escola, status='ALUNO').count()
            inativos = total - ativos
            pagas = MensalidadeEscola.objects.filter(matricula__escola=escola, status='PAGO').count()
            pendentes = MensalidadeEscola.objects.filter(matricula__escola=escola, status='PENDENTE').count()
            faturamento = MensalidadeEscola.objects.filter(matricula__escola=escola, status='PAGO').aggregate(total=Sum('valor_pago'))['total'] or 0
            escolas_data.append({
                'nome': escola.nome,
                'total': total,
                'ativos': ativos,
                'inativos': inativos,
                'pagas': pagas,
                'pendentes': pendentes,
                'faturamento': float(faturamento),
            })
        context['escolas_data'] = escolas_data
        # Ranking de escolas por faturamento
        ranking = sorted(escolas_data, key=lambda x: x['faturamento'], reverse=True)
        context['ranking'] = ranking[:5]
        # Gráfico de distribuição de modalidades
        modalidades = Esporte.objects.values('nome').annotate(qtd=Count('alunos'))
        context['modalidades_labels'] = [m['nome'] for m in modalidades]
        context['modalidades_data'] = [m['qtd'] for m in modalidades]
        return context
