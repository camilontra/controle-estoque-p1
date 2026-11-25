# Melhorias da P1

1. Padronizar isolamento de dados por organização em todas as consultas e formulários.
2. Evitar consultas N+1 em listagens e movimentações usando `select_related` / `prefetch_related`.
3. Centralizar validações de regra de negócio para não duplicar entre forms, models e API.
4. Revisar permissões e acessos diretos por ID (`pk`) nas views.
