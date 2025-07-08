from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from club.models import Socio, ClienteLead, ClienteDayUse, ClienteLocador
from .forms import SocioForm, ClienteLeadForm, ClienteDayUseForm, ClienteLocadorForm

# Sócios
class SocioListView(ListView):
    model = Socio
    template_name = 'club/users/socio_list.html'
    context_object_name = 'socios'

class SocioCreateView(CreateView):
    model = Socio
    form_class = SocioForm
    template_name = 'club/users/socio_form.html'
    success_url = reverse_lazy('club:socio_list')

class SocioUpdateView(UpdateView):
    model = Socio
    form_class = SocioForm
    template_name = 'club/users/socio_form.html'
    success_url = reverse_lazy('club:socio_list')

class SocioDeleteView(DeleteView):
    model = Socio
    template_name = 'club/users/socio_confirm_delete.html'
    success_url = reverse_lazy('club:socio_list')

# Leads
class ClienteLeadListView(ListView):
    model = ClienteLead
    template_name = 'club/users/lead_list.html'
    context_object_name = 'leads'

class ClienteLeadCreateView(CreateView):
    model = ClienteLead
    form_class = ClienteLeadForm
    template_name = 'club/users/lead_form.html'
    success_url = reverse_lazy('club:lead_list')

class ClienteLeadUpdateView(UpdateView):
    model = ClienteLead
    form_class = ClienteLeadForm
    template_name = 'club/users/lead_form.html'
    success_url = reverse_lazy('club:lead_list')

class ClienteLeadDeleteView(DeleteView):
    model = ClienteLead
    template_name = 'club/users/lead_confirm_delete.html'
    success_url = reverse_lazy('club:lead_list')

# Day-Use
class ClienteDayUseListView(ListView):
    model = ClienteDayUse
    template_name = 'club/users/dayuse_list.html'
    context_object_name = 'dayusers'

class ClienteDayUseCreateView(CreateView):
    model = ClienteDayUse
    form_class = ClienteDayUseForm
    template_name = 'club/users/dayuse_form.html'
    success_url = reverse_lazy('club:dayuse_list')

class ClienteDayUseUpdateView(UpdateView):
    model = ClienteDayUse
    form_class = ClienteDayUseForm
    template_name = 'club/users/dayuse_form.html'
    success_url = reverse_lazy('club:dayuse_list')

class ClienteDayUseDeleteView(DeleteView):
    model = ClienteDayUse
    template_name = 'club/users/dayuse_confirm_delete.html'
    success_url = reverse_lazy('club:dayuse_list')

# Locadores
class ClienteLocadorListView(ListView):
    model = ClienteLocador
    template_name = 'club/users/locador_list.html'
    context_object_name = 'locadores'

class ClienteLocadorCreateView(CreateView):
    model = ClienteLocador
    form_class = ClienteLocadorForm
    template_name = 'club/users/locador_form.html'
    success_url = reverse_lazy('club:locador_list')

class ClienteLocadorUpdateView(UpdateView):
    model = ClienteLocador
    form_class = ClienteLocadorForm
    template_name = 'club/users/locador_form.html'
    success_url = reverse_lazy('club:locador_list')

class ClienteLocadorDeleteView(DeleteView):
    model = ClienteLocador
    template_name = 'club/users/locador_confirm_delete.html'
    success_url = reverse_lazy('club:locador_list')
