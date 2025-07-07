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
        fields = ['cliente', 'espaco', 'data_agendamento', 'status']
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
        fields = ['cliente', 'data_utilizacao', 'valor', 'pago', 'data_pagamento', 'forma_pagamento', 'observacoes']
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
