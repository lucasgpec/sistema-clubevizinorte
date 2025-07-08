from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Esporte
from .forms import EsporteForm

@login_required
def esportes_list(request):
    if not request.user.pode_gerenciar_escolas and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:dashboard')
    esportes = Esporte.objects.all().order_by('nome')
    return render(request, 'club/escolas/esportes_list.html', {'esportes': esportes})

@login_required
def esporte_create(request):
    if not request.user.pode_gerenciar_escolas and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:esportes_list')
    if request.method == 'POST':
        form = EsporteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Esporte cadastrado com sucesso!')
            return redirect('club:esportes_list')
    else:
        form = EsporteForm()
    return render(request, 'club/escolas/esporte_form.html', {'form': form, 'title': 'Novo Esporte'})

@login_required
def esporte_edit(request, pk):
    if not request.user.pode_gerenciar_escolas and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:esportes_list')
    esporte = get_object_or_404(Esporte, pk=pk)
    if request.method == 'POST':
        form = EsporteForm(request.POST, instance=esporte)
        if form.is_valid():
            form.save()
            messages.success(request, 'Esporte atualizado com sucesso!')
            return redirect('club:esportes_list')
    else:
        form = EsporteForm(instance=esporte)
    return render(request, 'club/escolas/esporte_form.html', {'form': form, 'title': 'Editar Esporte'})

@login_required
def esporte_delete(request, pk):
    if not request.user.pode_gerenciar_escolas and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:esportes_list')
    esporte = get_object_or_404(Esporte, pk=pk)
    if request.method == 'POST':
        esporte.delete()
        messages.success(request, 'Esporte excluído com sucesso!')
        return redirect('club:esportes_list')
    return render(request, 'club/escolas/esporte_confirm_delete.html', {'esporte': esporte})
