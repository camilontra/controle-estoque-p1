from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db.models import Sum
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render
)

from .forms import (
    FornecedorForm,
    ProdutoForm,
    DepositoForm,
    MovimentacaoForm
)

from .models import (
    Fornecedor,
    Produto,
    Deposito,
    Movimentacao
)


def org_atual(request):
    try:
        return request.user.perfil.organizacao
    except ObjectDoesNotExist:
        raise PermissionDenied(
            'Seu usuário não está vinculado a nenhuma organização.'
        )


@login_required
def home(request):
    org = org_atual(request)

    contexto = {
        'total_produtos': Produto.objects.filter(
            organizacao=org
        ).count(),
        'total_fornecedores': Fornecedor.objects.filter(
            organizacao=org
        ).count(),
        'total_depositos': Deposito.objects.filter(
            organizacao=org
        ).count(),
        'total_movimentacoes': Movimentacao.objects.filter(
            organizacao=org
        ).count(),
    }

    return render(
        request,
        'estoque/home.html',
        contexto
    )


# =========================================================
# PRODUTOS
# =========================================================

@login_required
def produto_list(request):
    org = org_atual(request)

    busca = request.GET.get('q', '')
    fornecedor_id = request.GET.get('fornecedor', '')

    produtos = Produto.objects.filter(organizacao=org)

    if busca:
        produtos = produtos.filter(
            nome__icontains=busca
        ) | produtos.filter(
            codigo__icontains=busca
        )

    if fornecedor_id:
        produtos = produtos.filter(
            fornecedor_id=fornecedor_id
        )

    fornecedores = Fornecedor.objects.filter(
        organizacao=org
    ).order_by('nome')

    return render(
        request,
        'estoque/produto_list.html',
        {
            'produtos': produtos,
            'busca': busca,
            'fornecedores': fornecedores,
            'fornecedor_id': fornecedor_id
        }
    )


@login_required
def produto_create(request):
    org = org_atual(request)

    if request.method == 'POST':
        form = ProdutoForm(request.POST, org=org)

        if form.is_valid():
            produto = form.save(commit=False)
            produto.organizacao = org
            produto.save()
            messages.success(
                request,
                'Produto cadastrado com sucesso!'
            )
            return redirect('produto_list')

    else:
        form = ProdutoForm(org=org)

    return render(
        request,
        'estoque/produto_form.html',
        {
            'form': form,
            'titulo': 'Cadastrar produto'
        }
    )


@login_required
def produto_update(request, pk):
    produto = get_object_or_404(
        Produto,
        pk=pk,
        organizacao=org_atual(request)
    )

    if request.method == 'POST':
        form = ProdutoForm(
            request.POST,
            instance=produto,
            org=org_atual(request)
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Produto atualizado com sucesso!'
            )
            return redirect('produto_list')

    else:
        form = ProdutoForm(
            instance=produto,
            org=org_atual(request)
        )

    return render(
        request,
        'estoque/produto_form.html',
        {
            'form': form,
            'titulo': 'Editar produto'
        }
    )


@login_required
def produto_delete(request, pk):
    produto = get_object_or_404(
        Produto,
        pk=pk,
        organizacao=org_atual(request)
    )

    if request.method == 'POST':
        produto.delete()
        messages.success(
            request,
            'Produto excluído com sucesso!'
        )
        return redirect('produto_list')

    return render(
        request,
        'estoque/produto_confirm_delete.html',
        {'produto': produto}
    )


# =========================================================
# FORNECEDORES
# =========================================================

@login_required
def fornecedor_list(request):
    org = org_atual(request)

    busca = request.GET.get('q', '')

    fornecedores = Fornecedor.objects.filter(organizacao=org)

    if busca:
        fornecedores = fornecedores.filter(
            nome__icontains=busca
        ) | fornecedores.filter(
            email__icontains=busca
        )

    return render(
        request,
        'estoque/fornecedor_list.html',
        {
            'fornecedores': fornecedores,
            'busca': busca
        }
    )


@login_required
def fornecedor_create(request):
    org = org_atual(request)

    if request.method == 'POST':
        form = FornecedorForm(request.POST)

        if form.is_valid():
            fornecedor = form.save(commit=False)
            fornecedor.organizacao = org
            fornecedor.save()
            messages.success(
                request,
                'Fornecedor cadastrado com sucesso!'
            )
            return redirect('fornecedor_list')

    else:
        form = FornecedorForm()

    return render(
        request,
        'estoque/fornecedor_form.html',
        {
            'form': form,
            'titulo': 'Cadastrar fornecedor'
        }
    )


@login_required
def fornecedor_update(request, pk):
    fornecedor = get_object_or_404(
        Fornecedor,
        pk=pk,
        organizacao=org_atual(request)
    )

    if request.method == 'POST':
        form = FornecedorForm(
            request.POST,
            instance=fornecedor
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Fornecedor atualizado com sucesso!'
            )
            return redirect('fornecedor_list')

    else:
        form = FornecedorForm(
            instance=fornecedor
        )

    return render(
        request,
        'estoque/fornecedor_form.html',
        {
            'form': form,
            'titulo': 'Editar fornecedor'
        }
    )


@login_required
def fornecedor_delete(request, pk):
    fornecedor = get_object_or_404(
        Fornecedor,
        pk=pk,
        organizacao=org_atual(request)
    )

    if request.method == 'POST':
        fornecedor.delete()
        messages.success(
            request,
            'Fornecedor excluído com sucesso!'
        )
        return redirect('fornecedor_list')

    return render(
        request,
        'estoque/fornecedor_confirm_delete.html',
        {'fornecedor': fornecedor}
    )


# =========================================================
# DEPÓSITOS
# =========================================================

