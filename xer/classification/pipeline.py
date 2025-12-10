"""
Pipeline de classificação de contos usando LangGraph.

Este pipeline recebe um conto e o processa através de:
1. Pré-processamento (passthrough por enquanto)
2. Classificadores em paralelo:
   - Personagens de Propp (7 Esferas de Ação)
   - Estrutura Narrativa de Propp (33 Funções)
   - 7 Plots de Booker
3. Agregação e persistência (a ser implementado)
"""

from typing import TypedDict, Any
from langgraph.graph import StateGraph, START, END


# ============================================================================
# ESTADO CENTRALIZADO DO PIPELINE
# ============================================================================
class PipelineState(TypedDict):
    """Estado compartilhado entre todos os nós do pipeline."""

    # Entrada
    conto: str
    conto_preprocessado: str

    # Resultados dos classificadores
    personagens_propp: dict[str, Any]  # {personagens, classificacoes, justificativas}
    estrutura_narrativa_propp: dict[
        str, Any
    ]  # {funcoes_identificadas, sequencia_narrativa}
    booker_7_plots: dict[
        str, Any
    ]  # {categoria, confianca, arco_emocional, motivos_principais, analise}

    # Status de conclusão de cada etapa
    status: dict[str, bool]


# ============================================================================
# NÓ DE PRÉ-PROCESSAMENTO
# ============================================================================
def node_preprocessar(state: PipelineState) -> dict:
    """
    Nó de pré-processamento do conto.

    Por enquanto, apenas passa o texto sem alterações.
    Futuramente: normalização, limpeza, tokenização, etc.
    """
    print("\n📝 Pré-processamento...")

    # Passthrough: apenas copia o conto para conto_preprocessado
    conto_preprocessado = state["conto"]

    print("✓ Pré-processamento concluído (passthrough)")

    return {
        "conto_preprocessado": conto_preprocessado,
        "status": {"preprocessado": True},
    }


# ============================================================================
# NÓS DE CLASSIFICAÇÃO (executados em paralelo)
# ============================================================================
def node_classificar_personagens_propp(state: PipelineState) -> dict:
    """
    Classifica personagens segundo as 7 Esferas de Ação de Propp.

    Utiliza o grafo definido em personagens_propp.py.
    """
    from personagens_propp import construir_grafo as construir_grafo_personagens

    print("\n👤 Classificador: Personagens de Propp...")

    # Construir e executar o grafo de personagens
    grafo = construir_grafo_personagens()

    resultado = grafo.invoke(
        {
            "conto": state["conto_preprocessado"],
            "personagens": [],
            "classificacoes": {},
            "justificativas": {},
            "resultado_final": "",
        }
    )

    print("✓ Classificação de personagens concluída")

    return {
        "personagens_propp": {
            "personagens": resultado["personagens"],
            "classificacoes": resultado["classificacoes"],
            "justificativas": resultado["justificativas"],
        },
        "status": {"personagens_propp": True},
    }


def node_classificar_estrutura_narrativa_propp(state: PipelineState) -> dict:
    """
    Identifica as 33 Funções Narrativas de Propp no conto.

    Utiliza o grafo definido em estrut_narrativa_propp.py.
    """
    from estrut_narrativa_propp import construir_grafo as construir_grafo_estrutura

    print("\n📖 Classificador: Estrutura Narrativa de Propp...")

    # Construir e executar o grafo de estrutura narrativa
    grafo = construir_grafo_estrutura()

    resultado = grafo.invoke(
        {
            "conto": state["conto_preprocessado"],
            "funcoes_identificadas": [],
            "sequencia_narrativa": "",
            "resultado_final": "",
        }
    )

    print("✓ Classificação de estrutura narrativa concluída")

    return {
        "estrutura_narrativa_propp": {
            "funcoes_identificadas": resultado["funcoes_identificadas"],
            "sequencia_narrativa": resultado["sequencia_narrativa"],
        },
        "status": {"estrutura_narrativa_propp": True},
    }


def node_classificar_booker_7_plots(state: PipelineState) -> dict:
    """
    Classifica o conto segundo os 7 Plots de Booker.

    Utiliza o agente definido em booker_7_plots.py.
    """
    from booker_7_plots import run_booker_7_plots_classification

    print("\n🎭 Classificador: 7 Plots de Booker...")

    # Executar o agente de classificação
    resultado = run_booker_7_plots_classification(state["conto_preprocessado"])

    # Extrair a resposta estruturada
    structured = resultado["structured_response"]

    print("✓ Classificação de 7 Plots concluída")

    return {
        "booker_7_plots": {
            "categoria": structured.categoria,
            "confianca": structured.confianca,
            "arco_emocional": structured.arco_emocional,
            "motivos_principais": structured.motivos_principais,
            "analise": structured.analise,
        },
        "status": {"booker_7_plots": True},
    }


