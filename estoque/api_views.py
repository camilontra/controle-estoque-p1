from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from .models import Deposito, Fornecedor, Movimentacao, Produto
from .serializers import (
    DepositoSerializer,
    FornecedorSerializer,
    MovimentacaoSerializer,
    ProdutoSerializer,
)


class BaseOrganizacaoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_organizacao(self):
        try:
            return self.request.user.perfil.organizacao
        except ObjectDoesNotExist:
            raise PermissionDenied(
                'Seu usuário não está vinculado a nenhuma organização.'
            )

    def get_queryset(self):
        org = self.get_organizacao()
        return self.queryset.filter(organizacao=org)

    def perform_create(self, serializer):
        serializer.save(organizacao=self.get_organizacao())


class ProdutoViewSet(BaseOrganizacaoViewSet):
    queryset = Produto.objects.select_related('fornecedor').all()
    serializer_class = ProdutoSerializer


class FornecedorViewSet(BaseOrganizacaoViewSet):
    queryset = Fornecedor.objects.all()
    serializer_class = FornecedorSerializer


class DepositoViewSet(BaseOrganizacaoViewSet):
    queryset = Deposito.objects.all()
    serializer_class = DepositoSerializer


class MovimentacaoViewSet(BaseOrganizacaoViewSet):
    queryset = Movimentacao.objects.select_related(
        'produto', 'deposito', 'fornecedor'
    ).all()
    serializer_class = MovimentacaoSerializer