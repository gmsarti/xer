# Como Usar os Workflows do Antigravity

Este projeto está configurado com regras customizadas e workflows para guiar o desenvolvimento.

## Regras Customizadas

As regras em `.agent/rules.md` são **automaticamente aplicadas** pelo Antigravity. Elas incluem:
- **Não fazer correções automáticas de linting** (responsabilidade do Ruff)
- **Consultar `docs/` como fonte da verdade** para decisões
- **Priorizar estética premium** conforme princípios

## Workflows Disponíveis

Use os workflows com comandos `/` no chat:

### `/implement-story` - Implementar User Story
Implementa uma user story do início ao fim seguindo o checklist em `docs/tasks/`.

**Exemplo de uso:**
```
/implement-story US-01
```

O agente vai:
1. Abrir `docs/user_stories.md` e `docs/tasks/US-01_explorar_contos.md`
2. Validar contra princípios e arquitetura
3. Implementar tarefas sequencialmente
4. Rodar testes
5. Atualizar documentação

---

### `/new-story` - Criar Nova User Story
Cria uma nova user story com tasks detalhadas.

**Exemplo de uso:**
```
/new-story
```

O agente vai perguntar:
- Quem é o usuário?
- O que ele quer fazer?
- Por quê?
- Critérios de aceitação

E então criar `docs/user_stories.md` (nova entrada) e `docs/tasks/US-XX_nome.md`.

---

### `/quality-check` - Verificação de Qualidade
Executa todas as verificações de qualidade do código.

**Exemplo de uso:**
```
/quality-check
```

Roda automaticamente (com `// turbo`):
- `uv run taskipy test_cov`
- `uv run taskipy lint`
- `uv run taskipy format`

---

### `/test-suite` - Rodar Testes
Executa a suite completa de testes com cobertura.

**Exemplo de uso:**
```
/test-suite
```

---

## Editando Workflows

Os workflows estão em `.agent/workflows/`. Você pode:
- **Editar** workflows existentes para ajustar passos
- **Adicionar** novos workflows criando arquivos `.md` no diretório

### Formato de Workflow

```markdown
---
description: Breve descrição do workflow
---

# Workflow: Nome

## Passos

1. **Passo 1**
   - Descrição do que fazer

// turbo
2. **Passo 2 (Auto-run)**
   ```bash
   comando que roda automaticamente
   ```

3. **Passo 3**
   - Outro passo
```

**Nota**: A anotação `// turbo` faz comandos rodarem automaticamente sem confirmação.

---

## Dicas de Uso

### Combinar com Instruções Diretas
```
/implement-story US-01, mas deixe a estilização CSS para depois
```

### Atualizar Documentação Durante Workflow
Os workflows já atualizam `docs/` automaticamente, marcando tasks como `[x]` quando concluídas.

### Verificar Alinhamento com Princípios
```
Antes de implementar, revise se está alinhado com docs/principles.md
```

---

## Estrutura Completa

```
.agent/
├── rules.md                      # Regras aplicadas automaticamente
└── workflows/
    ├── implement-story.md        # /implement-story
    ├── new-story.md              # /new-story
    ├── quality-check.md          # /quality-check
    └── test-suite.md             # /test-suite

docs/
├── principles.md                 # Princípios do projeto
├── tech_stack.md                 # Stack técnica
├── specification.md              # O que será construído
├── implementation_plan.md        # Como será construído
├── user_stories.md               # User stories (visão ampla)
└── tasks/
    ├── US-01_explorar_contos.md  # Tasks detalhadas
    ├── US-02_buscar_contos.md
    ├── US-03_ler_contos.md
    └── US-04_design_system.md
```