# ============================================================================
# NÓ DE AGREGAÇÃO E PERSISTÊNCIA
# ============================================================================
def node_salvar_banco(state: PipelineState) -> dict:
    """
    Agrega os resultados e salva no banco de dados.

    Por enquanto, apenas imprime um resumo dos resultados.
    Futuramente: persistência em banco de dados.
    """
    print("\n💾 Salvando resultados...")

    # TODO: Implementar persistência no banco de dados
    # Por enquanto, apenas exibe um resumo

    print("\n" + "=" * 70)
    print("📊 RESUMO DOS RESULTADOS")
    print("=" * 70)

    # Personagens de Propp
    if state.get("personagens_propp"):
        pp = state["personagens_propp"]
        print(f"\n👤 Personagens encontrados: {len(pp.get('personagens', []))}")
        for p in pp.get("personagens", []):
            papeis = pp.get("classificacoes", {}).get(p, [])
            print(f"   • {p}: {', '.join(papeis) if papeis else 'sem papel definido'}")

    # Estrutura Narrativa de Propp
    if state.get("estrutura_narrativa_propp"):
        enp = state["estrutura_narrativa_propp"]
        funcoes = enp.get("funcoes_identificadas", [])
        print(f"\n📖 Funções narrativas identificadas: {len(funcoes)}")
        for f in funcoes[:5]:  # Mostrar apenas as 5 primeiras
            if isinstance(f, dict):
                print(f"   • {f.get('simbolo', '?')}: {f.get('nome', 'N/A')}")

    # 7 Plots de Booker
    if state.get("booker_7_plots"):
        b7p = state["booker_7_plots"]
        print(f"\n🎭 Categoria (Booker): {b7p.get('categoria', 'N/A')}")
        print(f"   Confiança: {b7p.get('confianca', 0):.0%}")
        print(f"   Arco emocional: {b7p.get('arco_emocional', 'N/A')}")

    print("\n" + "=" * 70)
    print("✓ Todos os dados processados!")

    return {"status": {"salvo": True}}


# ============================================================================
# CONSTRUÇÃO DO GRAFO (PIPELINE)
# ============================================================================
def criar_pipeline() -> StateGraph:
    """
    Constrói o pipeline de classificação de contos.

    Estrutura:
        START → preprocessar → [personagens_propp, estrutura_narrativa, booker_7_plots] → salvar → END

    Os 3 classificadores são executados em paralelo (fan-out/fan-in).
    """
    workflow = StateGraph(PipelineState)

    # Adicionar nós
    workflow.add_node("preprocessar", node_preprocessar)
    workflow.add_node("personagens_propp", node_classificar_personagens_propp)
    workflow.add_node("estrutura_narrativa", node_classificar_estrutura_narrativa_propp)
    workflow.add_node("booker_7_plots", node_classificar_booker_7_plots)
    workflow.add_node("salvar", node_salvar_banco)

    # Fan-out: pré-processamento → TODOS classificadores em PARALELO
    workflow.add_edge(START, "preprocessar")
    workflow.add_edge("preprocessar", "personagens_propp")
    workflow.add_edge("preprocessar", "estrutura_narrativa")
    workflow.add_edge("preprocessar", "booker_7_plots")

    # Fan-in: todos classificadores → salvar → fim
    workflow.add_edge("personagens_propp", "salvar")
    workflow.add_edge("estrutura_narrativa", "salvar")
    workflow.add_edge("booker_7_plots", "salvar")
    workflow.add_edge("salvar", END)

    return workflow.compile()


# ============================================================================
# FUNÇÃO PRINCIPAL DE EXECUÇÃO
# ============================================================================
def executar_pipeline(conto: str) -> PipelineState:
    """
    Executa o pipeline completo de classificação de contos.

    Args:
        conto: Texto do conto a ser classificado.

    Returns:
        Estado final do pipeline com todos os resultados.
    """
    pipeline = criar_pipeline()

    estado_inicial: PipelineState = {
        "conto": conto,
        "conto_preprocessado": "",
        "personagens_propp": {},
        "estrutura_narrativa_propp": {},
        "booker_7_plots": {},
        "status": {},
    }

    return pipeline.invoke(estado_inicial)


# ============================================================================
# EXECUÇÃO DIRETA (para testes)
# ============================================================================
if __name__ == "__main__":
    from pathlib import Path

    # Carregar conto de exemplo
    file_path = Path.cwd() / "data" / "cinderela.txt"

    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            conto = f.read()
    else:
        conto = """
        Era uma vez uma jovem chamada Cinderela que vivia com sua madrasta malvada
        e suas duas irmãs invejosas. Um dia, o príncipe do reino anunciou um grande
        baile para encontrar uma esposa. Com a ajuda de sua fada madrinha, Cinderela
        foi ao baile, encantou o príncipe, mas teve que fugir à meia-noite, deixando
        para trás apenas um sapatinho de cristal. O príncipe procurou por todo o
        reino até encontrar Cinderela, e eles viveram felizes para sempre.
        """

    print("🏰 Iniciando Pipeline de Classificação de Contos")
    print("=" * 70)

    resultado = executar_pipeline(conto)

    print("\n✅ Pipeline executado com sucesso!")
