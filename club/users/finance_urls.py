from django.urls import path
from . import finance_views

urlpatterns = [
    # Categorias Financeiras
    path('categorias/', finance_views.CategoriaFinanceiraListView.as_view(), name='categoriafinanceira_list'),
    path('categorias/nova/', finance_views.CategoriaFinanceiraCreateView.as_view(), name='categoriafinanceira_create'),
    path('categorias/<int:pk>/editar/', finance_views.CategoriaFinanceiraUpdateView.as_view(), name='categoriafinanceira_update'),
    path('categorias/<int:pk>/excluir/', finance_views.CategoriaFinanceiraDeleteView.as_view(), name='categoriafinanceira_delete'),

    # Lançamentos Financeiros
    path('lancamentos/', finance_views.LancamentoFinanceiroListView.as_view(), name='lancamentofinanceiro_list'),
    path('lancamentos/novo/', finance_views.LancamentoFinanceiroCreateView.as_view(), name='lancamentofinanceiro_create'),
    path('lancamentos/<int:pk>/editar/', finance_views.LancamentoFinanceiroUpdateView.as_view(), name='lancamentofinanceiro_update'),
    path('lancamentos/<int:pk>/excluir/', finance_views.LancamentoFinanceiroDeleteView.as_view(), name='lancamentofinanceiro_delete'),
]
