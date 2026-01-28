---
description: Implementar uma user story do início ao fim
---

# Workflow: Implementar User Story

Este workflow guia a implementação completa de uma user story.

## Passos

1. **Confirmar qual User Story implementar**
   - Perguntar ao usuário qual US (ex: US-01, US-02, etc.)
   - Abrir `docs/user_stories.md` para contexto
   - Abrir `docs/tasks/US-XX_nome.md` correspondente

2. **Revisar Princípios e Arquitetura**
   - Revisar `docs/principles.md` para garantir alinhamento
   - Consultar `docs/implementation_plan.md` para decisões técnicas

3. **Implementar Tarefas Sequencialmente**
   - Seguir o checklist em `docs/tasks/US-XX_nome.md`
   - Marcar cada task como `[x]` quando completada
   - Criar commits incrementais (se aplicável)

4. **Executar Testes**
// turbo
   - Informar usuário para rodar: `uv run taskipy test`

5. **Verificação de Qualidade**
   - Informar usuário para rodar: `uv run taskipy lint` e `uv run taskipy format`
   - NÃO executar automaticamente - apenas informar

6. **Atualizar User Story**
   - Marcar critérios de aceitação em `docs/user_stories.md` como completos
   - Pedir review ao usuário

7. **Documentar**
   - Se houve mudanças significativas, atualizar `docs/implementation_plan.md`