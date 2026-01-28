# User Stories

Este documento captura as histórias de usuário do projeto, fornecendo uma visão ampla das funcionalidades do ponto de vista do usuário.

## US-01: Explorar Contos

**Como** visitante do site  
**Quero** navegar por uma lista de contos de fadas  
**Para que** eu possa descobrir histórias interessantes para ler

### Critérios de Aceitação
- [x] Homepage exibe uma lista visual de contos (cards/grid)
- [x] Cada card mostra título e preview do conto
- [x] Interface é visualmente atraente (design premium)
- [x] Paginação funciona corretamente para grandes volumes

### Tarefas Relacionadas
Ver [`docs/tasks/US-01_explorar_contos.md`](file:///Users/gustavosarti/Work/code/xer/docs/tasks/US-01_explorar_contos.md)

---

## US-02: Buscar Contos

**Como** usuário  
**Quero** buscar contos por texto ou classificações narrativas  
**Para que** eu possa encontrar histórias específicas ou padrões narrativos

### Critérios de Aceitação
- [x] Campo de busca textual funciona (título/conteúdo)
- [ ] Filtros por classificação estão disponíveis (Propp, Booker)
- [x] Limitador do número de resultados é funcional
- [x] Resultados são relevantes e bem formatados
- [x] Busca é rápida (< 500ms para queries simples)

### Tarefas Relacionadas
Ver [`docs/tasks/US-02_buscar_contos.md`](file:///Users/gustavosarti/Work/code/xer/docs/tasks/US-02_buscar_contos.md)

---

## US-03: Ler Contos

**Como** leitor  
**Quero** uma experiência de leitura focada e confortável  
**Para que** eu possa ler contos sem distrações

### Critérios de Aceitação
- [x] Tipografia otimizada para leitura (line-height, measure)
- [x] Layout limpo sem elementos visuais competindo
- [x] Metadados (classificações) visíveis mas não intrusivos
- [x] Navegação entre contos (próximo/anterior) disponível

### Tarefas Relacionadas
Ver [`docs/tasks/US-03_ler_contos.md`](file:///Users/gustavosarti/Work/code/xer/docs/tasks/US-03_ler_contos.md)

---

## US-04: Design System (Infraestrutura)

**Como** desenvolvedor  
**Quero** um design system consistente  
**Para que** todas as páginas tenham aparência e comportamento uniforme

### Critérios de Aceitação
- [x] Paleta de cores definida (CSS variables)
- [x] Tipografia consistente em todas as páginas
- [x] Componentes reutilizáveis (cards, buttons, forms)
- [x] Código CSS é maintainable e organizado

### Tarefas Relacionadas
Ver [`docs/tasks/US-04_design_system.md`](file:///Users/gustavosarti/Work/code/xer/docs/tasks/US-04_design_system.md)
