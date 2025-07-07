from django.contrib import admin
from django.utils.html import format_html
from datetime import date
from django import forms
from django.contrib import messages

from .models import (
    Usuario, ConfiguracaoClube, Cliente, Socio, Dependente, Espaco, Locacao,
    ContaBancaria, ConfiguracaoFinanceira, DayUse, Mensalidade,
    EscolaEsporte, MatriculaEscola, MensalidadeEscola, RepasseEscola,
    MensalidadeLocacao
)

# --- SISTEMA DE USUÁRIOS ---

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'nome_completo', 'tipo_usuario', 'ativo', 'data_criacao')
    list_filter = ('tipo_usuario', 'ativo', 'data_criacao')
    search_fields = ('username', 'nome_completo', 'cpf', 'email')
    readonly_fields = ('data_criacao', 'data_atualizacao', 'criado_por')
    
    fieldsets = (
        ('Informações de Login', {
            'fields': ('username', 'password', 'email')
        }),
        ('Dados Pessoais', {
            'fields': ('nome_completo', 'cpf', 'telefone')
        }),
        ('Tipo de Usuário', {
            'fields': ('tipo_usuario',)
        }),
        ('Permissões por Setor', {
            'fields': ('pode_gerenciar_socios', 'pode_gerenciar_financeiro', 
                      'pode_gerenciar_locacoes', 'pode_gerenciar_escolas', 
                      'pode_gerenciar_dayuse'),
            'classes': ('collapse',)
        }),
        ('Controle de Acesso', {
            'fields': ('ativo', 'criado_por', 'data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        readonly = list(self.readonly_fields)
        if obj:  # Editando usuário existente
            readonly.append('tipo_usuario')
        return readonly
    
    def save_model(self, request, obj, form, change):
        if not change:  # Criando novo usuário
            obj.criado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(ConfiguracaoClube)
class ConfiguracaoClubeAdmin(admin.ModelAdmin):
    list_display = ('nome_clube', 'ativa', 'data_atualizacao')
    list_filter = ('ativa',)
    readonly_fields = ('data_criacao', 'data_atualizacao')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome_clube', 'logo', 'descricao')
        }),
        ('Dados de Contato', {
            'fields': ('endereco', 'telefone', 'email', 'site')
        }),
        ('Cores do Sistema', {
            'fields': ('cor_primaria', 'cor_secundaria', 'cor_terciaria'),
            'description': 'Cores baseadas na identidade visual do clube'
        }),
        ('Status', {
            'fields': ('ativa', 'data_criacao', 'data_atualizacao')
        }),
    )
    
    def has_delete_permission(self, request, obj=None):
        # Previne a exclusão da configuração ativa
        if obj and obj.ativa:
            return False
        return super().has_delete_permission(request, obj)


# --- ADMINS PRINCIPAIS ---

def tornar_socio(modeladmin, request, queryset):
    from .models import Socio
    criados = 0
    ignorados = 0
    for cliente in queryset:
        if hasattr(cliente, 'socio') and cliente.socio is not None:
            ignorados += 1
            continue
        Socio.objects.create(cliente=cliente)
        criados += 1
    if criados:
        messages.success(request, f"{criados} cliente(s) agora são sócios (status pendente).")
    if ignorados:
        messages.warning(request, f"{ignorados} cliente(s) já eram sócios e foram ignorados.")

tornar_socio.short_description = "Tornar cliente(s) sócio(s) (status pendente)"

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'cpf', 'email', 'telefone', 'data_criacao')
    list_filter = ('data_criacao',)
    search_fields = ('nome_completo', 'cpf', 'email')
    readonly_fields = ('data_criacao', 'data_atualizacao')
    actions = [tornar_socio]
    fieldsets = (
        ('Dados Pessoais', {
            'fields': ('nome_completo', 'cpf', 'data_nascimento', 'email', 'telefone')
        }),
        ('Controle', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )


class DependenteInline(admin.TabularInline):
    model = Dependente
    extra = 1
    fields = ('nome_completo', 'data_nascimento', 'parentesco', 'cursando_ensino_superior', 'pcd')


class SocioAdminForm(forms.ModelForm):
    class Meta:
        model = Socio
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Só permite selecionar clientes que ainda não são sócios
        self.fields['cliente'].queryset = Cliente.objects.filter(socio__isnull=True)


@admin.register(Socio)
class SocioAdmin(admin.ModelAdmin):
    form = SocioAdminForm
    list_display = ('cliente', 'plano', 'status', 'convites_mensais', 'taxa_adesao_paga')
    list_filter = ('plano', 'status', 'taxa_adesao_paga')
    search_fields = ('cliente__nome_completo', 'cliente__cpf')
    inlines = [DependenteInline]
    fieldsets = (
        ('Informações do Sócio', {
            'fields': ('cliente', 'plano', 'status')
        }),
        ('Benefícios', {
            'fields': ('convites_mensais', 'taxa_adesao_paga')
        }),
    )


@admin.register(Dependente)
class DependenteAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'socio_titular', 'parentesco', 'data_nascimento', 'cursando_ensino_superior', 'pcd')
    list_filter = ('parentesco', 'cursando_ensino_superior', 'pcd')
    search_fields = ('nome_completo', 'socio_titular__cliente__nome_completo')
    fieldsets = (
        ('Dados do Dependente', {
            'fields': ('socio_titular', 'nome_completo', 'data_nascimento', 'parentesco')
        }),
        ('Situação Especial', {
            'fields': ('cursando_ensino_superior', 'pcd'),
            'description': 'Marque as opções conforme a situação do dependente'
        }),
    )


