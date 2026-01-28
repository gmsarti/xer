# Princípios do Projeto

Este documento estabelece os pilares fundamentais que guiam o desenvolvimento, design e evolução do projeto **Xer**.

## 1. Experiência do Usuário & Design
> **"First Impressions Matter."**

- **Estética Premium ("Wow Factor")**: O design não deve ser apenas funcional, mas encantar. Utilizamos paletas de cores harmoniosas, tipografia moderna e layouts limpos. Evitamos o "básico" ou "genérico".
- **Interface Viva**: A interface deve parecer responsiva e viva. Micro-interações, estados de hover e transições suaves são essenciais, não opcionais.
- **Leitura Imersiva**: Como um site de contos, a tipografia e o espaçamento devem garantir uma experiência de leitura confortável e engajante.

## 2. Filosofia Técnica
> **"Simple is better than complex."**

- **Arquitetura Pragmática**: Escolhemos a ferramenta certa para o estágio atual. Jinja2 + Server-Side Rendering (SSR) nos dá velocidade de desenvolvimento e SEO imediato sem a complexidade de um SPA neste momento.
- **SEO por Padrão**: Sendo um arquivo de conteúdo, a indexabilidade é crítica. Semântica HTML, meta tags e performance são prioridade.
- **Pythonic Core**: O backend segue as convenções modernas de Python (Type Hints, Pydantic, Ruff para linting). Código limpo e legível é mandato.
- **Resource Management**: Sempre use context managers (`with` statement) para gerenciar recursos como conexões de banco de dados, arquivos, etc. Isso garante que recursos sejam sempre liberados corretamente, mesmo em caso de exceções.

## 3. Qualidade & Manutenibilidade
- **Testes Automatizados**: Funcionalidades críticas devem ter testes. Confiança no deploy vem de uma suite de testes verde.
- **Documentação Viva**: Mantemos a documentação próxima ao código e atualizada. Se a arquitetura muda, a documentação muda junto.

## 4. Evolução do Produto
- **Iteração Rápida**: Lançamos o MVP (Minimum Viable Product) polido, mas focado no core (busca e leitura), e expandimos baseado em feedback.
- **Performance First**: O site deve carregar instantaneamente. Otimização de assets e queries eficientes são parte do desenvolvimento, não uma etapa final.
