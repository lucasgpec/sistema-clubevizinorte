from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import datetime, timedelta
from .models import *
from .forms import UsuarioForm, LoginForm


def home(request):
    """Página inicial - redirecionamento baseado no status do usuário"""
    if request.user.is_authenticated:
        return redirect('club:dashboard')
    return render(request, 'club/home.html')


def login_view(request):
    """View de login"""
    if request.user.is_authenticated:
        return redirect('club:dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if user.ativo:
                    login(request, user)
                    messages.success(request, f'Bem-vindo, {user.nome_completo}!')
                    return redirect('club:dashboard')
                else:
                    messages.error(request, 'Usuário inativo. Contate o administrador.')
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = LoginForm()
    
    return render(request, 'club/login.html', {'form': form})


@login_required
def logout_view(request):
    """View de logout"""
    logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('club:home')


@login_required
def dashboard(request):
    """Dashboard principal do sistema"""
    user = request.user
    
    # Estatísticas básicas
    stats = {
        'total_socios': Socio.objects.filter(status='ATIVO').count(),
        'total_clientes': Cliente.objects.count(),
        'mensalidades_pendentes': Mensalidade.objects.filter(status='PENDENTE').count(),
        'locacoes_mes': Locacao.objects.filter(
            data_agendamento__month=datetime.now().month,
            data_agendamento__year=datetime.now().year
        ).count(),
    }
    
    # Configuração do clube
    config_clube = ConfiguracaoClube.objects.filter(ativa=True).first()
    
    context = {
        'stats': stats,
        'config_clube': config_clube,
        'user': user,
    }
    
    return render(request, 'club/dashboard.html', context)


@login_required
def usuarios_list(request):
    """Lista de usuários - apenas gestora pode acessar"""
    if request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado. Apenas gestoras podem gerenciar usuários.')
        return redirect('club:dashboard')
    
    usuarios = Usuario.objects.all().order_by('-data_criacao')
    
    return render(request, 'club/usuarios/list.html', {'usuarios': usuarios})


@login_required
def usuario_create(request):
    """Criar novo usuário - apenas gestora"""
    if request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:dashboard')
    
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.criado_por = request.user
            usuario.save()
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('club:usuarios_list')
    else:
        form = UsuarioForm()
    
    return render(request, 'club/usuarios/form.html', {'form': form, 'title': 'Novo Usuário'})


@login_required
def usuario_edit(request, pk):
    """Editar usuário - apenas gestora"""
    if request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:dashboard')
    
    usuario = get_object_or_404(Usuario, pk=pk)
    
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário atualizado com sucesso!')
            return redirect('club:usuarios_list')
    else:
        form = UsuarioForm(instance=usuario)
    
    return render(request, 'club/usuarios/form.html', {'form': form, 'title': 'Editar Usuário'})


@login_required
def usuario_toggle(request, pk):
    """Ativar/desativar usuário - apenas gestora"""
    if request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:dashboard')
    
    usuario = get_object_or_404(Usuario, pk=pk)
    usuario.ativo = not usuario.ativo
    usuario.save()
    
    status = 'ativado' if usuario.ativo else 'desativado'
    messages.success(request, f'Usuário {status} com sucesso!')
    
    return redirect('club:usuarios_list')


@login_required
def socios_list(request):
    """Lista de sócios"""
    if not request.user.pode_gerenciar_socios:
        messages.error(request, 'Acesso negado.')
        return redirect('club:dashboard')
    
    socios = Socio.objects.select_related('cliente').all().order_by('-id')
    
    return render(request, 'club/socios/list.html', {'socios': socios})


@login_required
def financeiro_dashboard(request):
    """Dashboard financeiro"""
    if not request.user.pode_gerenciar_financeiro:
        messages.error(request, 'Acesso negado.')
        return redirect('club:dashboard')
    
    # Estatísticas financeiras
    stats = {
        'mensalidades_pendentes': Mensalidade.objects.filter(status='PENDENTE').count(),
        'mensalidades_vencidas': Mensalidade.objects.filter(status='VENCIDO').count(),
        'valor_pendente': Mensalidade.objects.filter(status='PENDENTE').aggregate(
            total=Sum('valor_total')
        )['total'] or 0,
        'receita_mes': Mensalidade.objects.filter(
            status='PAGO',
            data_pagamento__month=datetime.now().month,
            data_pagamento__year=datetime.now().year
        ).aggregate(total=Sum('valor_pago'))['total'] or 0,
    }
    
    return render(request, 'club/financeiro/dashboard.html', {'stats': stats})


@login_required
def locacoes_list(request):
    """Lista de locações"""
    if not request.user.pode_gerenciar_locacoes:
        messages.error(request, 'Acesso negado.')
        return redirect('club:dashboard')
    
    locacoes = Locacao.objects.select_related('cliente', 'espaco').all().order_by('-data_agendamento')
    
    return render(request, 'club/locacoes/list.html', {'locacoes': locacoes})


@login_required
def escolas_list(request):
    """Lista de escolas de esporte"""
    if not request.user.pode_gerenciar_escolas:
        messages.error(request, 'Acesso negado.')
        return redirect('club:dashboard')
    
    escolas = EscolaEsporte.objects.all().order_by('nome')
    
    return render(request, 'club/escolas/list.html', {'escolas': escolas})


@login_required
def dayuse_list(request):
    """Lista de day uses"""
    if not request.user.pode_gerenciar_dayuse:
        messages.error(request, 'Acesso negado.')
        return redirect('club:dashboard')
    
    dayuses = DayUse.objects.select_related('cliente').all().order_by('-data_utilizacao')
    
    return render(request, 'club/dayuse/list.html', {'dayuses': dayuses})
