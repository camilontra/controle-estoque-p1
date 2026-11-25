# Controle de Estoque

Sistema web desenvolvido em Django para controle de estoque.

## Funcionalidades

- Cadastro de produtos
- Cadastro de fornecedores
- Cadastro de depósitos
- Registro de movimentações
- Controle de entradas e saídas
- Cálculo do saldo de estoque
- Validação para impedir saída maior que o estoque disponível

## Tecnologias

- Python
- Django
- SQLite
- HTML
- CSS

## Como executar

Clone o projeto e entre na pasta:

```bash
cd controle-estoque-p1
```

## Multi-organização

O sistema atende várias organizações na mesma base de dados. Cada dado
(fornecedores, produtos, depósitos e movimentações) pertence a uma
organização, e cada usuário enxerga somente os dados da organização
à qual está vinculado.

Estratégia adotada: **coluna discriminadora** (todos os dados no mesmo
banco, com uma chave estrangeira para `Organizacao`).

### Como cadastrar organizações e usuários

Por enquanto o cadastro é feito pelo Django Admin (`/admin/`):

1. Crie as organizações em **Organizações**.
2. Crie os usuários em **Usuários**.
3. Vincule cada usuário a uma organização em **Perfis**.

Os registros que já existiam antes da multi-organização foram
atribuídos, pela migração de dados, à organização **Organização padrão**.

### Roteiro de testes de isolamento

Duas organizações (A e B) e dois usuários (um em cada).

| Cenário | Resultado esperado | Resultado obtido |
|---|---|---|
| Usuário A abre as listas (produtos, fornecedores, depósitos, movimentações) | Vê só os dados da organização A | Aprovado |
| Usuário A abre a edição ou exclusão de um registro da B pelo ID na URL | Erro 404 | Aprovado |
| Usuário A cria um registro | Gravado com a organização A, mesmo que o formulário tente enviar outra | Aprovado |
| Formulários do usuário A | Selects mostram só opções da organização A | Aprovado |
| Usuário A cadastra um produto com um código que a B já usa | Permitido (unicidade é por organização) | Aprovado |
| Usuário A cadastra um produto com um código que a própria A já usa | Recusado com mensagem no formulário | Aprovado |
| Usuário A tenta retirar do estoque mais do que a organização A possui | Recusado (o saldo da B não conta) | Aprovado |
| Acesso sem login | Redireciona para a tela de login | Aprovado |

Esse roteiro está automatizado em `estoque/tests.py`
(classe `IsolamentoOrganizacaoTestCase`). Para executar:

```bash
python manage.py test
```
