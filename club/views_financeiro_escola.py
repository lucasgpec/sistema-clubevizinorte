from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FinanceiroEscola, Escola, AlunoEscola, Esporte
from .forms import FinanceiroEscolaForm

@login_required
def financeiro_escola_list(request, escola_pk):
    if not request.user.pode_gerenciar_escolas and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:escolas_list')
    escola = get_object_or_404(Escola, pk=escola_pk)
    pagamentos = escola.financeiro.select_related('aluno', 'esporte').all().order_by('-data_pagamento')
    return render(request, 'club/escolas/financeiro_list.html', {'escola': escola, 'pagamentos': pagamentos})

@login_required
def financeiro_escola_create(request, escola_pk):
    if not request.user.pode_gerenciar_escolas and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:financeiro_escola_list', escola_pk=escola_pk)
    escola = get_object_or_404(Escola, pk=escola_pk)
    if request.method == 'POST':
        form = FinanceiroEscolaForm(request.POST)
        if form.is_valid():
            pagamento = form.save(commit=False)
            pagamento.escola = escola
            pagamento.save()
            messages.success(request, 'Pagamento registrado com sucesso!')
            return redirect('club:financeiro_escola_list', escola_pk=escola.pk)
    else:
        form = FinanceiroEscolaForm(initial={'escola': escola})
    return render(request, 'club/escolas/financeiro_form.html', {'form': form, 'escola': escola, 'title': 'Novo Pagamento'})

@login_required
def financeiro_escola_edit(request, escola_pk, pk):
    if not request.user.pode_gerenciar_escolas and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:financeiro_escola_list', escola_pk=escola_pk)
    escola = get_object_or_404(Escola, pk=escola_pk)
    pagamento = get_object_or_404(FinanceiroEscola, pk=pk, escola=escola)
    if request.method == 'POST':
        form = FinanceiroEscolaForm(request.POST, instance=pagamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pagamento atualizado com sucesso!')
            return redirect('club:financeiro_escola_list', escola_pk=escola.pk)
    else:
        form = FinanceiroEscolaForm(instance=pagamento)
    return render(request, 'club/escolas/financeiro_form.html', {'form': form, 'escola': escola, 'title': 'Editar Pagamento'})

@login_required
def financeiro_escola_delete(request, escola_pk, pk):
    if not request.user.pode_gerenciar_escolas and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:financeiro_escola_list', escola_pk=escola_pk)
    escola = get_object_or_404(Escola, pk=escola_pk)
    pagamento = get_object_or_404(FinanceiroEscola, pk=pk, escola=escola)
    if request.method == 'POST':
        pagamento.delete()
        messages.success(request, 'Pagamento excluído com sucesso!')
        return redirect('club:financeiro_escola_list', escola_pk=escola.pk)
    return render(request, 'club/escolas/financeiro_confirm_delete.html', {'pagamento': pagamento, 'escola': escola})
