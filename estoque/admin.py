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
        'telefone',
        'organizacao'
    ]

    search_fields = [
        'nome',
        'email'
    ]

    list_filter = [
        'organizacao'
    ]


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = [
        'codigo',
        'nome',
        'preco',
        'estoque_minimo',
        'fornecedor',
        'organizacao'
    ]

    search_fields = [
        'nome',
        'codigo'
    ]

    list_filter = [
        'organizacao',
        'fornecedor'
    ]


@admin.register(Deposito)
class DepositoAdmin(admin.ModelAdmin):
    list_display = [
        'nome',
        'localizacao',
        'organizacao'
    ]

    search_fields = [
        'nome',
        'localizacao'
    ]

    list_filter = [
        'organizacao'
    ]


@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = [
        'produto',
        'deposito',
        'tipo',
        'quantidade',
        'data',
        'fornecedor',
        'organizacao'
    ]

    list_filter = [
        'organizacao',
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