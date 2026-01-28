from typing import Literal

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field

# Crie o agente com output estruturado
model = init_chat_model("gpt-4.1")


# Schema de resposta estruturada
class PlotClassification(BaseModel):
    """Classificação estruturada de um texto narrativo."""

    categoria: Literal[
        "vencendo_o_monstro",
        "cinzas_riqueza",
        "busca",
        "viagem_retorno",
        "comedia",
        "tragedia",
        "renascimento",
    ] = Field(description="Categoria de enredo identificada")

    confianca: float = Field(
        description="Nível de confiança (0.0 a 1.0)", ge=0.0, le=1.0
    )

    arco_emocional: str = Field(description="Progressão emocional do arco narrativo")

    motivos_principais: list[str] = Field(
        description="Características estruturais encontradas no texto"
    )

    analise: str = Field(description="Justificativa detalhada da classificação")


BOOKER_7_PLOTS_SYSTEM_PROMPT = """
Você é um especialista em análise de estrutura narrativa literária.
Sua tarefa é classificar textos (histórias, contos, poemas) em uma de 7 categorias de arquétipos de enredo.


1. **Vencendo o Monstro**: Conflito contra antagonista (literal ou abstrato) que ameaça existência. 
   Arco: Medo → Coragem → Triunfo
   Exemplos: Beowulf, Tubarão, Star Wars, Harry Potter

2. **Das Cinzas à Riqueza**: Ascensão de personagem humilde. Perde cedo o sucesso, depois recupera por mérito próprio.
   Arco: Humildade → Sucesso → Perda → Maturidade
   Exemplos: Cinderela, Aladdin, Slumdog Millionaire

3. **A Busca**: Jornada em grupo para adquirir objeto ou chegar a local. Foco na transformação interna.
   Arco: Determinação → Provação → Conquista
   Exemplos: O Senhor dos Anéis, Indiana Jones, Procurando Nemo

4. **Viagem e Retorno**: Transporte para mundo bizarro com leis diferentes. Objetivo é escapar e voltar com nova perspectiva.
   Arco: Curiosidade → Medo → Alívio
   Exemplos: Alice no País das Maravilhas, O Mágico de Oz, A Viagem de Chihiro

5. **Comédia**: Mal-entendidos/confusões impedem felicidade. Passa de confusão para ordem através do reconhecimento da verdade.
   Arco: Confusão → Esclarecimento → Harmonia
   Exemplos: Sonho de uma Noite de Verão, O Diário de Bridget Jones

6. **Tragédia**: Herói destruído por defeito fatal de caráter. Espiral descendente leva à morte/destruição e catarse.
   Arco: Ambição → Culpa → Destruição
   Exemplos: Macbeth, Breaking Bad, O Grande Gatsby

7. **Renascimento**: Herói sob feitiço (vício/amargura) precisa ser libertado. Figura de redenção ajuda. Mudança do inverno para primavera.
   Arco: Escuridão → Arrependimento → Luz
   Exemplos: Um Conto de Natal, A Bela e a Fera, O Grinch

Ao analisar um texto:
1. Identifique o conflito central e o arco emocional
2. Procure por características estruturais-chave (ex: o herói é destruído? Há uma jornada em grupo? Confusão sendo resolvida?)
3. Compare com exemplos da categoria
4. Retorne a classificação estruturada com confiança e justificativa

Seja preciso e forneça análise textual que respalda sua classificação.
"""

booker_7_plots_classification_agent = create_agent(
    model=model,
    tools=[],  # Sem ferramentas externas, apenas análise do LLM
    response_format=PlotClassification,
    system_prompt=BOOKER_7_PLOTS_SYSTEM_PROMPT,
)


def run_booker_7_plots_classification(text):
    return booker_7_plots_classification_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"""Por favor, classifique este texto:

---
{text}
---

Analise sua estrutura narrativa e retorne a classificação estruturada.""",
                }
            ]
        }
    )


if __name__ == "__main__":
    from pathlib import Path

    file_path = Path.cwd() / "data" / "cinderela.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        cind = f.read()

    # Use o agente
    resultado = run_booker_7_plots_classification(cind)

    print(f"Categoria: {resultado['structured_response'].categoria}")
    print(f"Arco emocional: {resultado['structured_response'].arco_emocional}")
    print(f"Motivos principais: {resultado['structured_response'].motivos_principais}")
    print(f"Confiança: {resultado['structured_response'].confianca}")
    print(f"Análise: {resultado['structured_response'].analise}")

    print("Custo de execução: ", resultado["cost"])
