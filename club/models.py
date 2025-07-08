from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from decimal import Decimal
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

# — SISTEMA DE USUÁRIOS —

class Usuario(AbstractUser):
    """Sistema de usuários customizado para o clube"""
    
    TIPO_ADMINISTRADOR = 'ADMIN'
    TIPO_GESTORA = 'GESTORA'
    TIPO_FUNCIONARIO = 'FUNCIONARIO'
    TIPO_CHOICES = [
        (TIPO_ADMINISTRADOR, 'Administrador'),
        (TIPO_GESTORA, 'Gestora'),
        (TIPO_FUNCIONARIO, 'Funcionário'),
    ]
    
    tipo_usuario = models.CharField(
        max_length=11, 
        choices=TIPO_CHOICES, 
        default=TIPO_FUNCIONARIO
    )
    
    # Controle de setores para funcionários
    pode_gerenciar_socios = models.BooleanField(default=False)
    pode_gerenciar_financeiro = models.BooleanField(default=False)
    pode_gerenciar_locacoes = models.BooleanField(default=False)
    pode_gerenciar_escolas = models.BooleanField(default=False)
    pode_gerenciar_dayuse = models.BooleanField(default=False)
    
    # Dados pessoais
    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True, help_text="Formato: XXX.XXX.XXX-XX")
    telefone = models.CharField(max_length=20, blank=True)
    
    # Controle de acesso
    ativo = models.BooleanField(default=True)
    criado_por = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, blank=True,
        related_name='usuarios_criados'
    )
    
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nome_completo} ({self.get_tipo_usuario_display()})"
    
    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"


class ConfiguracaoClube(models.Model):
    """Configurações gerais do clube"""
    nome_clube = models.CharField(max_length=200, default="Clube Vizinho Norte")
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    descricao = models.TextField(blank=True)
    
    # Dados de contato
    endereco = models.CharField(max_length=255, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    site = models.URLField(blank=True)
    
    # Configurações de aparência
    cor_primaria = models.CharField(max_length=7, default="#231f1e", help_text="Cor primária (hex)")
    cor_secundaria = models.CharField(max_length=7, default="#304097", help_text="Cor secundária (hex)")
    cor_terciaria = models.CharField(max_length=7, default="#3a9ed2", help_text="Cor terciária (hex)")
    
    ativa = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Garante que só existe uma configuração ativa
        if self.ativa:
            ConfiguracaoClube.objects.filter(ativa=True).update(ativa=False)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nome_clube
    
    class Meta:
        verbose_name = "Configuração do Clube"
        verbose_name_plural = "Configurações do Clube"


# — MODELO CENTRAL —

class Cliente(models.Model):
    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True, help_text="Formato: XXX.XXX.XXX-XX")
    data_nascimento = models.DateField()
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome_completo} (CPF: {self.cpf})"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


# — MODELOS DO CLUBE —

class Socio(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, unique=True, null=True, blank=True)

    PLANO_INDIVIDUAL = "INDIVIDUAL"
    PLANO_FAMILIA = "FAMILIA"
    PLANO_CHOICES = [
        (PLANO_INDIVIDUAL, "Plano Individual - R$ 115,00"), 
        (PLANO_FAMILIA, "Plano Família - R$ 170,00")
    ]

    STATUS_ATIVO = "ATIVO"
    STATUS_INATIVO = "INATIVO"
    STATUS_PENDENTE = "PENDENTE"
    STATUS_CHOICES = [
        (STATUS_ATIVO, "Ativo"), 
        (STATUS_INATIVO, "Inativo"), 
        (STATUS_PENDENTE, "Pendente")
    ]

    plano = models.CharField(max_length=10, choices=PLANO_CHOICES, default=PLANO_INDIVIDUAL)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDENTE)
    convites_mensais = models.PositiveIntegerField(default=4, help_text="Convites não acumulativos")
    taxa_adesao_paga = models.BooleanField(default=False, help_text="Taxa de adesão de R$ 75,00")

    def __str__(self):
        return self.cliente.nome_completo

    class Meta:
        verbose_name = "Sócio"
        verbose_name_plural = "Sócios"


