from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from core.models import Organizacao, Perfil

from .models import Fornecedor, Produto


class ProdutoTestCase(TestCase):

    def test_criacao_produto(self):
        organizacao = Organizacao.objects.create(
            nome='Organização Teste'
        )

        fornecedor = Fornecedor.objects.create(
            organizacao=organizacao,
            nome='Fornecedor Teste',
            email='teste@email.com'
        )

        produto = Produto.objects.create(
            organizacao=organizacao,
            nome='Produto Teste',
            codigo='TESTE001',
            preco=10.00,
            estoque_minimo=5,
            fornecedor=fornecedor
        )

        self.assertEqual(
            produto.nome,
            'Produto Teste'
        )

    def test_pagina_produtos(self):
        organizacao = Organizacao.objects.create(
            nome='Organização Teste'
        )

        usuario = User.objects.create_user(
            username='usuario',
            password='senha-teste-123'
        )

        Perfil.objects.create(
            usuario=usuario,
            organizacao=organizacao
        )

        self.client.force_login(usuario)

        response = self.client.get(
            reverse('produto_list')
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_pagina_produtos_exige_login(self):
        response = self.client.get(
            reverse('produto_list')
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertIn(
            reverse('login'),
            response.url
        )
