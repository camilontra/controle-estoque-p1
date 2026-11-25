from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from core.models import Organizacao, Perfil

from .models import Deposito, Fornecedor, Movimentacao, Produto


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


class IsolamentoOrganizacaoTestCase(TestCase):
    """
    Roteiro de isolamento: duas organizações, dois usuários.
    O usuário A nunca pode ver nem alterar dados da organização B.
    """

    def setUp(self):
        self.org_a = Organizacao.objects.create(nome='Org A')
        self.org_b = Organizacao.objects.create(nome='Org B')

        self.usuario_a = User.objects.create_user(
            username='usuario_a',
            password='senha-teste-123'
        )
        self.usuario_b = User.objects.create_user(
            username='usuario_b',
            password='senha-teste-123'
        )

        Perfil.objects.create(
            usuario=self.usuario_a,
            organizacao=self.org_a
        )
        Perfil.objects.create(
            usuario=self.usuario_b,
            organizacao=self.org_b
        )

        self.fornecedor_a = Fornecedor.objects.create(
            organizacao=self.org_a,
            nome='Fornecedor da A'
        )
        self.fornecedor_b = Fornecedor.objects.create(
            organizacao=self.org_b,
            nome='Fornecedor da B'
        )

        self.deposito_a = Deposito.objects.create(
            organizacao=self.org_a,
            nome='Deposito da A',
            localizacao='Local A'
        )
        self.deposito_b = Deposito.objects.create(
            organizacao=self.org_b,
            nome='Deposito da B',
            localizacao='Local B'
        )

        self.produto_a = Produto.objects.create(
            organizacao=self.org_a,
            nome='Produto da A',
            codigo='COD-A',
            preco=10,
            fornecedor=self.fornecedor_a
        )
        self.produto_b = Produto.objects.create(
            organizacao=self.org_b,
            nome='Produto da B',
            codigo='COD-B',
            preco=20,
            fornecedor=self.fornecedor_b
        )

        self.movimentacao_a = Movimentacao.objects.create(
            organizacao=self.org_a,
            produto=self.produto_a,
            deposito=self.deposito_a,
            tipo='ENTRADA',
            quantidade=10
        )
        self.movimentacao_b = Movimentacao.objects.create(
            organizacao=self.org_b,
            produto=self.produto_b,
            deposito=self.deposito_b,
            tipo='ENTRADA',
            quantidade=99
        )

        self.client.force_login(self.usuario_a)

    # 1. Usuário A abre as listas e vê só o que é da organização A

    def test_listas_mostram_so_a_propria_organizacao(self):
        casos = [
            ('produto_list', 'Produto da A', 'Produto da B'),
            ('fornecedor_list', 'Fornecedor da A', 'Fornecedor da B'),
            ('deposito_list', 'Deposito da A', 'Deposito da B'),
            ('movimentacao_list', 'Produto da A', 'Produto da B'),
        ]

        for nome_url, visivel, oculto in casos:
            with self.subTest(url=nome_url):
                response = self.client.get(reverse(nome_url))

                self.assertContains(response, visivel)
                self.assertNotContains(response, oculto)

    def test_home_e_estoque_contam_so_a_propria_organizacao(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.context['total_produtos'], 1)
        self.assertEqual(response.context['total_fornecedores'], 1)
        self.assertEqual(response.context['total_depositos'], 1)
        self.assertEqual(response.context['total_movimentacoes'], 1)

        response = self.client.get(reverse('estoque'))

        self.assertEqual(response.context['total_unidades'], 10)
        self.assertEqual(len(response.context['estoques']), 1)

    # 2. Usuário A abre o ID da B e recebe 404

    def test_editar_e_excluir_registro_de_outra_organizacao_da_404(self):
        casos = [
            ('produto', self.produto_b),
            ('fornecedor', self.fornecedor_b),
            ('deposito', self.deposito_b),
            ('movimentacao', self.movimentacao_b),
        ]

        for nome, objeto in casos:
            for acao in ['update', 'delete']:
                with self.subTest(url=f'{nome}_{acao}'):
                    url = reverse(
                        f'{nome}_{acao}',
                        args=[objeto.pk]
                    )

                    self.assertEqual(
                        self.client.get(url).status_code,
                        404
                    )

    def test_excluir_por_post_nao_apaga_registro_de_outra_organizacao(self):
        response = self.client.post(
            reverse('produto_delete', args=[self.produto_b.pk])
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(
            Produto.objects.filter(pk=self.produto_b.pk).exists()
        )

    def test_editar_por_post_nao_altera_registro_de_outra_organizacao(self):
        response = self.client.post(
            reverse('produto_update', args=[self.produto_b.pk]),
            {
                'nome': 'Alterado pela A',
                'codigo': 'COD-B',
                'preco': '1.00',
                'estoque_minimo': 0,
            }
        )

        self.assertEqual(response.status_code, 404)

        self.produto_b.refresh_from_db()
        self.assertEqual(self.produto_b.nome, 'Produto da B')

    # 3. Usuário A cria registro: fica na organização A

    def test_criar_produto_grava_a_organizacao_do_usuario(self):
        self.client.post(
            reverse('produto_create'),
            {
                'nome': 'Novo produto',
                'codigo': 'NOVO-1',
                'preco': '5.00',
                'estoque_minimo': 0,
                # tentativa de forjar a organização pelo formulário
                'organizacao': self.org_b.pk,
            }
        )

        produto = Produto.objects.get(codigo='NOVO-1')

        self.assertEqual(produto.organizacao, self.org_a)

    def test_criar_fornecedor_e_deposito_gravam_a_organizacao_do_usuario(self):
        self.client.post(
            reverse('fornecedor_create'),
            {'nome': 'Fornecedor novo'}
        )
        self.client.post(
            reverse('deposito_create'),
            {'nome': 'Deposito novo', 'localizacao': 'Algum lugar'}
        )

        self.assertEqual(
            Fornecedor.objects.get(nome='Fornecedor novo').organizacao,
            self.org_a
        )
        self.assertEqual(
            Deposito.objects.get(nome='Deposito novo').organizacao,
            self.org_a
        )

    def test_criar_movimentacao_grava_a_organizacao_do_usuario(self):
        self.client.post(
            reverse('movimentacao_create'),
            {
                'produto': self.produto_a.pk,
                'deposito': self.deposito_a.pk,
                'tipo': 'ENTRADA',
                'quantidade': 3,
            }
        )

        self.assertEqual(
            Movimentacao.objects.filter(
                organizacao=self.org_a,
                quantidade=3
            ).count(),
            1
        )

    # 4. Selects dos formulários mostram só opções da organização A

    def test_selects_dos_formularios_mostram_so_opcoes_da_organizacao(self):
        response = self.client.get(reverse('produto_create'))
        campos = response.context['form'].fields

        self.assertEqual(
            list(campos['fornecedor'].queryset),
            [self.fornecedor_a]
        )

        response = self.client.get(reverse('movimentacao_create'))
        campos = response.context['form'].fields

        self.assertEqual(
            list(campos['produto'].queryset),
            [self.produto_a]
        )
        self.assertEqual(
            list(campos['deposito'].queryset),
            [self.deposito_a]
        )
        self.assertEqual(
            list(campos['fornecedor'].queryset),
            [self.fornecedor_a]
        )

    def test_nao_aceita_fornecedor_de_outra_organizacao_no_post(self):
        self.client.post(
            reverse('produto_create'),
            {
                'nome': 'Produto com fornecedor alheio',
                'codigo': 'ALHEIO-1',
                'preco': '5.00',
                'estoque_minimo': 0,
                'fornecedor': self.fornecedor_b.pk,
            }
        )

        self.assertFalse(
            Produto.objects.filter(codigo='ALHEIO-1').exists()
        )

    def test_saldo_de_saida_ignora_estoque_de_outra_organizacao(self):
        # A tem 10 unidades; a B tem 99. A não pode retirar 11.
        self.client.post(
            reverse('movimentacao_create'),
            {
                'produto': self.produto_a.pk,
                'deposito': self.deposito_a.pk,
                'tipo': 'SAIDA',
                'quantidade': 11,
            }
        )

        self.assertFalse(
            Movimentacao.objects.filter(
                organizacao=self.org_a,
                tipo='SAIDA'
            ).exists()
        )

    # 5. Unicidade é por organização

    def test_mesmo_codigo_em_organizacoes_diferentes_e_permitido(self):
        response = self.client.post(
            reverse('produto_create'),
            {
                'nome': 'Produto com código da B',
                'codigo': 'COD-B',
                'preco': '5.00',
                'estoque_minimo': 0,
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Produto.objects.filter(
                organizacao=self.org_a,
                codigo='COD-B'
            ).exists()
        )

    def test_codigo_duplicado_na_mesma_organizacao_e_rejeitado(self):
        response = self.client.post(
            reverse('produto_create'),
            {
                'nome': 'Duplicado',
                'codigo': 'COD-A',
                'preco': '5.00',
                'estoque_minimo': 0,
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('codigo', response.context['form'].errors)
        self.assertEqual(
            Produto.objects.filter(
                organizacao=self.org_a,
                codigo='COD-A'
            ).count(),
            1
        )

    def test_editar_produto_mantendo_o_proprio_codigo_e_permitido(self):
        response = self.client.post(
            reverse('produto_update', args=[self.produto_a.pk]),
            {
                'nome': 'Produto da A renomeado',
                'codigo': 'COD-A',
                'preco': '10.00',
                'estoque_minimo': 0,
                'fornecedor': self.fornecedor_a.pk,
            }
        )

        self.assertEqual(response.status_code, 302)

        self.produto_a.refresh_from_db()
        self.assertEqual(self.produto_a.nome, 'Produto da A renomeado')
