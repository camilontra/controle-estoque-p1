from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from estoque.api_views import (
    DepositoViewSet,
    FornecedorViewSet,
    MovimentacaoViewSet,
    ProdutoViewSet,
)

router = DefaultRouter()
router.register(r'produtos', ProdutoViewSet, basename='api-produto')
router.register(r'fornecedores', FornecedorViewSet, basename='api-fornecedor')
router.register(r'depositos', DepositoViewSet, basename='api-deposito')
router.register(r'movimentacoes', MovimentacaoViewSet, basename='api-movimentacao')

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'login/',
        auth_views.LoginView.as_view(),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),
    path('api/', include(router.urls)),
    path('', include('estoque.urls')),
]