# US-01: Explorar Contos

**História**: Como visitante do site, quero navegar por uma lista de contos de fadas, para que eu possa descobrir histórias interessantes para ler.

## Tarefas

### Setup Inicial
- [x] Adicionar Jinja2 ao projeto: `uv add jinja2`
- [x] Criar estrutura de diretórios `xer/templates/` e `static/`
- [x] Configurar FastAPI para servir static files e templates

### Backend
- [x] Criar função `list_tales(limit, offset)` em `xer/database.py`
- [x] Criar rota `GET /` em `main.py` que renderiza a homepage
- [x] Passar lista de contos para o template

### Frontend
- [x] Criar template `xer/templates/index.html`:
  - [x] Hero section com título do site
  - [x] Grid responsivo de contos (cards)
  - [x] Paginação (se > 20 contos)
- [x] Estilizar cards de contos:
  - [x] Título visível
  - [x] Preview do texto (primeiras linhas)
  - [x] Hover effect (elevação/shadow)
  - [x] Link para página do conto

### Testes
- [x] Testar listagem com diferentes quantidades de contos
- [x] Verificar responsividade (mobile/tablet/desktop)

