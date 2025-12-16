# US-01: Explorar Contos

**História**: Como visitante do site, quero navegar por uma lista de contos de fadas, para que eu possa descobrir histórias interessantes para ler.

## Tarefas

### Setup Inicial
- [ ] Adicionar Jinja2 ao projeto: `uv add jinja2`
- [ ] Criar estrutura de diretórios `xer/templates/` e `static/`
- [ ] Configurar FastAPI para servir static files e templates

### Backend
- [ ] Criar função `list_tales(limit, offset)` em `xer/database.py`
- [ ] Criar rota `GET /` em `main.py` que renderiza a homepage
- [ ] Passar lista de contos para o template

### Frontend
- [ ] Criar template `xer/templates/index.html`:
  - [ ] Hero section com título do site
  - [ ] Grid responsivo de contos (cards)
  - [ ] Paginação (se > 20 contos)
- [ ] Estilizar cards de contos:
  - [ ] Título visível
  - [ ] Preview do texto (primeiras linhas)
  - [ ] Hover effect (elevação/shadow)
  - [ ] Link para página do conto

### Testes
- [ ] Testar listagem com diferentes quantidades de contos
- [ ] Verificar responsividade (mobile/tablet/desktop)
