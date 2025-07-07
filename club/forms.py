from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario


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
