from django.db import models
from core.models import DaOrganizacao


class Fornecedor(DaOrganizacao):
    nome = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.nome


class Produto(DaOrganizacao):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque_minimo = models.PositiveIntegerField(default=0)
    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["organizacao", "codigo"],
                name="codigo_unico_por_org",
            ),
        ]

    def __str__(self):
        return f"{self.codigo} - {self.nome}"


class Deposito(DaOrganizacao):
    nome = models.CharField(max_length=100)
    localizacao = models.CharField(max_length=150)

    def __str__(self):
        return self.nome


class Movimentacao(DaOrganizacao):
    TIPO_CHOICES = [
        ("ENTRADA", "Entrada"),
        ("SAIDA", "Saída"),
    ]

    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
    )

    deposito = models.ForeignKey(
        Deposito,
        on_delete=models.CASCADE,
    )

    tipo = models.CharField(
        max_length=10,
        choices=TIPO_CHOICES,
    )

    quantidade = models.PositiveIntegerField()

    data = models.DateTimeField(auto_now_add=True)

    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.produto.nome} - {self.tipo} - {self.quantidade}"