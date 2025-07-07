from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()

class Command(BaseCommand):
    help = 'Cria um superusuário padrão se não existir'

    def handle(self, *args, **options):
        username = 'admin'
        email = 'admin@clubevizinhorte.com'
        password = 'admin123'
        
        try:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    nome_completo='Administrador do Sistema',
                    cpf='000.000.000-00',
                    tipo_usuario='ADMIN'
                )
                user.is_superuser = True
                user.is_staff = True
                user.save()
                
                self.stdout.write(
                    self.style.SUCCESS(f'Superusuário "{username}" criado com sucesso!')
                )
                self.stdout.write(
                    self.style.WARNING(f'Login: {username}')
                )
                self.stdout.write(
                    self.style.WARNING(f'Senha: {password}')
                )
                self.stdout.write(
                    self.style.WARNING('IMPORTANTE: Altere a senha após o primeiro login!')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Usuário "{username}" já existe.')
                )
        except IntegrityError as e:
            self.stdout.write(
                self.style.ERROR(f'Erro ao criar usuário: {e}')
            )