@login_required
def deposito_list(request):
    org = org_atual(request)

    busca = request.GET.get('q', '')

    depositos = Deposito.objects.filter(organizacao=org)

    if busca:
        depositos = depositos.filter(
            nome__icontains=busca
        ) | depositos.filter(
            localizacao__icontains=busca
        )

    return render(
        request,
        'estoque/deposito_list.html',
        {
            'depositos': depositos,
            'busca': busca
        }
    )


@login_required
def deposito_create(request):
    org = org_atual(request)

    if request.method == 'POST':
        form = DepositoForm(request.POST)

        if form.is_valid():
            deposito = form.save(commit=False)
            deposito.organizacao = org
            deposito.save()
            messages.success(
                request,
                'Depósito cadastrado com sucesso!'
            )
            return redirect('deposito_list')

    else:
        form = DepositoForm()

    return render(
        request,
        'estoque/deposito_form.html',
        {
            'form': form,
            'titulo': 'Cadastrar depósito'
        }
    )


@login_required
def deposito_update(request, pk):
    deposito = get_object_or_404(
        Deposito,
        pk=pk,
        organizacao=org_atual(request)
    )

    if request.method == 'POST':
        form = DepositoForm(
            request.POST,
            instance=deposito
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Depósito atualizado com sucesso!'
            )
            return redirect('deposito_list')

    else:
        form = DepositoForm(
            instance=deposito
        )

    return render(
        request,
        'estoque/deposito_form.html',
        {
            'form': form,
            'titulo': 'Editar depósito'
        }
    )


@login_required
def deposito_delete(request, pk):
    deposito = get_object_or_404(
        Deposito,
        pk=pk,
        organizacao=org_atual(request)
    )

    if request.method == 'POST':
        deposito.delete()
        messages.success(
            request,
            'Depósito excluído com sucesso!'
        )
        return redirect('deposito_list')

    return render(
        request,
        'estoque/deposito_confirm_delete.html',
        {'deposito': deposito}
    )


# =========================================================
# MOVIMENTAÇÕES
# =========================================================

@login_required
def movimentacao_list(request):
    org = org_atual(request)

    movimentacoes = (
        Movimentacao.objects
        .filter(organizacao=org)
        .select_related(
            'produto',
            'deposito',
            'fornecedor'
        )
        .order_by('-data')
    )

    return render(
        request,
        'estoque/movimentacao_list.html',
        {
            'movimentacoes': movimentacoes
        }
    )


@login_required
def movimentacao_create(request):
    org = org_atual(request)

    if request.method == 'POST':
        form = MovimentacaoForm(request.POST, org=org)

        if form.is_valid():
            movimentacao = form.save(commit=False)
            movimentacao.organizacao = org
            movimentacao.save()
            messages.success(
                request,
                'Movimentação registrada com sucesso!'
            )
            return redirect('movimentacao_list')

    else:
        form = MovimentacaoForm(org=org)

    return render(
        request,
        'estoque/movimentacao_form.html',
        {
            'form': form,
            'titulo': 'Registrar movimentação'
        }
    )


@login_required
def movimentacao_update(request, pk):
    movimentacao = get_object_or_404(
        Movimentacao,
        pk=pk,
        organizacao=org_atual(request)
    )

    if request.method == 'POST':
        form = MovimentacaoForm(
            request.POST,
            instance=movimentacao,
            org=org_atual(request)
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Movimentação atualizada com sucesso!'
            )
            return redirect('movimentacao_list')

    else:
        form = MovimentacaoForm(
            instance=movimentacao,
            org=org_atual(request)
        )

    return render(
        request,
        'estoque/movimentacao_form.html',
        {
            'form': form,
            'titulo': 'Editar movimentação'
        }
    )


@login_required
def movimentacao_delete(request, pk):
    movimentacao = get_object_or_404(
        Movimentacao,
        pk=pk,
        organizacao=org_atual(request)
    )

    if request.method == 'POST':
        movimentacao.delete()
        messages.success(
            request,
            'Movimentação excluída com sucesso!'
        )
        return redirect('movimentacao_list')

    return render(
        request,
        'estoque/movimentacao_confirm_delete.html',
        {
            'movimentacao': movimentacao
        }
    )


# =========================================================
# ESTOQUE
# =========================================================

@login_required
def estoque(request):

    org = org_atual(request)

    produtos = Produto.objects.filter(
        organizacao=org
    ).order_by('nome')

    depositos = Deposito.objects.filter(
        organizacao=org
    ).order_by('nome')

    saldos = []

    for produto in produtos:

        for deposito in depositos:

            entradas = (
                Movimentacao.objects
                .filter(
                    organizacao=org,
                    produto=produto,
                    deposito=deposito,
                    tipo='ENTRADA'
                )
                .aggregate(
                    total=Sum('quantidade')
                )['total']
                or 0
            )

            saidas = (
                Movimentacao.objects
                .filter(
                    organizacao=org,
                    produto=produto,
                    deposito=deposito,
                    tipo='SAIDA'
                )
                .aggregate(
                    total=Sum('quantidade')
                )['total']
                or 0
            )

            saldo = entradas - saidas

            saldos.append({
                'produto': produto,
                'deposito': deposito,
                'entradas': entradas,
                'saidas': saidas,
                'saldo': saldo,
                'baixo_estoque': (
                    saldo <= produto.estoque_minimo
                )
            })

    total_produtos = produtos.count()

    total_unidades = sum(
        item['saldo']
        for item in saldos
    )

    total_estoque_baixo = sum(
        1
        for item in saldos
        if item['baixo_estoque']
    )

    return render(
        request,
        'estoque/estoque.html',
        {
            'estoques': saldos,
            'total_produtos': total_produtos,
            'total_unidades': total_unidades,
            'total_estoque_baixo': total_estoque_baixo
        }
    )