class Dependente(models.Model):
    socio_titular = models.ForeignKey(Socio, on_delete=models.CASCADE, related_name="dependentes")
    nome_completo = models.CharField(max_length=255)
    data_nascimento = models.DateField()


    PARENTESCO_CONJUGE = "CONJUGE"
    PARENTESCO_FILHO = "FILHO"
    PARENTESCO_CHOICES = [
        (PARENTESCO_CONJUGE, "Companheiro(a)"), 
        (PARENTESCO_FILHO, "Filho(a)")
    ]

    parentesco = models.CharField(max_length=10, choices=PARENTESCO_CHOICES)
    cursando_ensino_superior = models.BooleanField(
        default=False, 
        help_text="Marcar se for filho(a) entre 18 e 24 anos cursando ensino técnico ou superior"
    )
    pcd = models.BooleanField(
        default=False, 
        help_text="Marcar se for filho(a) PcD (sem limite de idade)"
    )

    def __str__(self):
        return f"{self.nome_completo} (Dependente de {self.socio_titular.cliente.nome_completo})"

    class Meta:
        verbose_name = "Dependente"
        verbose_name_plural = "Dependentes"


class Espaco(models.Model):
    nome = models.CharField(max_length=100)
    capacidade = models.PositiveIntegerField(default=0)
    valor_locacao = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)


    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Espaço"
        verbose_name_plural = "Espaços"


class Locacao(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    espaco = models.ForeignKey(Espaco, on_delete=models.PROTECT)
    data_agendamento = models.DateField()


    STATUS_AGENDADA = "AGENDADA"
    STATUS_REALIZADA = "REALIZADA"
    STATUS_CANCELADA = "CANCELADA"
    STATUS_CHOICES = [
        (STATUS_AGENDADA, "Agendada"),
        (STATUS_REALIZADA, "Realizada"),
        (STATUS_CANCELADA, "Cancelada")
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_AGENDADA)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.espaco.nome} locado por {self.cliente.nome_completo} em {self.data_agendamento.strftime('%d/%m/%Y')}"

    class Meta:
        verbose_name = "Locação"
        verbose_name_plural = "Locações"


# — SISTEMA FINANCEIRO —

class ContaBancaria(models.Model):
    """Contas bancárias do clube para geração de boletos"""
    banco = models.CharField(max_length=100)
    agencia = models.CharField(max_length=10)
    conta = models.CharField(max_length=20)
    digito = models.CharField(max_length=2)
    nome_titular = models.CharField(max_length=200)
    cpf_cnpj_titular = models.CharField(max_length=18)
    ativa = models.BooleanField(default=True)

    # Configurações para boletos
    codigo_banco = models.CharField(max_length=3, help_text="Código do banco para boletos")
    convenio = models.CharField(max_length=20, blank=True, null=True)
    carteira = models.CharField(max_length=10, blank=True, null=True)

    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.banco} - Ag: {self.agencia} - Conta: {self.conta}-{self.digito}"

    class Meta:
        verbose_name = "Conta Bancária"
        verbose_name_plural = "Contas Bancárias"


