# US-03: Ler Contos

**História**: Como leitor, quero uma experiência de leitura focada e confortável, para que eu possa ler contos sem distrações.

## Tarefas

### Backend
- [ ] Criar função `get_tale(id)` em `xer/database.py`
- [ ] Criar função `get_tale_classifications(tale_id)` para buscar metadados
- [ ] Criar rota `GET /tales/{id}` em `main.py`

### Frontend
- [ ] Criar template `xer/templates/tale.html`:
  - [ ] Layout em 2 colunas (desktop) ou 1 coluna (mobile):
    - **Main**: Texto do conto
    - **Sidebar**: Metadados e classificações
  - [ ] Tipografia otimizada:
    - [ ] Line-height: ~1.6-1.8
    - [ ] Measure (largura): ~65-75 caracteres
    - [ ] Font-size: 18-20px
  - [ ] Título do conto destacado
  - [ ] Navegação:
    - [ ] Botão "← Voltar"
    - [ ] Links "Próximo/Anterior conto" (opcional)

### Sidebar de Metadados
- [ ] Exibir classificações de forma organizada:
  - [ ] Seção "Personagens" (badges/tags)
  - [ ] Seção "Estrutura Narrativa" (lista)
  - [ ] Seção "Plot" (badge)
- [ ] Links para buscar contos com classificações similares

### Estilo
- [ ] Fundo neutro para reduzir fadiga visual
- [ ] Contraste adequado (WCAG AA)
- [ ] Transições suaves ao carregar

### Testes
- [ ] Testar leitura em diferentes dispositivos
- [ ] Verificar acessibilidade (contraste, hierarquia)
- [ ] Testar com contos de diferentes tamanhos
