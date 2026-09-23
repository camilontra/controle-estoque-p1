from django.contrib import messages
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

 
def home(request):
    contexto = {
        'total_produtos': Produto.objects.count(),
        'total_fornecedores': Fornecedor.objects.count(),
        'total_depositos': Deposito.objects.count(),
        'total_movimentacoes': Movimentacao.objects.count(),
    }

    return render(
        request,
        'estoque/home.html',
        contexto
    )


# =========================================================
# PRODUTOS
# =========================================================

def produto_list(request):
    busca = request.GET.get('q', '')
    fornecedor_id = request.GET.get('fornecedor', '')

    produtos = Produto.objects.all()

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

    fornecedores = Fornecedor.objects.all().order_by('nome')

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


def produto_create(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Produto cadastrado com sucesso!'
            )
            return redirect('produto_list')

    else:
        form = ProdutoForm()

    return render(
        request,
        'estoque/produto_form.html',
        {
            'form': form,
            'titulo': 'Cadastrar produto'
        }
    )


def produto_update(request, pk):
    produto = get_object_or_404(
        Produto,
        pk=pk
    )

    if request.method == 'POST':
        form = ProdutoForm(
            request.POST,
            instance=produto
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
            instance=produto
        )

    return render(
        request,
        'estoque/produto_form.html',
        {
            'form': form,
            'titulo': 'Editar produto'
        }
    )


def produto_delete(request, pk):
    produto = get_object_or_404(
        Produto,
        pk=pk
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

def fornecedor_list(request):
    busca = request.GET.get('q', '')

    fornecedores = Fornecedor.objects.all()

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


def fornecedor_create(request):
    if request.method == 'POST':
        form = FornecedorForm(request.POST)

        if form.is_valid():
            form.save()
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


def fornecedor_update(request, pk):
    fornecedor = get_object_or_404(
        Fornecedor,
        pk=pk
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


def fornecedor_delete(request, pk):
    fornecedor = get_object_or_404(
        Fornecedor,
        pk=pk
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

def deposito_list(request):
    busca = request.GET.get('q', '')

    depositos = Deposito.objects.all()

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


def deposito_create(request):
    if request.method == 'POST':
        form = DepositoForm(request.POST)

        if form.is_valid():
            form.save()
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


def deposito_update(request, pk):
    deposito = get_object_or_404(
        Deposito,
        pk=pk
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


def deposito_delete(request, pk):
    deposito = get_object_or_404(
        Deposito,
        pk=pk
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

def movimentacao_list(request):
    movimentacoes = (
        Movimentacao.objects
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


def movimentacao_create(request):
    if request.method == 'POST':
        form = MovimentacaoForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Movimentação registrada com sucesso!'
            )
            return redirect('movimentacao_list')

    else:
        form = MovimentacaoForm()

    return render(
        request,
        'estoque/movimentacao_form.html',
        {
            'form': form,
            'titulo': 'Registrar movimentação'
        }
    )


def movimentacao_update(request, pk):
    movimentacao = get_object_or_404(
        Movimentacao,
        pk=pk
    )

    if request.method == 'POST':
        form = MovimentacaoForm(
            request.POST,
            instance=movimentacao
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
            instance=movimentacao
        )

    return render(
        request,
        'estoque/movimentacao_form.html',
        {
            'form': form,
            'titulo': 'Editar movimentação'
        }
    )


def movimentacao_delete(request, pk):
    movimentacao = get_object_or_404(
        Movimentacao,
        pk=pk
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

def estoque(request):

    produtos = Produto.objects.all().order_by('nome')

    depositos = Deposito.objects.all().order_by('nome')

    saldos = []

    for produto in produtos:

        for deposito in depositos:

            entradas = (
                Movimentacao.objects
                .filter(
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

    total_produtos = Produto.objects.count()

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