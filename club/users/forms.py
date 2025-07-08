from django import forms
from club.models import Socio, ClienteLead, ClienteDayUse, ClienteLocador, Cliente

class SocioForm(forms.ModelForm):
    class Meta:
        model = Socio
        fields = ['cliente', 'plano', 'status', 'convites_mensais', 'taxa_adesao_paga']

class ClienteLeadForm(forms.ModelForm):
    class Meta:
        model = ClienteLead
        fields = ['cliente', 'escola', 'modalidade', 'potencial_conversao']

class ClienteDayUseForm(forms.ModelForm):
    class Meta:
        model = ClienteDayUse
        fields = ['cliente', 'frequencia', 'preferencias', 'valor_gasto']

class ClienteLocadorForm(forms.ModelForm):
    class Meta:
        model = ClienteLocador
        fields = ['cliente', 'tipo_evento', 'espaco_preferido']
