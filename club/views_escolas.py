from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Escola
from .forms import EscolaForm

@login_required
def escolas_list(request):
    if not request.user.pode_gerenciar_escolas and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:dashboard')
    escolas = Escola.objects.all().order_by('nome')
    return render(request, 'club/escolas/list.html', {'escolas': escolas})

@login_required
def escola_create(request):
    if not request.user.pode_gerenciar_escolas and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:escolas_list')
    if request.method == 'POST':
        form = EscolaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Escola cadastrada com sucesso!')
            return redirect('club:escolas_list')
    else:
        form = EscolaForm()
    return render(request, 'club/escolas/escola_form.html', {'form': form, 'title': 'Nova Escola'})

@login_required
def escola_edit(request, pk):
    if not request.user.pode_gerenciar_escolas and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:escolas_list')
    escola = get_object_or_404(Escola, pk=pk)
    if request.method == 'POST':
        form = EscolaForm(request.POST, request.FILES, instance=escola)
        if form.is_valid():
            form.save()
            messages.success(request, 'Escola atualizada com sucesso!')
            return redirect('club:escolas_list')
    else:
        form = EscolaForm(instance=escola)
    return render(request, 'club/escolas/escola_form.html', {'form': form, 'title': 'Editar Escola'})

@login_required
def escola_delete(request, pk):
    if not request.user.pode_gerenciar_escolas and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:escolas_list')
    escola = get_object_or_404(Escola, pk=pk)
    if request.method == 'POST':
        escola.delete()
        messages.success(request, 'Escola excluída com sucesso!')
        return redirect('club:escolas_list')
    return render(request, 'club/escolas/escola_confirm_delete.html', {'escola': escola})
