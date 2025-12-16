# Regras Customizadas do Projeto Xer

## Code Quality & Linting
- **NÃO faça correções automáticas de linting ou formatting**. Isso é responsabilidade exclusiva do Ruff. Se encontrar problemas de linting, apenas informe o usuário para rodar `uv run taskipy format` e `uv run taskipy lint`.
- Sempre escreva código seguindo as convenções Python modernas (Type Hints, docstrings quando apropriado).

## Documentação como Fonte da Verdade
- Sempre consulte `docs/principles.md` antes de fazer decisões de design ou arquitetura.
- Ao implementar features, siga `docs/user_stories.md` e os arquivos em `docs/tasks/` correspondentes.
- Ao fazer mudanças arquiteturais, valide contra `docs/implementation_plan.md`.
- Sempre atualize a documentação se fizer mudanças significativas.

## Design & Frontend
- Priorize **estética premium** e **"Wow Factor"** conforme `docs/principles.md`.
- Use Jinja2 para templates (server-side rendering).
- Use HTML, CSS e JavaScript puros para implementar a interface.
- CSS deve usar variáveis (custom properties) para consistência.
- Evite JavaScript desnecessário - progressive enhancement.

## Testes
- Funcionalidades críticas devem ter testes com pytest.
- Testes devem ser escritos de forma que possam ser executados em qualquer ambiente.
- Considere sempre a possibilidade de reaproveitar as configurações de testes.
- Não faça deploy sem testes passando.

## Workflows
- Use os workflows em `.agent/workflows/` para tarefas repetíveis:
  - `/implement-story` - Implementar uma user story
  - `/quality-check` - Rodar verificações de qualidade
  - `/test-suite` - Executar todos os testes
