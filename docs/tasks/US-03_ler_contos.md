# US-03: Ler Contos

**História**: Como leitor, quero uma experiência de leitura focada e confortável, para que eu possa ler contos sem distrações.

## Tarefas

### Backend
- [x] Criar função `get_tale(id)` em `xer/database.py`
- [x] Criar função `get_tale_classifications(tale_id)` para buscar metadados
- [x] Criar rota `GET /tales/{id}` em `main.py`

### Frontend
- [x] Criar template `xer/templates/tale.html`:
  - [x] Layout em 2 colunas (desktop) ou 1 coluna (mobile):
    - **Main**: Texto do conto
    - **Sidebar**: Metadados e classificações
  - [x] Tipografia otimizada:
    - [x] Line-height: ~1.6-1.8
    - [x] Measure (largura): ~65-75 caracteres
    - [x] Font-size: 18-20px
  - [x] Título do conto destacado
  - [x] Navegação:
    - [x] Botão "← Voltar"
    - [x] Links "Próximo/Anterior conto" (opcional)

### Sidebar de Metadados
- [ ] Exibir classificações de forma organizada:
  - [ ] Seção "Personagens" (badges/tags)
  - [ ] Seção "Estrutura Narrativa" (lista)
  - [ ] Seção "Plot" (badge)
- [ ] Links para buscar contos com classificações similares

### Estilo
- [x] Fundo neutro para reduzir fadiga visual
- [x] Contraste adequado (WCAG AA)
- [x] Transições suaves ao carregar

### Testes
- [x] Testar leitura em diferentes dispositivos
- [x] Verificar acessibilidade (contraste, hierarquia)
- [x] Testar com contos de diferentes tamanhos
