from typing import Literal
from pydantic import BaseModel, Field
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from pathlib import Path
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langchain.tools import tool
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import JsonOutputParser
import json


# ====== MODELOS PYDANTIC PARA OUTPUT PARSING ======
class PersonagensOutput(BaseModel):
    """Modelo para a saída da listagem de personagens."""

    personagens: list[str] = Field(
        description="Lista de nomes dos personagens encontrados no conto"
    )


class ClassificacaoProppOutput(BaseModel):
    """Modelo para a saída da classificação de personagens segundo Propp."""

    classificacoes: dict[str, list[str]] = Field(
        description="Dicionário mapeando nome do personagem para lista de papéis de Propp"
    )
    justificativas: dict[str, dict[str, str]] = Field(
        description="Dicionário mapeando nome do personagem para dicionário de papel->justificativa"
    )


# ====== DEFINIÇÕES DE PROPP ======
PROPP_ROLES_DEFINITIONS = """
1. AGRESSOR (VILÃO): Causa o dano inicial ou a "falta" que inicia a história; entra em combate direto com o herói.
2. DOADOR (PROVEDOR): Testa o herói (interroga ou propõe desafio) e lhe fornece um objeto ou agente mágico.
3. AUXILIAR (AJUDANTE): Desloca o herói no espaço (voo, viagem rápida), resgata-o de perseguição, resolve tarefas difíceis ou transfigura o herói.
4. PRINCESA (E PAI): O objetivo da busca. O Pai atribui tarefas difíceis e entrega a Princesa. A Princesa é quem se casa com o herói.
5. MANDANTE: Aquele que percebe a falta e despacha o herói para a aventura (faz o chamado).
6. HERÓI: Aquele que parte na busca (buscador) ou sofre a agressão inicial (vítima) e reata a ela; casa-se no final.
7. FALSO HERÓI: Reivindica falsamente os feitos do herói ou tenta se casar com a princesa através de engano; geralmente é desmascarado.
"""


# ====== ESTADO DO GRAFO ======
class GraphState(TypedDict):
    conto: str
    personagens: list[str]
    classificacoes: dict
    justificativas: dict
    resultado_final: str


# ====== INICIALIZAR MODELO ======
def obter_modelo():
    """Inicializa o modelo de forma limpa."""
    return init_chat_model("gpt-4o-mini", model_provider="openai", temperature=0)


# ====== NÓS DO GRAFO ======
def node_listar_personagens(state: GraphState) -> GraphState:
    """Nó 1: Lista todos os personagens do conto."""
    print("\n📖 Etapa 1: Listando personagens...")

    model = obter_modelo()

    # Configurar o output parser
    parser = JsonOutputParser(pydantic_object=PersonagensOutput)

    prompt = f"""
Analise este conto e liste TODOS os personagens mencionados (nomes próprios ou descrições como "O Rei", "A Bruxa", etc).

Conto:
{state["conto"]}

{parser.get_format_instructions()}
"""

    # Criar chain com o parser
    chain = model | parser

    try:
        result = chain.invoke(prompt)
        state["personagens"] = result.get("personagens", [])
        print(f"✓ Personagens encontrados: {state['personagens']}")
    except Exception as e:
        print(f"⚠️  Falha ao parsear JSON: {e}")
        state["personagens"] = ["Personagem não identificado"]

    return state


def node_classificar_propp(state: GraphState) -> GraphState:
    """Nó 2: Classifica personagens segundo Propp."""
    print("\n🎭 Etapa 2: Classificando personagens segundo Propp...")

    model = obter_modelo()

    # Configurar o output parser
    parser = JsonOutputParser(pydantic_object=ClassificacaoProppOutput)

    personagens_str = ", ".join(state["personagens"])

    prompt = f"""
Você é um especialista em Narratologia.
Sua tarefa é analisar contos e classificar os personagens segundo as 7 Esferas de Ação de Vladimir Propp.

AS REGRAS DE PROPP:
{PROPP_ROLES_DEFINITIONS}

Nota: Um personagem pode ter múltiplos papéis.
Nota: Nem todos os papéis precisam estar presentes no conto.

Conto a analisar:
{state["conto"]}

Personagens para classificar: {personagens_str}

{parser.get_format_instructions()}
"""

    # Criar chain com o parser
    chain = model | parser

    try:
        result = chain.invoke(prompt)
        state["classificacoes"] = result.get("classificacoes", {})
        state["justificativas"] = result.get("justificativas", {})
        print("✓ Classificações concluídas")
    except Exception as e:
        print(f"⚠️  Erro ao parsear JSON: {e}")
        state["classificacoes"] = {p: [] for p in state["personagens"]}
        state["justificativas"] = {p: {} for p in state["personagens"]}

    return state


def node_formatar_resultado(state: GraphState) -> GraphState:
    """Nó 3: Formata o resultado final."""
    print("\n📊 Etapa 3: Formatando resultado...")

    resultado = "=" * 70 + "\n"
    resultado += "ANÁLISE NARRATOLÓGICA - ESFERAS DE AÇÃO DE VLADIMIR PROPP\n"
    resultado += "=" * 70 + "\n\n"

    for personagem in state["personagens"]:
        resultado += f"👤 {personagem.upper()}\n"
        resultado += "─" * 70 + "\n"

        papéis = state["classificacoes"].get(personagem, [])
        if papéis:
            resultado += "   Papéis atribuídos:\n"
            for papel in papéis:
                justificativa = (
                    state["justificativas"].get(personagem, {}).get(papel, "")
                )
                resultado += f"      • {papel}\n"
                if justificativa:
                    resultado += f"        └─ {justificativa}\n"
        else:
            resultado += "   ℹ️  Nenhum papel narrativo principal atribuído\n"

        resultado += "\n"

    state["resultado_final"] = resultado
    print("✓ Resultado formatado")

    return state


# ====== CONSTRUIR O GRAFO ======
def construir_grafo():
    """Constrói o grafo de análise narratológica."""

    graph = StateGraph(GraphState)

    # Adicionar nós
    graph.add_node("listar_personagens", node_listar_personagens)
    graph.add_node("classificar_propp", node_classificar_propp)
    graph.add_node("formatar_resultado", node_formatar_resultado)

    # Adicionar arestas (fluxo)
    graph.add_edge(START, "listar_personagens")
    graph.add_edge("listar_personagens", "classificar_propp")
    graph.add_edge("classificar_propp", "formatar_resultado")
    graph.add_edge("formatar_resultado", END)

    return graph.compile()


if __name__ == "__main__":
    from pathlib import Path

    file_path = Path.cwd() / "data" / "cinderela.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        cind = f.read()

    # Inicializar o grafo
    graph = construir_grafo()

    # Executar o grafo
    resultado = graph.invoke(
        {
            "conto": cind,
            "personagens": [],
            "classificacoes": {},
            "justificativas": {},
            "resultado_final": "",
        }
    )

    # Exibir resultado formatado
    print("\n" + resultado["resultado_final"])

    # Exibir dados estruturados em JSON
    print("\n📋 DADOS ESTRUTURADOS (JSON):")
    print(
        json.dumps(
            {
                "personagens": resultado["personagens"],
                "classificacoes": resultado["classificacoes"],
                "justificativas": resultado["justificativas"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
