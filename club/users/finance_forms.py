from django import forms
from club.models import CategoriaFinanceira, LancamentoFinanceiro

class CategoriaFinanceiraForm(forms.ModelForm):
    class Meta:
        model = CategoriaFinanceira
        fields = ['nome', 'tipo', 'ativa']

class LancamentoFinanceiroForm(forms.ModelForm):
    class Meta:
        model = LancamentoFinanceiro
        fields = [
            'categoria', 'conta', 'usuario', 'data', 'valor', 'descricao',
            'conciliado', 'data_conciliacao', 'observacoes'
        ]
