from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import datetime, timedelta
from .models import *
from .forms import (
    UsuarioForm, LoginForm, ClienteForm, SocioForm, 
    EspacoForm, LocacaoForm, EscolaEsporteForm, DayUseForm
)
from .views_socios_detail_edit import socio_detail, socio_edit, socio_delete


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
    
    context = {
        'stats': stats,
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
    if not request.user.pode_gerenciar_socios and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:dashboard')
    
    socios = Socio.objects.select_related('cliente').all().order_by('-id')
    
    return render(request, 'club/socios/list.html', {'socios': socios})


@login_required
def cliente_create(request):
    """Criar novo cliente"""
    if not request.user.pode_gerenciar_socios and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:dashboard')
    
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'Cliente "{cliente.nome_completo}" criado com sucesso!')
            return redirect('club:socios_list')
    else:
        form = ClienteForm()
    
    return render(request, 'club/socios/cliente_form.html', {
        'form': form, 
        'title': 'Novo Cliente',
        'subtitle': 'Cadastre um novo cliente no sistema'
    })


@login_required
def socio_create(request):
    """Criar novo sócio"""
    if not request.user.pode_gerenciar_socios and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:dashboard')
    
    if request.method == 'POST':
        form = SocioForm(request.POST)
        if form.is_valid():
            socio = form.save()
            messages.success(request, f'Sócio "{socio.cliente.nome_completo}" criado com sucesso!')
            return redirect('club:socios_list')
    else:
        form = SocioForm()
    
    return render(request, 'club/socios/socio_form.html', {
        'form': form, 
        'title': 'Novo Sócio',
        'subtitle': 'Transforme um cliente em sócio'
    })


@login_required
def financeiro_dashboard(request):
    """Dashboard financeiro"""
    if not request.user.pode_gerenciar_financeiro and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:dashboard')
    
    # Estatísticas financeiras com tratamento de erro
    try:
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
    except:
        # Se houver erro nas consultas, usar valores padrão
        stats = {
            'mensalidades_pendentes': 0,
            'mensalidades_vencidas': 0,
            'valor_pendente': 0,
            'receita_mes': 0,
        }
    
    return render(request, 'club/financeiro/dashboard.html', {'stats': stats})


@login_required
def locacoes_list(request):
    """Lista de locações"""
    if not request.user.pode_gerenciar_locacoes and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:dashboard')
    
    locacoes = Locacao.objects.select_related('cliente', 'espaco').all().order_by('-data_agendamento')
    
    return render(request, 'club/locacoes/list.html', {'locacoes': locacoes})


@login_required
def locacao_create(request):
    """Criar nova locação"""
    if not request.user.pode_gerenciar_locacoes and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:dashboard')
    
    if request.method == 'POST':
        form = LocacaoForm(request.POST)
        if form.is_valid():
            locacao = form.save()
            messages.success(request, f'Locação criada com sucesso para {locacao.data_agendamento.strftime("%d/%m/%Y")}!')
            return redirect('club:locacoes_list')
    else:
        form = LocacaoForm()
    
    return render(request, 'club/locacoes/form.html', {
        'form': form, 
        'title': 'Nova Locação',
        'subtitle': 'Reserve um espaço do clube'
    })


@login_required
def espaco_create(request):
    """Criar novo espaço"""
    if not request.user.pode_gerenciar_locacoes and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:dashboard')
    
    if request.method == 'POST':
        form = EspacoForm(request.POST)
        if form.is_valid():
            espaco = form.save()
            messages.success(request, f'Espaço "{espaco.nome}" criado com sucesso!')
            return redirect('club:locacoes_list')
    else:
        form = EspacoForm()
    
    return render(request, 'club/locacoes/espaco_form.html', {
        'form': form, 
        'title': 'Novo Espaço',
        'subtitle': 'Cadastre um novo espaço para locação'
    })


@login_required
def escolas_list(request):
    """Lista de escolas de esporte"""
    if not request.user.pode_gerenciar_escolas and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:dashboard')
    
    escolas = EscolaEsporte.objects.all().order_by('nome')
    
    return render(request, 'club/escolas/list.html', {'escolas': escolas})


@login_required
def escola_create(request):
    """Criar nova escola de esporte"""
    if not request.user.pode_gerenciar_escolas and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:dashboard')
    
    if request.method == 'POST':
        form = EscolaEsporteForm(request.POST)
        if form.is_valid():
            escola = form.save()
            messages.success(request, f'Escola "{escola.nome}" criada com sucesso!')
            return redirect('club:escolas_list')
    else:
        form = EscolaEsporteForm()
    
    return render(request, 'club/escolas/form.html', {
        'form': form, 
        'title': 'Nova Escola de Esporte',
        'subtitle': 'Cadastre uma nova escola parceira'
    })


@login_required
def dayuse_list(request):
    """Lista de day uses"""
    if not request.user.pode_gerenciar_dayuse and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:dashboard')
    
    dayuses = DayUse.objects.select_related('cliente').all().order_by('-data_utilizacao')
    
    return render(request, 'club/dayuse/list.html', {'dayuses': dayuses})


@login_required
def dayuse_create(request):
    """Criar novo day use"""
    if not request.user.pode_gerenciar_dayuse and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:dashboard')
    
    if request.method == 'POST':
        form = DayUseForm(request.POST)
        if form.is_valid():
            dayuse = form.save()
            messages.success(request, f'Day Use criado com sucesso para {dayuse.cliente.nome_completo}!')
            return redirect('club:dayuse_list')
    else:
        form = DayUseForm()
        # Define valor padrão do day use
        config = ConfiguracaoFinanceira.objects.filter(ativa=True).first()
        if config:
            form.initial['valor'] = config.valor_day_use
    
    return render(request, 'club/dayuse/form.html', {
        'form': form, 
        'title': 'Novo Day Use',
        'subtitle': 'Registre um visitante de day use'
    })


@login_required
def cliente_detail(request, pk):
    """Detalhes do cliente"""
    if not request.user.pode_gerenciar_socios and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:socios_list')
    
    cliente = get_object_or_404(Cliente, pk=pk)
    
    return render(request, 'club/socios/cliente_detail.html', {'cliente': cliente})


@login_required
def cliente_edit(request, pk):
    """Editar cliente"""
    if not request.user.pode_gerenciar_socios and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:socios_list')
    
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente atualizado com sucesso!')
            return redirect('club:socios_list')
    else:
        form = ClienteForm(instance=cliente)
    
    return render(request, 'club/socios/cliente_form.html', {
        'form': form, 
        'title': 'Editar Cliente',
        'subtitle': 'Edite os dados do cliente'
    })


@login_required
def cliente_delete(request, pk):
    """Excluir cliente"""
    if not request.user.pode_gerenciar_socios and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:socios_list')
    
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente excluído com sucesso!')
        return redirect('club:socios_list')
    
    return render(request, 'club/socios/cliente_confirm_delete.html', {'cliente': cliente})
