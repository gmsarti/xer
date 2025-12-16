---
description: Executar verificações de qualidade do código
---

# Workflow: Verificação de Qualidade

Este workflow executa todas as verificações de qualidade do projeto.

## Passos

1. **Rodar Testes**
// turbo
   ```bash
   uv run taskipy test_cov
   ```

2. **Verificar Linting**
// turbo
   ```bash
   uv run taskipy lint
   ```

3. **Formatar Código**
// turbo
   ```bash
   uv run taskipy format
   ```

4. **Verificar Novamente (após format)**
// turbo
   ```bash
   uv run taskipy lint
   ```

5. **Reportar Resultados**
   - Informar ao usuário o status de todos os checks
   - Se houver falhas, listar os problemas encontrados
   - Sugerir correções se necessário
