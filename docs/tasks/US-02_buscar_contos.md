# US-02: Buscar Contos

**História**: Como usuário, quero buscar contos por texto ou classificações narrativas, para que eu possa encontrar histórias específicas ou padrões narrativos.

## Tarefas

### Backend
- [ ] Criar função `search_tales(query, filters)` em `xer/database.py`:
  - [ ] Busca textual em título e conteúdo (LIKE ou FTS)
  - [ ] Filtros por classificação (JOIN com tabela classifications)
  - [ ] Retornar resultados ordenados por relevância

### Rotas
- [ ] Criar rota `GET /search` em `main.py`
- [ ] Aceitar query params: `q` (texto), `classification` (filtros)
- [ ] Renderizar template de resultados

### Frontend
- [ ] Adicionar barra de busca na homepage (hero section)
- [ ] Criar template `xer/templates/search.html`:
  - [ ] Exibir query atual
  - [ ] Sidebar com filtros por classificação:
    - [ ] Personagens de Propp (checkboxes)
    - [ ] Estrutura narrativa (checkboxes)
    - [ ] Booker plots (checkboxes)
  - [ ] Grid de resultados (similar à homepage)
  - [ ] Mensagem "Nenhum resultado encontrado" se vazio
  - [ ] Highlighting de termos buscados (opcional)

### Performance
- [ ] Criar índices no SQLite para campos buscados
- [ ] Testar performance com queries complexas

### Testes
- [ ] Testar busca textual simples
- [ ] Testar filtros combinados
- [ ] Verificar edge cases (query vazia, caracteres especiais)