class ConfiguracaoFinanceira(models.Model):
    """Configurações gerais do sistema financeiro"""


    # Valores das mensalidades
    valor_socio_individual = models.DecimalField(
        max_digits=8, decimal_places=2, 
        default=Decimal("115.00"),
        help_text="Valor mensal do plano individual"
    )
    valor_socio_familia = models.DecimalField(
        max_digits=8, decimal_places=2, 
        default=Decimal("170.00"),
        help_text="Valor mensal do plano família"
    )
    valor_taxa_adesao = models.DecimalField(
        max_digits=8, decimal_places=2, 
        default=Decimal("75.00"),
        help_text="Taxa de adesão única"
    )
    valor_day_use = models.DecimalField(
        max_digits=8, decimal_places=2, 
        default=Decimal("50.00"),
        help_text="Valor do day use"
    )

    # Configurações de cobrança
    dia_vencimento = models.IntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(28)],
        help_text="Dia do mês para vencimento das mensalidades"
    )
    dias_tolerancia = models.IntegerField(
        default=5,
        help_text="Dias de tolerância após vencimento"
    )

    # Multas e juros
    percentual_multa = models.DecimalField(
        max_digits=5, decimal_places=2, 
        default=Decimal("2.00"),
        help_text="Percentual de multa por atraso"
    )
    percentual_juros_dia = models.DecimalField(
        max_digits=5, decimal_places=4, 
        default=Decimal("0.0333"),
        help_text="Percentual de juros ao dia (1% ao mês = 0.0333% ao dia)"
    )

    # Conta padrão para boletos
    conta_padrao = models.ForeignKey(
        ContaBancaria, 
        on_delete=models.SET_NULL, 
        null=True, blank=True,
        help_text="Conta bancária padrão para geração de boletos"
    )

    ativa = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Garante que só existe uma configuração ativa
        if self.ativa:
            ConfiguracaoFinanceira.objects.filter(ativa=True).update(ativa=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Configuração Financeira - {self.data_atualizacao.strftime('%d/%m/%Y')}"

    class Meta:
        verbose_name = "Configuração Financeira"
        verbose_name_plural = "Configurações Financeiras"


class DayUse(models.Model):
    """Controle de day use para clientes não sócios"""
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data_utilizacao = models.DateField()
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    pago = models.BooleanField(default=False)
    data_pagamento = models.DateField(null=True, blank=True)
    forma_pagamento = models.CharField(max_length=20, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Day Use - {self.cliente.nome_completo} ({self.data_utilizacao.strftime('%d/%m/%Y')})"

    class Meta:
        verbose_name = "Day Use"
        verbose_name_plural = "Day Uses"
        ordering = ["-data_utilizacao"]


class Mensalidade(models.Model):
    """Mensalidades dos sócios"""
    TIPO_MENSALIDADE = "MENSALIDADE"
    TIPO_TAXA_ADESAO = "TAXA_ADESAO"
    TIPO_CHOICES = [
        (TIPO_MENSALIDADE, "Mensalidade"),
        (TIPO_TAXA_ADESAO, "Taxa de Adesão"),
    ]


    STATUS_PENDENTE = "PENDENTE"
    STATUS_PAGO = "PAGO"
    STATUS_VENCIDO = "VENCIDO"
    STATUS_CANCELADO = "CANCELADO"
    STATUS_CHOICES = [
        (STATUS_PENDENTE, "Pendente"),
        (STATUS_PAGO, "Pago"),
        (STATUS_VENCIDO, "Vencido"),
        (STATUS_CANCELADO, "Cancelado"),
    ]

    socio = models.ForeignKey(Socio, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, default=TIPO_MENSALIDADE)
    mes_referencia = models.DateField(help_text="Primeiro dia do mês de referência")
    data_vencimento = models.DateField()
    valor_original = models.DecimalField(max_digits=8, decimal_places=2)
    valor_multa = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal("0.00"))
    valor_juros = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal("0.00"))
    valor_total = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDENTE)

    # Dados do pagamento
    data_pagamento = models.DateField(null=True, blank=True)
    valor_pago = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    forma_pagamento = models.CharField(max_length=20, blank=True, null=True)

    # Dados do boleto
    nosso_numero = models.CharField(max_length=20, blank=True, null=True)
    linha_digitavel = models.CharField(max_length=60, blank=True, null=True)
    codigo_barras = models.CharField(max_length=50, blank=True, null=True)

    observacoes = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def calcular_multa_juros(self):
        """Calcula multa e juros baseado na data atual"""
        if self.status == self.STATUS_PAGO:
            return
            
        config = ConfiguracaoFinanceira.objects.filter(ativa=True).first()
        if not config:
            return
            
        hoje = date.today()
        if hoje <= self.data_vencimento:
            return
            
        dias_atraso = (hoje - self.data_vencimento).days
        
        if dias_atraso > config.dias_tolerancia:
            # Calcula multa
            self.valor_multa = (self.valor_original * config.percentual_multa) / 100
            
            # Calcula juros
            self.valor_juros = (self.valor_original * config.percentual_juros_dia * dias_atraso) / 100
            
            # Atualiza valor total
            self.valor_total = self.valor_original + self.valor_multa + self.valor_juros
            
            # Atualiza status
            self.status = self.STATUS_VENCIDO

    def save(self, *args, **kwargs):
        self.calcular_multa_juros()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.socio.cliente.nome_completo} - {self.mes_referencia.strftime('%m/%Y')}"

    class Meta:
        verbose_name = "Mensalidade"
        verbose_name_plural = "Mensalidades"
        unique_together = ("socio", "mes_referencia", "tipo")
        ordering = ["-mes_referencia"]


