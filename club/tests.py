from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Cliente, Socio

class SocioClienteFlowTests(TestCase):
    def setUp(self):
        self.client = Client()
        User = get_user_model()
        self.user = User.objects.create_user(
            username='gestora', password='1234', tipo_usuario='GESTORA', nome_completo='Gestora Teste', cpf='000.000.000-00', ativo=True
        )
        self.user.pode_gerenciar_socios = True
        self.user.save()
        self.client.login(username='gestora', password='1234')
        self.cliente = Cliente.objects.create(
            nome_completo='Cliente Teste', cpf='111.111.111-11', data_nascimento='2000-01-01', email='cliente@teste.com', telefone='123456789'
        )
        self.socio = Socio.objects.create(cliente=self.cliente)

    def test_socio_detail(self):
        url = reverse('club:socio_detail', args=[self.socio.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Cliente Teste')

    def test_socio_edit(self):
        url = reverse('club:socio_edit', args=[self.socio.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post(url, {'cliente': self.cliente.pk})
        self.assertEqual(resp.status_code, 302)

    def test_socio_delete(self):
        url = reverse('club:socio_delete', args=[self.socio.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Socio.objects.filter(pk=self.socio.pk).exists())

    def test_cliente_detail(self):
        url = reverse('club:cliente_detail', args=[self.cliente.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Cliente Teste')

    def test_cliente_edit(self):
        url = reverse('club:cliente_edit', args=[self.cliente.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post(url, {
            'nome_completo': 'Cliente Editado',
            'cpf': '111.111.111-11',
            'data_nascimento': '2000-01-01',
            'email': 'cliente@teste.com',
            'telefone': '987654321'
        })
        self.assertEqual(resp.status_code, 302)
        self.cliente.refresh_from_db()
        self.assertEqual(self.cliente.nome_completo, 'Cliente Editado')

    def test_cliente_delete(self):
        url = reverse('club:cliente_delete', args=[self.cliente.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Cliente.objects.filter(pk=self.cliente.pk).exists())

class ModulosPrincipaisFlowTests(TestCase):
    def setUp(self):
        self.client = Client()
        User = get_user_model()
        self.user = User.objects.create_user(
            username='gestora2', password='1234', tipo_usuario='GESTORA', nome_completo='Gestora 2', cpf='222.222.222-22', ativo=True
        )
        self.user.pode_gerenciar_locacoes = True
        self.user.pode_gerenciar_escolas = True
        self.user.pode_gerenciar_dayuse = True
        self.user.pode_gerenciar_financeiro = True
        self.user.save()
        self.client.login(username='gestora2', password='1234')

    def test_locacoes_list(self):
        url = reverse('club:locacoes_list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('locacoes', resp.context)

    def test_locacao_create_get(self):
        url = reverse('club:locacao_create')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_escolas_list(self):
        url = reverse('club:escolas_list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('escolas', resp.context)

    def test_escola_create_get(self):
        url = reverse('club:escola_create')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_dayuse_list(self):
        url = reverse('club:dayuse_list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('dayuses', resp.context)

    def test_dayuse_create_get(self):
        url = reverse('club:dayuse_create')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_financeiro_dashboard(self):
        url = reverse('club:financeiro_dashboard')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('stats', resp.context)
