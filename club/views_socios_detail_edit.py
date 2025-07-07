from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Socio
from .forms import SocioForm

@login_required
def socio_detail(request, pk):
    if not request.user.pode_gerenciar_socios and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:socios_list')
    socio = get_object_or_404(Socio, pk=pk)
    return render(request, 'club/socios/socio_detail.html', {'socio': socio})

@login_required
def socio_edit(request, pk):
    if not request.user.pode_gerenciar_socios and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:socios_list')
    socio = get_object_or_404(Socio, pk=pk)
    if request.method == 'POST':
        form = SocioForm(request.POST, instance=socio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sócio atualizado com sucesso!')
            return redirect('club:socios_list')
    else:
        form = SocioForm(instance=socio)
    return render(request, 'club/socios/socio_form.html', {'form': form, 'title': 'Editar Sócio', 'subtitle': 'Edite os dados do sócio'})

@login_required
def socio_delete(request, pk):
    if not request.user.pode_gerenciar_socios and request.user.tipo_usuario != 'GESTORA':
        messages.error(request, 'Acesso negado.')
        return redirect('club:socios_list')
    socio = get_object_or_404(Socio, pk=pk)
    if request.method == 'POST':
        socio.delete()
        messages.success(request, 'Sócio excluído com sucesso!')
        return redirect('club:socios_list')
    return render(request, 'club/socios/socio_confirm_delete.html', {'socio': socio})