class EscolaEsporte(models.Model):
    """Escolas de esporte parceiras - versão financeira"""
    nome = models.CharField(max_length=200)
    responsavel = models.CharField(max_length=200)
    cpf_cnpj = models.CharField(max_length=18, unique=True)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)


    # Dados financeiros
    percentual_repasse = models.DecimalField(
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentual que a escola repassa ao clube"
    )
    dia_repasse = models.IntegerField(
        default=10,
        validators=[MinValueValidator(1), MaxValueValidator(28)],
        help_text="Dia do mês para repasse"
    )

    # Dados bancários da escola
    banco_escola = models.CharField(max_length=100, blank=True, null=True)
    agencia_escola = models.CharField(max_length=10, blank=True, null=True)
    conta_escola = models.CharField(max_length=20, blank=True, null=True)

    ativa = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome} ({self.percentual_repasse}%)"

    class Meta:
        verbose_name = "Escola de Esporte"
        verbose_name_plural = "Escolas de Esporte"
        ordering = ["nome"]


class MatriculaEscola(models.Model):
    """Matrículas em escolas de esporte"""
    STATUS_ATIVA = 'ATIVA'
    STATUS_INATIVA = 'INATIVA'
    STATUS_SUSPENSA = 'SUSPENSA'
    STATUS_CHOICES = [
        (STATUS_ATIVA, 'Ativa'),
        (STATUS_INATIVA, 'Inativa'),
        (STATUS_SUSPENSA, 'Suspensa'),
    ]


    aluno = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    escola = models.ForeignKey(EscolaEsporte, on_delete=models.CASCADE)
    valor_mensalidade = models.DecimalField(max_digits=8, decimal_places=2)
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_ATIVA)

    # Dados do responsável financeiro (se menor de idade)
    responsavel_financeiro = models.ForeignKey(
        Cliente, 
        on_delete=models.SET_NULL, 
        null=True, blank=True,
        related_name="matriculas_responsavel"
    )

    observacoes = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.aluno.nome_completo} - {self.escola.nome}"

    class Meta:
        verbose_name = "Matrícula na Escola"
        verbose_name_plural = "Matrículas nas Escolas"
        unique_together = ("aluno", "escola")
        ordering = ["-data_inicio"]


class MensalidadeEscola(models.Model):
    """Mensalidades das escolas de esporte"""
    STATUS_PENDENTE = 'PENDENTE'
    STATUS_PAGO = 'PAGO'
    STATUS_VENCIDO = 'VENCIDO'
    STATUS_CANCELADO = 'CANCELADO'
    STATUS_CHOICES = [
        (STATUS_PENDENTE, 'Pendente'),
        (STATUS_PAGO, 'Pago'),
        (STATUS_VENCIDO, 'Vencido'),
        (STATUS_CANCELADO, 'Cancelado'),
    ]


    matricula = models.ForeignKey(MatriculaEscola, on_delete=models.CASCADE)
    mes_referencia = models.DateField()
    data_vencimento = models.DateField()
    valor_original = models.DecimalField(max_digits=8, decimal_places=2)
    valor_multa = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal("0.00"))
    valor_juros = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal("0.00"))
    valor_total = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDENTE)

    # Dados do pagamento
    data_pagamento = models.DateField(null=True, blank=True)
    valor_pago = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    forma_pagamento = models.CharField(max_length=20, blank=True, null=True)

    # Dados do boleto
    nosso_numero = models.CharField(max_length=20, blank=True, null=True)
    linha_digitavel = models.CharField(max_length=60, blank=True, null=True)
    codigo_barras = models.CharField(max_length=50, blank=True, null=True)

    observacoes = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def calcular_multa_juros(self):
        """Calcula multa e juros baseado na data atual"""
        if self.status == self.STATUS_PAGO:
            return
            
        config = ConfiguracaoFinanceira.objects.filter(ativa=True).first()
        if not config:
            return
            
        hoje = date.today()
        if hoje <= self.data_vencimento:
            return
            
        dias_atraso = (hoje - self.data_vencimento).days
        
        if dias_atraso > config.dias_tolerancia:
            self.valor_multa = (self.valor_original * config.percentual_multa) / 100
            self.valor_juros = (self.valor_original * config.percentual_juros_dia * dias_atraso) / 100
            self.valor_total = self.valor_original + self.valor_multa + self.valor_juros
            self.status = self.STATUS_VENCIDO

    def save(self, *args, **kwargs):
        self.calcular_multa_juros()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.matricula.aluno.nome_completo} - {self.matricula.escola.nome} ({self.mes_referencia.strftime('%m/%Y')})"

    class Meta:
        verbose_name = "Mensalidade da Escola"
        verbose_name_plural = "Mensalidades das Escolas"
        unique_together = ("matricula", "mes_referencia")
        ordering = ["-mes_referencia"]


