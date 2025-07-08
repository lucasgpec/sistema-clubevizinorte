from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


class LoginForm(forms.Form):
    """Formulário de login"""
    username = forms.CharField(
        label='Usuário',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu usuário'
        })
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha'
        })
    )


class UsuarioForm(UserCreationForm):
    """Formulário para criar/editar usuários"""
    
    class Meta:
        model = Usuario
        fields = [
            'username', 'nome_completo', 'cpf', 'email', 'telefone',
            'tipo_usuario', 'pode_gerenciar_socios', 'pode_gerenciar_financeiro',
            'pode_gerenciar_locacoes', 'pode_gerenciar_escolas', 'pode_gerenciar_dayuse'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'nome_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XXX.XXX.XXX-XX'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_usuario': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Estilização dos campos de permissão
        permission_fields = [
            'pode_gerenciar_socios', 'pode_gerenciar_financeiro',
            'pode_gerenciar_locacoes', 'pode_gerenciar_escolas', 'pode_gerenciar_dayuse'
        ]
        
        for field in permission_fields:
            self.fields[field].widget.attrs.update({'class': 'form-check-input'})
        
        # Estilização dos campos de senha
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        
        # Labels personalizados
        self.fields['password1'].label = 'Senha'
        self.fields['password2'].label = 'Confirmação de senha'
        
        # Ajustando campos baseado no tipo de usuário
        if self.instance and self.instance.pk:
            if self.instance.tipo_usuario == 'GESTORA':
                # Gestora tem todas as permissões
                for field in permission_fields:
                    self.fields[field].initial = True
                    self.fields[field].widget.attrs['disabled'] = True


class ClienteForm(forms.ModelForm):
    """Formulário para clientes"""
    
    class Meta:
        model = Cliente
        fields = ['nome_completo', 'cpf', 'data_nascimento', 'email', 'telefone']
        widgets = {
            'nome_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XXX.XXX.XXX-XX'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(XX) XXXXX-XXXX'}),
        }


class SocioForm(forms.ModelForm):
    """Formulário para sócios"""
    
    class Meta:
        model = Socio
        fields = ['cliente', 'plano', 'status', 'convites_mensais', 'taxa_adesao_paga']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'plano': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'convites_mensais': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'taxa_adesao_paga': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Só permite selecionar clientes que ainda não são sócios
        self.fields['cliente'].queryset = Cliente.objects.filter(socio__isnull=True)


class EspacoForm(forms.ModelForm):
    """Formulário para espaços"""
    
    class Meta:
        model = Espaco
        fields = ['nome', 'capacidade', 'valor_locacao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'capacidade': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'valor_locacao': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }


class LocacaoForm(forms.ModelForm):
    """Formulário para locações"""
    
    class Meta:
        model = Locacao
        fields = ['cliente', 'espaco', 'data_agendamento', 'status'
        ]
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'espaco': forms.Select(attrs={'class': 'form-control'}),
            'data_agendamento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class EscolaEsporteForm(forms.ModelForm):
    """Formulário para escolas de esporte"""
    
    class Meta:
        model = EscolaEsporte
        fields = [
            'nome', 'responsavel', 'cpf_cnpj', 'email', 'telefone',
            'percentual_repasse', 'dia_repasse', 
            'banco_escola', 'agencia_escola', 'conta_escola', 'ativa'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'responsavel': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf_cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XXX.XXX.XXX-XX ou XX.XXX.XXX/XXXX-XX'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'percentual_repasse': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'dia_repasse': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '28'}),
            'banco_escola': forms.TextInput(attrs={'class': 'form-control'}),
            'agencia_escola': forms.TextInput(attrs={'class': 'form-control'}),
            'conta_escola': forms.TextInput(attrs={'class': 'form-control'}),
            'ativa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class DayUseForm(forms.ModelForm):
    """Formulário para day use"""
    
    class Meta:
        model = DayUse
        fields = ['cliente', 'data_utilizacao', 'valor', 'pago', 'data_pagamento', 'forma_pagamento', 'observacoes'
        ]
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'data_utilizacao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'pago': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'data_pagamento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'forma_pagamento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Dinheiro, PIX, Cartão'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Campos condicionais
        self.fields['data_pagamento'].required = False
        self.fields['forma_pagamento'].required = False
        self.fields['observacoes'].required = False


class EsporteForm(forms.ModelForm):
    """Formulário para esportes"""
    
    class Meta:
        model = Esporte
        fields = ['nome', 'descricao', 'logo', 'tipo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control'}),
        }


class EscolaForm(forms.ModelForm):
    """Formulário para escolas"""
    
    class Meta:
        model = Escola
        fields = ['nome', 'tipo', 'logo', 'responsavel']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'responsavel': forms.Select(attrs={'class': 'form-control'}),
        }


class AlunoEscolaForm(forms.ModelForm):
    """Formulário para alunos de escola"""
    
    class Meta:
        model = AlunoEscola
        fields = ['nome', 'foto', 'escola', 'socio', 'status']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'escola': forms.Select(attrs={'class': 'form-control'}),
            'socio': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class HorarioEsporteForm(forms.ModelForm):
    """Formulário para horários de esporte"""
    
    class Meta:
        model = HorarioEsporte
        fields = ['aluno', 'esporte', 'dia_semana', 'horario', 'valor_mensalidade']
        widgets = {
            'aluno': forms.Select(attrs={'class': 'form-control'}),
            'esporte': forms.Select(attrs={'class': 'form-control'}),
            'dia_semana': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Segunda-feira'}),
            'horario': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'valor_mensalidade': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }


class FinanceiroEscolaForm(forms.ModelForm):
    """Formulário para financeiro de escola"""
    
    class Meta:
        model = FinanceiroEscola
        fields = ['escola', 'aluno', 'esporte', 'valor_pago', 'data_pagamento', 'observacao']
        widgets = {
            'escola': forms.Select(attrs={'class': 'form-control'}),
            'aluno': forms.Select(attrs={'class': 'form-control'}),
            'esporte': forms.Select(attrs={'class': 'form-control'}),
            'valor_pago': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'data_pagamento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class CobrancaForm(forms.ModelForm):
    """Formulário para criação e edição de cobranças"""
    
    class Meta:
        model = Cobranca
        fields = ['aluno', 'valor', 'vencimento', 'observacao']
        widgets = {
            'aluno': forms.Select(attrs={'class': 'form-select'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'vencimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