@admin.register(Espaco)
class EspacoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'capacidade', 'valor_locacao')
    search_fields = ('nome',)
    fieldsets = (
        ('Informações do Espaço', {
            'fields': ('nome', 'capacidade', 'valor_locacao')
        }),
    )


@admin.register(Locacao)
class LocacaoAdmin(admin.ModelAdmin):
    list_display = ('espaco', 'cliente', 'data_agendamento', 'status', 'data_criacao')
    list_filter = ('status', 'data_agendamento', 'espaco')
    search_fields = ('cliente__nome_completo', 'espaco__nome')
    readonly_fields = ('data_criacao', 'data_atualizacao')
    fieldsets = (
        ('Informações da Locação', {
            'fields': ('cliente', 'espaco', 'data_agendamento', 'status')
        }),
        ('Controle', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )


# --- SISTEMA FINANCEIRO ---

@admin.register(ContaBancaria)
class ContaBancariaAdmin(admin.ModelAdmin):
    list_display = ('banco', 'agencia', 'conta', 'digito', 'nome_titular', 'ativa')
    list_filter = ('ativa', 'banco')
    search_fields = ('banco', 'nome_titular', 'cpf_cnpj_titular')
    readonly_fields = ('data_criacao',)
    fieldsets = (
        ('Dados Bancários', {
            'fields': ('banco', 'agencia', 'conta', 'digito', 'nome_titular', 'cpf_cnpj_titular')
        }),
        ('Configurações de Boleto', {
            'fields': ('codigo_banco', 'convenio', 'carteira')
        }),
        ('Status', {
            'fields': ('ativa', 'data_criacao')
        }),
    )


@admin.register(ConfiguracaoFinanceira)
class ConfiguracaoFinanceiraAdmin(admin.ModelAdmin):
    list_display = ('data_atualizacao', 'valor_socio_individual', 'valor_socio_familia', 'dia_vencimento', 'ativa')
    list_filter = ('ativa',)
    readonly_fields = ('data_criacao', 'data_atualizacao')
    fieldsets = (
        ('Valores das Mensalidades', {
            'fields': ('valor_socio_individual', 'valor_socio_familia', 'valor_taxa_adesao', 'valor_day_use')
        }),
        ('Configurações de Cobrança', {
            'fields': ('dia_vencimento', 'dias_tolerancia', 'conta_padrao')
        }),
        ('Multas e Juros', {
            'fields': ('percentual_multa', 'percentual_juros_dia')
        }),
        ('Status', {
            'fields': ('ativa', 'data_criacao', 'data_atualizacao')
        }),
    )

    def has_delete_permission(self, request, obj=None):
        # Previne a exclusão da configuração ativa
        if obj and obj.ativa:
            return False
        return super().has_delete_permission(request, obj)


@admin.register(DayUse)
class DayUseAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'data_utilizacao', 'valor', 'pago', 'data_pagamento')
    list_filter = ('pago', 'data_utilizacao', 'forma_pagamento')
    search_fields = ('cliente__nome_completo', 'cliente__cpf')
    readonly_fields = ('data_criacao',)
    fieldsets = (
        ('Informações do Day Use', {
            'fields': ('cliente', 'data_utilizacao', 'valor')
        }),
        ('Pagamento', {
            'fields': ('pago', 'data_pagamento', 'forma_pagamento')
        }),
        ('Observações', {
            'fields': ('observacoes', 'data_criacao'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Mensalidade)
class MensalidadeAdmin(admin.ModelAdmin):
    list_display = ('socio', 'tipo', 'mes_referencia', 'valor_total', 'status', 'data_vencimento')
    list_filter = ('status', 'tipo', 'data_vencimento')
    search_fields = ('socio__cliente__nome_completo', 'socio__cliente__cpf')
    readonly_fields = ('valor_total', 'data_criacao', 'data_atualizacao')
    fieldsets = (
        ('Informações da Mensalidade', {
            'fields': ('socio', 'tipo', 'mes_referencia', 'data_vencimento')
        }),
        ('Valores', {
            'fields': ('valor_original', 'valor_multa', 'valor_juros', 'valor_total')
        }),
        ('Status e Pagamento', {
            'fields': ('status', 'data_pagamento', 'valor_pago', 'forma_pagamento')
        }),
        ('Dados do Boleto', {
            'fields': ('nosso_numero', 'linha_digitavel', 'codigo_barras'),
            'classes': ('collapse',)
        }),
        ('Observações', {
            'fields': ('observacoes', 'data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        readonly = list(self.readonly_fields)
        if obj and obj.status == 'PAGO':
            readonly.extend(['valor_original', 'valor_multa', 'valor_juros'])
        return readonly


# --- ESCOLAS DE ESPORTE ---

@admin.register(EscolaEsporte)
class EscolaEsporteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'responsavel', 'percentual_repasse', 'dia_repasse', 'ativa')
    list_filter = ('ativa', 'percentual_repasse')
    search_fields = ('nome', 'responsavel', 'cpf_cnpj')
    readonly_fields = ('data_criacao', 'data_atualizacao')
    fieldsets = (
        ('Informações da Escola', {
            'fields': ('nome', 'responsavel', 'cpf_cnpj', 'email', 'telefone')
        }),
        ('Configurações Financeiras', {
            'fields': ('percentual_repasse', 'dia_repasse')
        }),
        ('Dados Bancários', {
            'fields': ('banco_escola', 'agencia_escola', 'conta_escola'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('ativa', 'data_criacao', 'data_atualizacao')
        }),
    )


@admin.register(MatriculaEscola)
class MatriculaEscolaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'escola', 'valor_mensalidade', 'data_inicio', 'status')
    list_display = ('aluno', 'escola', 'valor_mensalidade', 'data_inicio', 'status')
    list_filter = ('status', 'escola', 'data_inicio')
    search_fields = ('aluno__nome_completo', 'escola__nome')
    readonly_fields = ('data_criacao', 'data_atualizacao')
    fieldsets = (
        ('Informações da Matrícula', {
            'fields': ('aluno', 'escola', 'valor_mensalidade', 'data_inicio', 'data_fim')
        }),
        ('Responsável Financeiro', {
            'fields': ('responsavel_financeiro',),
            'description': 'Informar apenas se o aluno for menor de idade'
        }),
        ('Status', {
            'fields': ('status', 'observacoes')
        }),
        ('Controle', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MensalidadeEscola)
class MensalidadeEscolaAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'mes_referencia', 'valor_total', 'status', 'data_vencimento')
    list_filter = ('status', 'matricula__escola', 'data_vencimento')
    search_fields = ('matricula__aluno__nome_completo', 'matricula__escola__nome')
    readonly_fields = ('valor_total', 'data_criacao', 'data_atualizacao')
    fieldsets = (
        ('Informações da Mensalidade', {
            'fields': ('matricula', 'mes_referencia', 'data_vencimento')
        }),
        ('Valores', {
            'fields': ('valor_original', 'valor_multa', 'valor_juros', 'valor_total')
        }),
        ('Status e Pagamento', {
            'fields': ('status', 'data_pagamento', 'valor_pago', 'forma_pagamento')
        }),
        ('Dados do Boleto', {
            'fields': ('nosso_numero', 'linha_digitavel', 'codigo_barras'),
            'classes': ('collapse',)
        }),
        ('Observações', {
            'fields': ('observacoes', 'data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )


@admin.register(RepasseEscola)
class RepasseEscolaAdmin(admin.ModelAdmin):
    list_display = ('escola', 'mes_referencia', 'valor_repasse', 'quantidade_alunos', 'status')
    list_filter = ('status', 'escola', 'mes_referencia')
    search_fields = ('escola__nome',)
    readonly_fields = ('data_criacao', 'data_atualizacao')
    fieldsets = (
        ('Informações do Repasse', {
            'fields': ('escola', 'mes_referencia', 'data_vencimento')
        }),
        ('Valores Calculados', {
            'fields': ('valor_total_arrecadado', 'valor_repasse', 'quantidade_alunos')
        }),
        ('Status e Pagamento', {
            'fields': ('status', 'data_pagamento', 'comprovante')
        }),
        ('Observações', {
            'fields': ('observacoes', 'data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MensalidadeLocacao)
class MensalidadeLocacaoAdmin(admin.ModelAdmin):
    list_display = ('locacao', 'valor_total', 'status', 'data_vencimento')
    list_filter = ('status', 'locacao__espaco', 'data_vencimento')
    search_fields = ('locacao__cliente__nome_completo', 'locacao__espaco__nome')
    readonly_fields = ('valor_total', 'data_criacao', 'data_atualizacao')
    fieldsets = (
        ('Informações da Cobrança', {
            'fields': ('locacao', 'data_vencimento')
        }),
        ('Valores', {
            'fields': ('valor_original', 'valor_multa', 'valor_juros', 'valor_total')
        }),
        ('Status e Pagamento', {
            'fields': ('status', 'data_pagamento', 'valor_pago', 'forma_pagamento')
        }),
        ('Dados do Boleto', {
            'fields': ('nosso_numero', 'linha_digitavel', 'codigo_barras'),
            'classes': ('collapse',)
        }),
        ('Observações', {
            'fields': ('observacoes', 'data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )


# --- CONFIGURAÇÕES ADICIONAIS ---

# Personalizações do admin
admin.site.site_header = "Sistema de Gestão do Clube"
admin.site.site_title = "Gestão do Clube"
admin.site.index_title = "Painel de Administração"