class RepasseEscola(models.Model):
    """Repasses mensais das escolas para o clube"""
    STATUS_PENDENTE = 'PENDENTE'
    STATUS_PAGO = 'PAGO'
    STATUS_VENCIDO = 'VENCIDO'
    STATUS_CHOICES = [
        (STATUS_PENDENTE, 'Pendente'),
        (STATUS_PAGO, 'Pago'),
        (STATUS_VENCIDO, 'Vencido'),
    ]


    escola = models.ForeignKey(EscolaEsporte, on_delete=models.CASCADE)
    mes_referencia = models.DateField()
    data_vencimento = models.DateField()

    # Valores calculados
    valor_total_arrecadado = models.DecimalField(max_digits=10, decimal_places=2)
    valor_repasse = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_alunos = models.IntegerField()

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDENTE)
    data_pagamento = models.DateField(null=True, blank=True)
    comprovante = models.FileField(upload_to="comprovantes/repasses/", null=True, blank=True)

    observacoes = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Repasse {self.escola.nome} - {self.mes_referencia.strftime('%m/%Y')}"

    class Meta:
        verbose_name = "Repasse da Escola"
        verbose_name_plural = "Repasses das Escolas"
        unique_together = ("escola", "mes_referencia")
        ordering = ["-mes_referencia"]


class MensalidadeLocacao(models.Model):
    """Mensalidades das locações de espaços"""
    STATUS_PENDENTE = 'PENDENTE'
    STATUS_PAGO = 'PAGO'
    STATUS_VENCIDO = 'VENCIDO'
    STATUS_CANCELADO = 'CANCELADO'
    STATUS_CHOICES = [
        (STATUS_PENDENTE, 'Pendente'),
        (STATUS_PAGO, 'Pago'),
        (STATUS_VENCIDO, 'Vencido'),
        (STATUS_CANCELADO, 'Cancelado'),
    ]


    locacao = models.OneToOneField(Locacao, on_delete=models.CASCADE)
    data_vencimento = models.DateField()
    valor_original = models.DecimalField(max_digits=8, decimal_places=2)
    valor_multa = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal("0.00"))
    valor_juros = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal("0.00"))
    valor_total = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDENTE)

    # Dados do pagamento
    data_pagamento = models.DateField(null=True, blank=True)
    valor_pago = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    forma_pagamento = models.CharField(max_length=20, blank=True, null=True)

    # Dados do boleto
    nosso_numero = models.CharField(max_length=20, blank=True, null=True)
    linha_digitavel = models.CharField(max_length=60, blank=True, null=True)
    codigo_barras = models.CharField(max_length=50, blank=True, null=True)

    observacoes = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def calcular_multa_juros(self):
        """Calcula multa e juros baseado na data atual"""
        if self.status == self.STATUS_PAGO:
            return
            
        config = ConfiguracaoFinanceira.objects.filter(ativa=True).first()
        if not config:
            return
            
        hoje = date.today()
        if hoje <= self.data_vencimento:
            return
            
        dias_atraso = (hoje - self.data_vencimento).days
        
        if dias_atraso > config.dias_tolerancia:
            self.valor_multa = (self.valor_original * config.percentual_multa) / 100
            self.valor_juros = (self.valor_original * config.percentual_juros_dia * dias_atraso) / 100
            self.valor_total = self.valor_original + self.valor_multa + self.valor_juros
            self.status = self.STATUS_VENCIDO

    def save(self, *args, **kwargs):
        self.calcular_multa_juros()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Cobrança Locação - {self.locacao.cliente.nome_completo} ({self.locacao.espaco.nome})"

    class Meta:
        verbose_name = "Mensalidade de Locação"
        verbose_name_plural = "Mensalidades de Locações"
        ordering = ["-data_vencimento"]


