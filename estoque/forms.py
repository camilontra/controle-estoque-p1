from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Sum

from .models import (
    Fornecedor,
    Produto,
    Deposito,
    Movimentacao
)


class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ['nome', 'email', 'telefone']


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            'nome',
            'codigo',
            'preco',
            'estoque_minimo',
            'fornecedor'
        ]


class DepositoForm(forms.ModelForm):
    class Meta:
        model = Deposito
        fields = ['nome', 'localizacao']


class MovimentacaoForm(forms.ModelForm):

    class Meta:
        model = Movimentacao
        fields = [
            'produto',
            'deposito',
            'tipo',
            'quantidade',
            'fornecedor'
        ]

    def clean(self):
        cleaned_data = super().clean()

        produto = cleaned_data.get('produto')
        deposito = cleaned_data.get('deposito')
        tipo = cleaned_data.get('tipo')
        quantidade = cleaned_data.get('quantidade')

        if (
            produto
            and deposito
            and tipo == 'SAIDA'
            and quantidade
        ):
            entradas = (
                Movimentacao.objects
                .filter(
                    produto=produto,
                    deposito=deposito,
                    tipo='ENTRADA'
                )
                .aggregate(total=Sum('quantidade'))['total']
                or 0
            )

            saidas = (
                Movimentacao.objects
                .filter(
                    produto=produto,
                    deposito=deposito,
                    tipo='SAIDA'
                )
                .aggregate(total=Sum('quantidade'))['total']
                or 0
            )

            saldo = entradas - saidas

            # Se estamos editando uma movimentação
            # de saída existente, devolvemos sua quantidade
            # ao saldo antes de fazer a validação.
            if self.instance.pk:
                movimentacao_anterior = self.instance

                if (
                    movimentacao_anterior.produto_id == produto.id
                    and movimentacao_anterior.deposito_id == deposito.id
                    and movimentacao_anterior.tipo == 'SAIDA'
                ):
                    saldo += movimentacao_anterior.quantidade

            if quantidade > saldo:
                raise ValidationError(
                    f'Não é possível retirar {quantidade} unidades. '
                    f'O estoque disponível é de {saldo} unidades.'
                )

        return cleaned_data