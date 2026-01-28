---
description: Executar suite completa de testes
---

# Workflow: Suite de Testes

Este workflow executa todos os testes do projeto.

## Passos

1. **Rodar testes com cobertura**
// turbo
   ```bash
   uv run taskipy test_cov
   ```

2. **Analisar resultados**
   - Reportar número de testes passados/falhados
   - Reportar cobertura de código
   - Se houver falhas, mostrar detalhes

3. **Sugerir próximos passos**
   - Se testes passaram: informar que o código está pronto
   - Se testes falharam: ajudar a debugar ou oferecer para corrigir
   - Se cobertura baixa: sugerir áreas que precisam de mais testes
