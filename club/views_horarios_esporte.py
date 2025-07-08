from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import HorarioEsporte, AlunoEscola
from .forms import HorarioEsporteForm

@login_required
def horarios_aluno_list(request, aluno_pk):
    aluno = get_object_or_404(AlunoEscola, pk=aluno_pk)
    if not request.user.pode_gerenciar_escolas and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:alunos_escola_list', escola_pk=aluno.escola.pk)
    horarios = aluno.horarios.all().order_by('dia_semana', 'horario')
    return render(request, 'club/escolas/horarios_list.html', {'aluno': aluno, 'horarios': horarios})

@login_required
def horario_create(request, aluno_pk):
    aluno = get_object_or_404(AlunoEscola, pk=aluno_pk)
    if not request.user.pode_gerenciar_escolas and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:horarios_aluno_list', aluno_pk=aluno.pk)
    if request.method == 'POST':
        form = HorarioEsporteForm(request.POST)
        if form.is_valid():
            horario = form.save(commit=False)
            horario.aluno = aluno
            horario.save()
            messages.success(request, 'Horário cadastrado com sucesso!')
            return redirect('club:horarios_aluno_list', aluno_pk=aluno.pk)
    else:
        form = HorarioEsporteForm(initial={'aluno': aluno})
    return render(request, 'club/escolas/horario_form.html', {'form': form, 'aluno': aluno, 'title': 'Novo Horário'})

@login_required
def horario_edit(request, aluno_pk, pk):
    aluno = get_object_or_404(AlunoEscola, pk=aluno_pk)
    horario = get_object_or_404(HorarioEsporte, pk=pk, aluno=aluno)
    if not request.user.pode_gerenciar_escolas and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:horarios_aluno_list', aluno_pk=aluno.pk)
    if request.method == 'POST':
        form = HorarioEsporteForm(request.POST, instance=horario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Horário atualizado com sucesso!')
            return redirect('club:horarios_aluno_list', aluno_pk=aluno.pk)
    else:
        form = HorarioEsporteForm(instance=horario)
    return render(request, 'club/escolas/horario_form.html', {'form': form, 'aluno': aluno, 'title': 'Editar Horário'})

@login_required
def horario_delete(request, aluno_pk, pk):
    aluno = get_object_or_404(AlunoEscola, pk=aluno_pk)
    horario = get_object_or_404(HorarioEsporte, pk=pk, aluno=aluno)
    if not request.user.pode_gerenciar_escolas and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:horarios_aluno_list', aluno_pk=aluno.pk)
    if request.method == 'POST':
        horario.delete()
        messages.success(request, 'Horário excluído com sucesso!')
        return redirect('club:horarios_aluno_list', aluno_pk=aluno.pk)
    return render(request, 'club/escolas/horario_confirm_delete.html', {'horario': horario, 'aluno': aluno})
