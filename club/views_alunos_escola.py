from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AlunoEscola, Escola
from .forms import AlunoEscolaForm

@login_required
def alunos_escola_list(request, escola_pk):
    if not request.user.pode_gerenciar_escolas and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:escolas_list')
    escola = get_object_or_404(Escola, pk=escola_pk)
    alunos = escola.alunos.all().order_by('nome')
    return render(request, 'club/escolas/alunos_list.html', {'escola': escola, 'alunos': alunos})

@login_required
def aluno_escola_create(request, escola_pk):
    if not request.user.pode_gerenciar_escolas and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:escolas_list')
    escola = get_object_or_404(Escola, pk=escola_pk)
    if request.method == 'POST':
        form = AlunoEscolaForm(request.POST, request.FILES)
        if form.is_valid():
            aluno = form.save(commit=False)
            aluno.escola = escola
            aluno.save()
            messages.success(request, 'Aluno cadastrado com sucesso!')
            return redirect('club:alunos_escola_list', escola_pk=escola.pk)
    else:
        form = AlunoEscolaForm(initial={'escola': escola})
    return render(request, 'club/escolas/aluno_form.html', {'form': form, 'escola': escola, 'title': 'Novo Aluno'})

@login_required
def aluno_escola_edit(request, escola_pk, pk):
    if not request.user.pode_gerenciar_escolas and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:escolas_list')
    escola = get_object_or_404(Escola, pk=escola_pk)
    aluno = get_object_or_404(AlunoEscola, pk=pk, escola=escola)
    if request.method == 'POST':
        form = AlunoEscolaForm(request.POST, request.FILES, instance=aluno)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aluno atualizado com sucesso!')
            return redirect('club:alunos_escola_list', escola_pk=escola.pk)
    else:
        form = AlunoEscolaForm(instance=aluno)
    return render(request, 'club/escolas/aluno_form.html', {'form': form, 'escola': escola, 'title': 'Editar Aluno'})

@login_required
def aluno_escola_delete(request, escola_pk, pk):
    if not request.user.pode_gerenciar_escolas and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:escolas_list')
    escola = get_object_or_404(Escola, pk=escola_pk)
    aluno = get_object_or_404(AlunoEscola, pk=pk, escola=escola)
    if request.method == 'POST':
        aluno.delete()
        messages.success(request, 'Aluno excluído com sucesso!')
        return redirect('club:alunos_escola_list', escola_pk=escola.pk)
    return render(request, 'club/escolas/aluno_confirm_delete.html', {'aluno': aluno, 'escola': escola})
