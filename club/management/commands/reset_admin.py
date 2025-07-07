from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()

class Command(BaseCommand):
    help = 'Reseta/cria o superusuário admin'

    def handle(self, *args, **options):
        username = 'clubeadmin'
        email = 'admin@clubevizinhorte.com'
        password = 'ClubVN2025!'
        
        try:
            # Remove usuário existente se houver
            if User.objects.filter(username=username).exists():
                User.objects.filter(username=username).delete()
                self.stdout.write(f'Usuário {username} removido.')
            
            # Cria novo usuário
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                nome_completo='Administrador do Clube',
                cpf='000.000.000-00',
                tipo_usuario='ADMIN'
            )
            user.is_superuser = True
            user.is_staff = True
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Superusuário "{username}" criado com sucesso!')
            )
            self.stdout.write(
                self.style.WARNING(f'🔑 Login: {username}')
            )
            self.stdout.write(
                self.style.WARNING(f'🔒 Senha: {password}')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erro: {e}')
            )