class Esporte(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    tipo = models.CharField(max_length=50, blank=True)  # Adicionado campo tipo
    logo = models.ImageField(upload_to='esportes_logos/', blank=True, null=True)  # Adicionado campo logo
    def __str__(self):
        return self.nome
    class Meta:
        verbose_name = 'Esporte'
        verbose_name_plural = 'Esportes'


class Escola(models.Model):
    nome = models.CharField(max_length=255)
    tipo = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='escolas/logos/', null=True, blank=True)
    responsavel = models.ForeignKey('Usuario', on_delete=models.SET_NULL, null=True, blank=True, related_name='escolas_responsavel')
    def __str__(self):
        return self.nome
    class Meta:
        verbose_name = 'Escola'
        verbose_name_plural = 'Escolas'


class AlunoEscola(models.Model):
    nome = models.CharField(max_length=255)
    foto = models.ImageField(upload_to='alunos/fotos/', null=True, blank=True)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE, related_name='alunos')
    esportes = models.ManyToManyField(Esporte, through='HorarioEsporte', related_name='alunos')
    socio = models.ForeignKey('Socio', on_delete=models.SET_NULL, null=True, blank=True, related_name='alunos_escola')
    status = models.CharField(max_length=20, choices=[('ALUNO','Aluno'),('SOCIO','Sócio'),('ALUNO_SOCIO','Aluno/Sócio')], default='ALUNO')
    data_cadastro = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.nome
    class Meta:
        verbose_name = 'Aluno de Escola'
        verbose_name_plural = 'Alunos de Escola'


class HorarioEsporte(models.Model):
    aluno = models.ForeignKey(AlunoEscola, on_delete=models.CASCADE, related_name='horarios')
    esporte = models.ForeignKey(Esporte, on_delete=models.CASCADE, related_name='horarios')
    dia_semana = models.CharField(max_length=20)
    horario = models.TimeField()
    valor_mensalidade = models.DecimalField(max_digits=8, decimal_places=2)
    def __str__(self):
        return f"{self.aluno.nome} - {self.esporte.nome} ({self.dia_semana} {self.horario})"
    class Meta:
        verbose_name = 'Horário de Esporte'
        verbose_name_plural = 'Horários de Esporte'


class FinanceiroEscola(models.Model):
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE, related_name='financeiro')
    aluno = models.ForeignKey(AlunoEscola, on_delete=models.CASCADE, related_name='pagamentos')
    esporte = models.ForeignKey(Esporte, on_delete=models.CASCADE, related_name='pagamentos')
    valor_pago = models.DecimalField(max_digits=8, decimal_places=2)
    data_pagamento = models.DateField()
    observacao = models.TextField(blank=True)
    def __str__(self):
        return f"{self.aluno.nome} - {self.escola.nome} - {self.valor_pago}"
    class Meta:
        verbose_name = 'Financeiro da Escola'
        verbose_name_plural = 'Financeiro das Escolas'


# --- COBRANÇAS E INTEGRAÇÃO FINANCEIRA ---

class Cobranca(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('PAGO', 'Pago'),
        ('CANCELADO', 'Cancelado'),
        ('ERRO', 'Erro'),
    ]
    aluno = models.ForeignKey(AlunoEscola, on_delete=models.CASCADE, related_name='cobrancas')
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    vencimento = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    linha_digitavel = models.CharField(max_length=255, blank=True)
    nosso_numero = models.CharField(max_length=50, blank=True)
    codigo_barras = models.CharField(max_length=255, blank=True)
    data_emissao = models.DateTimeField(auto_now_add=True)
    data_baixa = models.DateTimeField(null=True, blank=True)
    observacao = models.TextField(blank=True)
    retorno_banco = models.TextField(blank=True)
    def __str__(self):
        return f"Cobranca {self.id} - {self.aluno.nome} - {self.valor} ({self.status})"
    class Meta:
        verbose_name = 'Cobrança'
        verbose_name_plural = 'Cobranças'

