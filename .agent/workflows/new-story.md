---
description: Criar uma nova user story e tasks correspondentes
---

# Workflow: Nova User Story

Este workflow guia a criação de uma nova user story com tasks detalhadas.

## Passos

1. **Coletar Informações**
   - Perguntar ao usuário:
     - Quem é o usuário? (ex: visitante, leitor, admin)
     - O que ele quer fazer?
     - Por que ele quer fazer isso?
   - Pedir critérios de aceitação específicos

2. **Gerar ID da User Story**
   - Verificar última US em `docs/user_stories.md`
   - Atribuir próximo ID (ex: US-05)

3. **Adicionar em docs/user_stories.md**
   - Seguir formato existente:
     ```markdown
     ## US-XX: Título
     
     **Como** [papel]
     **Quero** [ação]
     **Para que** [benefício]
     
     ### Critérios de Aceitação
     - [ ] Critério 1
     - [ ] Critério 2
     
     ### Tarefas Relacionadas
     Ver [`docs/tasks/US-XX_nome.md`](file://...)
     ```

4. **Criar Arquivo de Tasks**
   - Criar `docs/tasks/US-XX_nome.md`
   - Quebrar a story em tarefas acionáveis:
     - Setup/Pré-requisitos
     - Backend (se aplicável)
     - Frontend (se aplicável)
     - Testes
   - Usar checkboxes `- [ ]` para tracking

5. **Validar com Princípios**
   - Revisar se a story está alinhada com `docs/principles.md`
   - Se houver impacto arquitetural, mencionar `docs/implementation_plan.md`

6. **Request Review**
   - Pedir ao usuário para revisar a nova story e tasks
   - Ajustar conforme feedback
