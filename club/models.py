from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from decimal import Decimal
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

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