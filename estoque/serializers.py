from rest_framework import serializers
from .models import Deposito, Fornecedor, Movimentacao, Produto


class FornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = ['id', 'nome', 'email', 'telefone', 'organizacao']
        read_only_fields = ['organizacao']


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = [
            'id',
            'nome',
            'codigo',
            'preco',
            'estoque_minimo',
            'fornecedor',
            'organizacao',
        ]
        read_only_fields = ['organizacao']


class DepositoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposito
        fields = ['id', 'nome', 'localizacao', 'organizacao']
        read_only_fields = ['organizacao']


class MovimentacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movimentacao
        fields = [
            'id',
            'produto',
            'deposito',
            'tipo',
            'quantidade',
            'data',
            'fornecedor',
            'organizacao',
        ]
        read_only_fields = ['id', 'data', 'organizacao']