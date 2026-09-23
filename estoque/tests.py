from django.test import TestCase
from django.urls import reverse

from .models import Fornecedor, Produto


class ProdutoTestCase(TestCase):

    def test_criacao_produto(self):
        fornecedor = Fornecedor.objects.create(
            nome='Fornecedor Teste',
            email='teste@email.com'
        )

        produto = Produto.objects.create(
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
        response = self.client.get(
            reverse('produto_list')
        )

        self.assertEqual(
            response.status_code,
            200
        )