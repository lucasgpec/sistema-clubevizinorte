# Generated by Django 5.2.4 on 2025-07-07 18:06

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_completo', models.CharField(max_length=255)),
                ('cpf', models.CharField(help_text='Formato: XXX.XXX.XXX-XX', max_length=14, unique=True)),
                ('data_nascimento', models.DateField()),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('telefone', models.CharField(max_length=20)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
        migrations.CreateModel(
            name='ConfiguracaoClube',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_clube', models.CharField(default='Clube Vizinho Norte', max_length=200)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logos/')),
                ('descricao', models.TextField(blank=True)),
                ('endereco', models.CharField(blank=True, max_length=255)),
                ('telefone', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('site', models.URLField(blank=True)),
                ('cor_primaria', models.CharField(default='#231f1e', help_text='Cor primária (hex)', max_length=7)),
                ('cor_secundaria', models.CharField(default='#304097', help_text='Cor secundária (hex)', max_length=7)),
                ('cor_terciaria', models.CharField(default='#3a9ed2', help_text='Cor terciária (hex)', max_length=7)),
                ('ativa', models.BooleanField(default=True)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Configuração do Clube',
                'verbose_name_plural': 'Configurações do Clube',
            },
        ),
        migrations.CreateModel(
            name='ContaBancaria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banco', models.CharField(max_length=100)),
                ('agencia', models.CharField(max_length=10)),
                ('conta', models.CharField(max_length=20)),
                ('digito', models.CharField(max_length=2)),
                ('nome_titular', models.CharField(max_length=200)),
                ('cpf_cnpj_titular', models.CharField(max_length=18)),
                ('ativa', models.BooleanField(default=True)),
                ('codigo_banco', models.CharField(help_text='Código do banco para boletos', max_length=3)),
                ('convenio', models.CharField(blank=True, max_length=20, null=True)),
                ('carteira', models.CharField(blank=True, max_length=10, null=True)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Conta Bancária',
                'verbose_name_plural': 'Contas Bancárias',
            },
        ),
        migrations.CreateModel(
            name='EscolaEsporte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('responsavel', models.CharField(max_length=200)),
                ('cpf_cnpj', models.CharField(max_length=18, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('telefone', models.CharField(max_length=20)),
                ('percentual_repasse', models.DecimalField(decimal_places=2, help_text='Percentual que a escola repassa ao clube', max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('dia_repasse', models.IntegerField(default=10, help_text='Dia do mês para repasse', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(28)])),
                ('banco_escola', models.CharField(blank=True, max_length=100, null=True)),
                ('agencia_escola', models.CharField(blank=True, max_length=10, null=True)),
                ('conta_escola', models.CharField(blank=True, max_length=20, null=True)),
                ('ativa', models.BooleanField(default=True)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Escola de Esporte',
                'verbose_name_plural': 'Escolas de Esporte',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Espaco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('capacidade', models.PositiveIntegerField(default=0)),
                ('valor_locacao', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
            ],
            options={
                'verbose_name': 'Espaço',
                'verbose_name_plural': 'Espaços',
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('tipo_usuario', models.CharField(choices=[('ADMIN', 'Administrador'), ('GESTORA', 'Gestora'), ('FUNCIONARIO', 'Funcionário')], default='FUNCIONARIO', max_length=11)),
                ('pode_gerenciar_socios', models.BooleanField(default=False)),
                ('pode_gerenciar_financeiro', models.BooleanField(default=False)),
                ('pode_gerenciar_locacoes', models.BooleanField(default=False)),
                ('pode_gerenciar_escolas', models.BooleanField(default=False)),
                ('pode_gerenciar_dayuse', models.BooleanField(default=False)),
                ('nome_completo', models.CharField(max_length=255)),
                ('cpf', models.CharField(help_text='Formato: XXX.XXX.XXX-XX', max_length=14, unique=True)),
                ('telefone', models.CharField(blank=True, max_length=20)),
                ('ativo', models.BooleanField(default=True)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('criado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='usuarios_criados', to=settings.AUTH_USER_MODEL)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Usuário',
                'verbose_name_plural': 'Usuários',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ConfiguracaoFinanceira',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_socio_individual', models.DecimalField(decimal_places=2, default=Decimal('115.00'), help_text='Valor mensal do plano individual', max_digits=8)),
                ('valor_socio_familia', models.DecimalField(decimal_places=2, default=Decimal('170.00'), help_text='Valor mensal do plano família', max_digits=8)),
                ('valor_taxa_adesao', models.DecimalField(decimal_places=2, default=Decimal('75.00'), help_text='Taxa de adesão única', max_digits=8)),
                ('valor_day_use', models.DecimalField(decimal_places=2, default=Decimal('50.00'), help_text='Valor do day use', max_digits=8)),
                ('dia_vencimento', models.IntegerField(default=10, help_text='Dia do mês para vencimento das mensalidades', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(28)])),
                ('dias_tolerancia', models.IntegerField(default=5, help_text='Dias de tolerância após vencimento')),
                ('percentual_multa', models.DecimalField(decimal_places=2, default=Decimal('2.00'), help_text='Percentual de multa por atraso', max_digits=5)),
                ('percentual_juros_dia', models.DecimalField(decimal_places=4, default=Decimal('0.0333'), help_text='Percentual de juros ao dia (1% ao mês = 0.0333% ao dia)', max_digits=5)),
                ('ativa', models.BooleanField(default=True)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('conta_padrao', models.ForeignKey(blank=True, help_text='Conta bancária padrão para geração de boletos', null=True, on_delete=django.db.models.deletion.SET_NULL, to='club.contabancaria')),
            ],
            options={
                'verbose_name': 'Configuração Financeira',
                'verbose_name_plural': 'Configurações Financeiras',
            },
        ),
        migrations.CreateModel(
            name='DayUse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_utilizacao', models.DateField()),
                ('valor', models.DecimalField(decimal_places=2, max_digits=8)),
                ('pago', models.BooleanField(default=False)),
                ('data_pagamento', models.DateField(blank=True, null=True)),
                ('forma_pagamento', models.CharField(blank=True, max_length=20, null=True)),
                ('observacoes', models.TextField(blank=True, null=True)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='club.cliente')),
            ],
            options={
                'verbose_name': 'Day Use',
                'verbose_name_plural': 'Day Uses',
                'ordering': ['-data_utilizacao'],
            },
        ),
        migrations.CreateModel(
            name='Locacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_agendamento', models.DateField()),
                ('status', models.CharField(choices=[('AGENDADA', 'Agendada'), ('REALIZADA', 'Realizada'), ('CANCELADA', 'Cancelada')], default='AGENDADA', max_length=10)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='club.cliente')),
                ('espaco', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='club.espaco')),
            ],
            options={
                'verbose_name': 'Locação',
                'verbose_name_plural': 'Locações',
            },
        ),
        migrations.CreateModel(
            name='MatriculaEscola',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_mensalidade', models.DecimalField(decimal_places=2, max_digits=8)),
                ('data_inicio', models.DateField()),
                ('data_fim', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('ATIVA', 'Ativa'), ('INATIVA', 'Inativa'), ('SUSPENSA', 'Suspensa')], default='ATIVA', max_length=10)),
                ('observacoes', models.TextField(blank=True, null=True)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='club.cliente')),
                ('escola', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='club.escolaesporte')),
                ('responsavel_financeiro', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='matriculas_responsavel', to='club.cliente')),
            ],
            options={
                'verbose_name': 'Matrícula na Escola',
                'verbose_name_plural': 'Matrículas nas Escolas',
                'ordering': ['-data_inicio'],
                'unique_together': {('aluno', 'escola')},
            },
        ),
        migrations.CreateModel(
            name='MensalidadeLocacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_vencimento', models.DateField()),
                ('valor_original', models.DecimalField(decimal_places=2, max_digits=8)),
                ('valor_multa', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=8)),
                ('valor_juros', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=8)),
                ('valor_total', models.DecimalField(decimal_places=2, max_digits=8)),
                ('status', models.CharField(choices=[('PENDENTE', 'Pendente'), ('PAGO', 'Pago'), ('VENCIDO', 'Vencido'), ('CANCELADO', 'Cancelado')], default='PENDENTE', max_length=10)),
                ('data_pagamento', models.DateField(blank=True, null=True)),
                ('valor_pago', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('forma_pagamento', models.CharField(blank=True, max_length=20, null=True)),
                ('nosso_numero', models.CharField(blank=True, max_length=20, null=True)),
                ('linha_digitavel', models.CharField(blank=True, max_length=60, null=True)),
                ('codigo_barras', models.CharField(blank=True, max_length=50, null=True)),
                ('observacoes', models.TextField(blank=True, null=True)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('locacao', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='club.locacao')),
            ],
            options={
                'verbose_name': 'Mensalidade de Locação',
                'verbose_name_plural': 'Mensalidades de Locações',
                'ordering': ['-data_vencimento'],
            },
        ),
        migrations.CreateModel(
            name='Socio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plano', models.CharField(choices=[('INDIVIDUAL', 'Plano Individual - R$ 115,00'), ('FAMILIA', 'Plano Família - R$ 170,00')], default='INDIVIDUAL', max_length=10)),
                ('status', models.CharField(choices=[('ATIVO', 'Ativo'), ('INATIVO', 'Inativo'), ('PENDENTE', 'Pendente')], default='PENDENTE', max_length=10)),
                ('convites_mensais', models.PositiveIntegerField(default=4, help_text='Convites não acumulativos')),
                ('taxa_adesao_paga', models.BooleanField(default=False, help_text='Taxa de adesão de R$ 75,00')),
                ('cliente', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='club.cliente')),
            ],
            options={
                'verbose_name': 'Sócio',
                'verbose_name_plural': 'Sócios',
            },
        ),
        migrations.CreateModel(
            name='Dependente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_completo', models.CharField(max_length=255)),
                ('data_nascimento', models.DateField()),
                ('parentesco', models.CharField(choices=[('CONJUGE', 'Companheiro(a)'), ('FILHO', 'Filho(a)')], max_length=10)),
                ('cursando_ensino_superior', models.BooleanField(default=False, help_text='Marcar se for filho(a) entre 18 e 24 anos cursando ensino técnico ou superior')),
                ('pcd', models.BooleanField(default=False, help_text='Marcar se for filho(a) PcD (sem limite de idade)')),
                ('socio_titular', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dependentes', to='club.socio')),
            ],
            options={
                'verbose_name': 'Dependente',
                'verbose_name_plural': 'Dependentes',
            },
        ),
        migrations.CreateModel(
            name='MensalidadeEscola',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes_referencia', models.DateField()),
                ('data_vencimento', models.DateField()),
                ('valor_original', models.DecimalField(decimal_places=2, max_digits=8)),
                ('valor_multa', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=8)),
                ('valor_juros', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=8)),
                ('valor_total', models.DecimalField(decimal_places=2, max_digits=8)),
                ('status', models.CharField(choices=[('PENDENTE', 'Pendente'), ('PAGO', 'Pago'), ('VENCIDO', 'Vencido'), ('CANCELADO', 'Cancelado')], default='PENDENTE', max_length=10)),
                ('data_pagamento', models.DateField(blank=True, null=True)),
                ('valor_pago', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('forma_pagamento', models.CharField(blank=True, max_length=20, null=True)),
                ('nosso_numero', models.CharField(blank=True, max_length=20, null=True)),
                ('linha_digitavel', models.CharField(blank=True, max_length=60, null=True)),
                ('codigo_barras', models.CharField(blank=True, max_length=50, null=True)),
                ('observacoes', models.TextField(blank=True, null=True)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('matricula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='club.matriculaescola')),
            ],
            options={
                'verbose_name': 'Mensalidade da Escola',
                'verbose_name_plural': 'Mensalidades das Escolas',
                'ordering': ['-mes_referencia'],
                'unique_together': {('matricula', 'mes_referencia')},
            },
        ),
        migrations.CreateModel(
            name='RepasseEscola',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes_referencia', models.DateField()),
                ('data_vencimento', models.DateField()),
                ('valor_total_arrecadado', models.DecimalField(decimal_places=2, max_digits=10)),
                ('valor_repasse', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantidade_alunos', models.IntegerField()),
                ('status', models.CharField(choices=[('PENDENTE', 'Pendente'), ('PAGO', 'Pago'), ('VENCIDO', 'Vencido')], default='PENDENTE', max_length=10)),
                ('data_pagamento', models.DateField(blank=True, null=True)),
                ('comprovante', models.FileField(blank=True, null=True, upload_to='comprovantes/repasses/')),
                ('observacoes', models.TextField(blank=True, null=True)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('escola', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='club.escolaesporte')),
            ],
            options={
                'verbose_name': 'Repasse da Escola',
                'verbose_name_plural': 'Repasses das Escolas',
                'ordering': ['-mes_referencia'],
                'unique_together': {('escola', 'mes_referencia')},
            },
        ),
        migrations.CreateModel(
            name='Mensalidade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('MENSALIDADE', 'Mensalidade'), ('TAXA_ADESAO', 'Taxa de Adesão')], default='MENSALIDADE', max_length=15)),
                ('mes_referencia', models.DateField(help_text='Primeiro dia do mês de referência')),
                ('data_vencimento', models.DateField()),
                ('valor_original', models.DecimalField(decimal_places=2, max_digits=8)),
                ('valor_multa', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=8)),
                ('valor_juros', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=8)),
                ('valor_total', models.DecimalField(decimal_places=2, max_digits=8)),
                ('status', models.CharField(choices=[('PENDENTE', 'Pendente'), ('PAGO', 'Pago'), ('VENCIDO', 'Vencido'), ('CANCELADO', 'Cancelado')], default='PENDENTE', max_length=10)),
                ('data_pagamento', models.DateField(blank=True, null=True)),
                ('valor_pago', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('forma_pagamento', models.CharField(blank=True, max_length=20, null=True)),
                ('nosso_numero', models.CharField(blank=True, max_length=20, null=True)),
                ('linha_digitavel', models.CharField(blank=True, max_length=60, null=True)),
                ('codigo_barras', models.CharField(blank=True, max_length=50, null=True)),
                ('observacoes', models.TextField(blank=True, null=True)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_atualizacao', models.DateTimeField(auto_now=True)),
                ('socio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='club.socio')),
            ],
            options={
                'verbose_name': 'Mensalidade',
                'verbose_name_plural': 'Mensalidades',
                'ordering': ['-mes_referencia'],
                'unique_together': {('socio', 'mes_referencia', 'tipo')},
            },
        ),
    ]
