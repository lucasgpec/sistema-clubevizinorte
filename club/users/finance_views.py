from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from club.models import CategoriaFinanceira, LancamentoFinanceiro
from .finance_forms import CategoriaFinanceiraForm, LancamentoFinanceiroForm

# Categorias Financeiras
class CategoriaFinanceiraListView(ListView):
    model = CategoriaFinanceira
    template_name = 'club/financeiro/categoriafinanceira_list.html'
    context_object_name = 'categorias'

class CategoriaFinanceiraCreateView(CreateView):
    model = CategoriaFinanceira
    form_class = CategoriaFinanceiraForm
    template_name = 'club/financeiro/categoriafinanceira_form.html'
    success_url = reverse_lazy('club:categoriafinanceira_list')

class CategoriaFinanceiraUpdateView(UpdateView):
    model = CategoriaFinanceira
    form_class = CategoriaFinanceiraForm
    template_name = 'club/financeiro/categoriafinanceira_form.html'
    success_url = reverse_lazy('club:categoriafinanceira_list')

class CategoriaFinanceiraDeleteView(DeleteView):
    model = CategoriaFinanceira
    template_name = 'club/financeiro/categoriafinanceira_confirm_delete.html'
    success_url = reverse_lazy('club:categoriafinanceira_list')

# Lançamentos Financeiros
class LancamentoFinanceiroListView(ListView):
    model = LancamentoFinanceiro
    template_name = 'club/financeiro/lancamentofinanceiro_list.html'
    context_object_name = 'lancamentos'

class LancamentoFinanceiroCreateView(CreateView):
    model = LancamentoFinanceiro
    form_class = LancamentoFinanceiroForm
    template_name = 'club/financeiro/lancamentofinanceiro_form.html'
    success_url = reverse_lazy('club:lancamentofinanceiro_list')

class LancamentoFinanceiroUpdateView(UpdateView):
    model = LancamentoFinanceiro
    form_class = LancamentoFinanceiroForm
    template_name = 'club/financeiro/lancamentofinanceiro_form.html'
    success_url = reverse_lazy('club:lancamentofinanceiro_list')

class LancamentoFinanceiroDeleteView(DeleteView):
    model = LancamentoFinanceiro
    template_name = 'club/financeiro/lancamentofinanceiro_confirm_delete.html'
    success_url = reverse_lazy('club:lancamentofinanceiro_list')
