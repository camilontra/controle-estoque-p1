from django.contrib import admin

from .models import (
    Fornecedor,
    Produto,
    Deposito,
    Movimentacao
)


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = [
        'nome',
        'email',
        'telefone'
    ]

    search_fields = [
        'nome',
        'email'
    ]


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = [
        'codigo',
        'nome',
        'preco',
        'estoque_minimo',
        'fornecedor'
    ]

    search_fields = [
        'nome',
        'codigo'
    ]

    list_filter = [
        'fornecedor'
    ]


@admin.register(Deposito)
class DepositoAdmin(admin.ModelAdmin):
    list_display = [
        'nome',
        'localizacao'
    ]

    search_fields = [
        'nome',
        'localizacao'
    ]


@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = [
        'produto',
        'deposito',
        'tipo',
        'quantidade',
        'data',
        'fornecedor'
    ]

    list_filter = [
        'tipo',
        'deposito',
        'data'
    ]

    search_fields = [
        'produto__nome',
        'produto__codigo'
    ]

    readonly_fields = [
        'data'
    ]