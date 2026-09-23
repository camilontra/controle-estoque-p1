from django.urls import path

from . import views


urlpatterns = [

    # Página inicial
    path(
        '',
        views.home,
        name='home'
    ),

    # Produtos
    path(
        'produtos/',
        views.produto_list,
        name='produto_list'
    ),

    path(
        'produtos/novo/',
        views.produto_create,
        name='produto_create'
    ),

    path(
        'produtos/<int:pk>/editar/',
        views.produto_update,
        name='produto_update'
    ),

    path(
        'produtos/<int:pk>/excluir/',
        views.produto_delete,
        name='produto_delete'
    ),

    # Fornecedores
    path(
        'fornecedores/',
        views.fornecedor_list,
        name='fornecedor_list'
    ),

    path(
        'fornecedores/novo/',
        views.fornecedor_create,
        name='fornecedor_create'
    ),

    path(
        'fornecedores/<int:pk>/editar/',
        views.fornecedor_update,
        name='fornecedor_update'
    ),

    path(
        'fornecedores/<int:pk>/excluir/',
        views.fornecedor_delete,
        name='fornecedor_delete'
    ),

    # Depósitos
    path(
        'depositos/',
        views.deposito_list,
        name='deposito_list'
    ),

    path(
        'depositos/novo/',
        views.deposito_create,
        name='deposito_create'
    ),

    path(
        'depositos/<int:pk>/editar/',
        views.deposito_update,
        name='deposito_update'
    ),

    path(
        'depositos/<int:pk>/excluir/',
        views.deposito_delete,
        name='deposito_delete'
    ),

    # Movimentações
    path(
        'movimentacoes/',
        views.movimentacao_list,
        name='movimentacao_list'
    ),

    path(
        'movimentacoes/nova/',
        views.movimentacao_create,
        name='movimentacao_create'
    ),

    path(
        'movimentacoes/<int:pk>/editar/',
        views.movimentacao_update,
        name='movimentacao_update'
    ),

    path(
        'movimentacoes/<int:pk>/excluir/',
        views.movimentacao_delete,
        name='movimentacao_delete'
    ),

    # Estoque
    path(
        'estoque/',
        views.estoque,
        name='estoque'
    ),
]