class ConfiguracaoIntegracaoFinanceira(models.Model):
    BANCO_CHOICES = [
        ('GERENCIANET', 'Gerencianet'),
        ('ASAAS', 'Asaas'),
        ('OUTRO', 'Outro'),
    ]
    banco = models.CharField(max_length=30, choices=BANCO_CHOICES, default='GERENCIANET')
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)
    webhook_url = models.URLField(blank=True)
    ambiente = models.CharField(max_length=20, choices=[('PRODUCAO','Produção'),('HOMOLOGACAO','Homologação')], default='HOMOLOGACAO')
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.get_banco_display()} ({'Ativo' if self.ativo else 'Inativo'})"
    class Meta:
        verbose_name = 'Configuração Integração Financeira'
        verbose_name_plural = 'Configurações Integração Financeira'


class CategoriaFinanceira(models.Model):
    """Categorias para lançamentos financeiros (ex: Mensalidade, Day-Use, Salário, Água, Luz, etc)"""
    TIPO_RECEITA = 'RECEITA'
    TIPO_DESPESA = 'DESPESA'
    TIPO_TRANSFERENCIA = 'TRANSFERENCIA'
    TIPO_CHOICES = [
        (TIPO_RECEITA, 'Receita'),
        (TIPO_DESPESA, 'Despesa'),
        (TIPO_TRANSFERENCIA, 'Transferência'),
    ]
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES)
    ativa = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"
    class Meta:
        verbose_name = "Categoria Financeira"
        verbose_name_plural = "Categorias Financeiras"


class LancamentoFinanceiro(models.Model):
    """Lançamentos financeiros: receitas, despesas, transferências"""
    categoria = models.ForeignKey(CategoriaFinanceira, on_delete=models.PROTECT)
    conta = models.ForeignKey(ContaBancaria, on_delete=models.PROTECT)
    usuario = models.ForeignKey('Usuario', on_delete=models.SET_NULL, null=True, blank=True)
    data = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.CharField(max_length=255, blank=True)
    conciliado = models.BooleanField(default=False)
    data_conciliacao = models.DateField(null=True, blank=True)
    observacoes = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.categoria} - R$ {self.valor} em {self.data.strftime('%d/%m/%Y')}"
    class Meta:
        verbose_name = "Lançamento Financeiro"
        verbose_name_plural = "Lançamentos Financeiros"
        ordering = ['-data', '-criado_em']


class ClienteLead(models.Model):
    """Cliente prospect (lead) matriculado em escola parceira"""
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, unique=True, null=True, blank=True)
    escola = models.ForeignKey('EscolaEsporte', on_delete=models.SET_NULL, null=True, blank=True)
    modalidade = models.CharField(max_length=100)
    potencial_conversao = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.cliente.nome_completo if self.cliente else 'Lead sem cliente'
    class Meta:
        verbose_name = "Cliente Lead"
        verbose_name_plural = "Clientes Lead"


class ClienteDayUse(models.Model):
    """Cliente de day-use"""
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, unique=True, null=True, blank=True)
    frequencia = models.PositiveIntegerField(default=0)
    preferencias = models.CharField(max_length=255, blank=True)
    valor_gasto = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    data_criacao = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.cliente.nome_completo if self.cliente else 'DayUse sem cliente'
    class Meta:
        verbose_name = "Cliente Day-Use"
        verbose_name_plural = "Clientes Day-Use"


class ClienteLocador(models.Model):
    """Cliente que aluga espaços do clube"""
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, unique=True, null=True, blank=True)
    tipo_evento = models.CharField(max_length=100)
    espaco_preferido = models.ForeignKey('Espaco', on_delete=models.SET_NULL, null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.cliente.nome_completo if self.cliente else 'Locador sem cliente'
    class Meta:
        verbose_name = "Cliente Locador"
        verbose_name_plural = "Clientes Locadores"