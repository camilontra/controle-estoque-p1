from django.db import models


class Organizacao(models.Model):
    nome = models.CharField(max_length=120)
    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class DaOrganizacao(models.Model):
    # null=True é temporário: será removido depois da migração de dados,
    # para não perder os registros que já existem.
    organizacao = models.ForeignKey(
        'core.Organizacao',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    class Meta:
        abstract = True
