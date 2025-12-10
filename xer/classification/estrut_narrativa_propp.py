import json
from pathlib import Path
from typing import Literal, TypedDict

from langchain.chat_models import init_chat_model
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

model = init_chat_model("gpt-4o-mini", model_provider="openai", temperature=0)

# ====== DEFINIÇÕES DAS 33 FUNÇÕES DE PROPP ======
PROPP_NARRATIVE_FUNCTIONS_SYSTEM_PROMPT = """

Você é um especialista em Narratologia e na teoria de Vladimir Propp.
Sua tarefa é analisar contos e identificar quais das 33 funções narrativas de Propp estão presentes.
As 33 Funções Narrativas de Vladimir Propp:
I. α - Situação Inicial: Apresentação do tempo, lugar e dos membros da família do futuro herói.
II. β - Afastamento: Um dos membros da família (ou o futuro herói) afasta-se de casa (partida, morte, etc.).
III. γ - Interdição: Uma proibição ou ordem é dirigida ao herói.
IV. δ - Transgressão: A proibição é violada (conduzindo ao conflito).
V. ε - Interrogatório: O agressor tenta obter informações sobre a vítima.
VI. ζ - Obtenção de Informação: O agressor recebe informações sobre a vítima.
VII. η - Engano (Truque): O agressor tenta enganar a vítima (disfarce, persuasão).
VIII. θ - Cumplicidade: A vítima (ingenuamente ou por erro) deixa-se enganar e ajuda o agressor.
IX. A - Dano/Malefício: O agressor causa algum prejuízo ou dano a um membro da família ou ao herói (o problema central do conto).
X. a - Carência: Falta algo (dinheiro, objeto mágico, noiva) ao herói. (Alternativa a A).
XI. B - Mediação: O herói toma conhecimento do dano ou carência, é procurado ou chamado para a reparação, ou é autorizado a partir.
XII. C - Início da Ação Contrária: O herói aceita ou decide reagir (ir em busca, etc.).
XIII. ↑ - Partida: O herói deixa a casa para cumprir sua missão.
XIV. D - Primeira Função do Doador: O herói é posto à prova, interrogado, atacado, etc., preparando-o para receber o meio mágico.
XV. E - Reação do Herói: O herói reage à prova do doador, sendo bem ou mal-sucedido.
XVI. F - Recepção do Objeto Mágico: O herói adquire ou recebe um objeto, animal ou auxiliar mágico (ou conselho).
XVII. G - Deslocamento/Transferência: O herói é transportado para o local do objeto de busca ou do agressor.
XVIII. H - Luta (Combate): O herói e o agressor enfrentam-se em combate direto.
XIX. I - Marca: O herói recebe uma marca no corpo, cicatriz ou um objeto identificador.
XX. J - Vitória: O agressor é derrotado (morto, expulso, aprisionado).
XXI. K - Reparação: O dano ou a carência inicial é reparada (o objeto é recuperado, o feitiço é quebrado).
XXII. ↓ - Regresso: O herói volta para casa.
XXIII. Pr - Perseguição: O herói é perseguido por um inimigo.
XXIV. Rs - Socorro: O herói é salvo da perseguição (fuga, disfarce, intervenção do auxiliar).
XXV. O - Chegada Incógnita: O herói chega em casa ou a outro país sem ser reconhecido.
XXVI. L - Pretensões Falsas: Um falso herói tenta ocupar o lugar do herói verdadeiro.
XXVII. M - Tarefa Difícil: Uma tarefa difícil é imposta ao herói (para provar sua identidade ou obter algo).
XXVIII. N - Solução: A tarefa difícil é realizada.
XXIX. Ex - Reconhecimento: O herói verdadeiro é reconhecido (pela marca, pelo objeto identificador ou pela solução da tarefa).
XXX. T - Desmascaramento: O falso herói ou agressor é desmascarado.
XXXI. U - Transfiguração: O herói recebe nova aparência (é curado, fica mais belo, recebe roupas novas).
XXXII. W - Punição: O agressor ou falso herói é punido.
XXXIII. Q - Casamento: O herói casa-se (e/ou ascende ao trono).
IMPORTANTE: Nem todas as funções precisam estar presentes em um conto.
As funções devem ser identificadas na ordem em que aparecem na narrativa.

Conto a analisar:
{state["conto"]}
Identifique TODAS as funções presentes no conto, na ordem em que aparecem.
Para cada função identificada, forneça:
1. O símbolo da função (ex: α, β, A, etc.)
2. O nome da função
3. Uma breve citação ou descrição do trecho do conto que exemplifica essa função
4. Uma justificativa de por que essa função está presente
Responda com um JSON exatamente neste formato:
{{
    "funcoes": [
        {{
            "simbolo": "α",
            "nome": "Situação Inicial",
            "trecho": "Era uma vez uma menina...",
            "justificativa": "Apresenta os personagens e o cenário inicial"
        }},
        {{
            "simbolo": "γ",
            "nome": "Interdição",
            "trecho": "A mãe disse: não fale com estranhos",
            "justificativa": "Uma proibição é dirigida ao herói"
        }}
    ]
}}
Responda APENAS com o JSON, sem nenhum texto adicional.
"""


# ====== ESTADO DO GRAFO ======
class GraphState(TypedDict):
    conto: str
    funcoes_identificadas: list[dict]
    sequencia_narrativa: str
    resultado_final: str


# Schema de resposta estruturada
class FunctionNarrPropp(BaseModel):
    """Classificação estruturada de um texto narrativo."""

    simbolo: Literal[
        "α",
        "β",
        "γ",
        "δ",
        "ε",
        "ζ",
        "η",
        "θ",
        "A",
        "a",
        "B",
        "C",
        "↑",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "↓",
        "Pr",
        "Rs",
        "O",
        "L",
        "M",
        "N",
        "Ex",
        "T",
        "U",
        "W",
        "Q",
    ] = Field(description="Categoria de enredo identificada")

    nome: Literal[
        "Situação Inicial",
        "Afastamento",
        "Interdição",
        "Transgressão",
        "Interrogatório",
        "Obtenção de Informação",
        "Engano (Truque)",
        "Cumplicidade",
        "Dano/Malefício",
        "Carência",
        "Mediação",
        "Início da Ação Contrária",
        "Partida",
        "Primeira Função do Doador",
        "Reação do Herói",
        "Recepção do Objeto Mágico",
        "Deslocamento/Transferência",
        "Luta (Combate)",
        "Marca",
        "Vitória",
        "Reparação",
        "Regresso",
        "Perseguição",
        "Socorro",
        "Chegada Incógnita",
        "Pretensões Falsas",
        "Tarefa Difícil",
        "Solução",
        "Reconhecimento",
        "Desmascaramento",
        "Transfiguração",
        "Punição",
        "Casamento",
    ] = Field(description="Categoria de enredo identificada")

    confianca: float = Field(
        description="Nível de confiança (0.0 a 1.0)", ge=0.0, le=1.0
    )

    arco_emocional: str = Field(description="Progressão emocional do arco narrativo")

    motivos_principais: list[str] = Field(
        description="Características estruturais encontradas no texto"
    )

    analise: str = Field(description="Justificativa detalhada da classificação")


class FunctionNarrProppList(BaseModel):
    funcoes: list[FunctionNarrPropp] = Field(description="Lista de funções narrativas")


# ====== HELPER FUNCTIONS ======


def clean_json_response(content: str) -> str:
    """Remove markdown code blocks from JSON responses."""
    content = content.strip()
    # Remove markdown code blocks
    if content.startswith("```"):
        # Find the first newline after ```json or ```
        first_newline = content.find("\n")
        # Find the last ```
        last_backticks = content.rfind("```")
        if first_newline != -1 and last_backticks != -1:
            content = content[first_newline + 1 : last_backticks].strip()
    return content


# ====== NÓS DO GRAFO ======
def node_identificar_funcoes(state: GraphState) -> GraphState:
    """Nó 1: Identifica as funções narrativas presentes no conto."""
    print("\n📖 Etapa 1: Identificando funções narrativas de Propp...")
    model = init_chat_model("gpt-4o-mini", model_provider="openai", temperature=0)
    prompt = PROPP_NARRATIVE_FUNCTIONS_SYSTEM_PROMPT
    response = model.invoke(prompt)
    cleaned_content = clean_json_response(response.content)
    try:
        result = json.loads(cleaned_content)
        state["funcoes_identificadas"] = result.get("funcoes", [])
    except json.JSONDecodeError as e:
        print(f"⚠️  Erro ao parsear JSON: {e}")
        print(f"📄 Resposta recebida (primeiros 500 chars):\n{response.content[:500]}")
        state["funcoes_identificadas"] = []
    print(f"✓ Funções identificadas: {len(state['funcoes_identificadas'])}")
    return state


def node_analisar_sequencia(state: GraphState) -> GraphState:
    """Nó 2: Analisa a sequência narrativa e padrões."""
    print("\n🔍 Etapa 2: Analisando sequência narrativa...")
    # Se não há funções identificadas, pular análise
    if not state["funcoes_identificadas"]:
        state["sequencia_narrativa"] = json.dumps(
            {
                "sequencia": "",
                "observacoes": "Nenhuma função foi identificada para análise",
                "tipo_conto": "Não classificado",
            },
            ensure_ascii=False,
            indent=2,
        )
        print("⚠️  Pulando análise - nenhuma função identificada")
        return state
    model = init_chat_model("gpt-4o-mini", model_provider="openai", temperature=0)
    funcoes_str = json.dumps(
        state["funcoes_identificadas"], ensure_ascii=False, indent=2
    )
    prompt = f"""
Você é um especialista em Narratologia.
Com base nas funções narrativas de Propp identificadas neste conto, faça uma análise da estrutura narrativa.
Funções identificadas:
{funcoes_str}
Forneça uma análise que inclua:
1. A sequência de símbolos das funções (ex: α-β-γ-δ-A-B-C-↑)
2. Observações sobre padrões narrativos (ex: presença de ciclos, funções ausentes importantes)
3. Classificação do tipo de conto baseado na estrutura (ex: conto de busca, conto de vitória sobre o agressor)
Responda com um JSON exatamente neste formato:
{{
    "sequencia": "α-β-γ-δ-A-B-C",
    "observacoes": "Este conto segue o padrão clássico...",
    "tipo_conto": "Conto de vitória sobre o agressor"
}}
Responda APENAS com o JSON, sem nenhum texto adicional.
"""
    response = model.invoke(prompt)
    cleaned_content = clean_json_response(response.content)
    try:
        result = json.loads(cleaned_content)
        state["sequencia_narrativa"] = json.dumps(result, ensure_ascii=False, indent=2)
    except json.JSONDecodeError as e:
        print(f"⚠️  Erro ao parsear JSON: {e}")
        print(f"📄 Resposta recebida (primeiros 500 chars):\n{response.content[:500]}")
        simbolos = [f["simbolo"] for f in state["funcoes_identificadas"]]
        state["sequencia_narrativa"] = json.dumps(
            {
                "sequencia": "-".join(simbolos),
                "observacoes": "Análise não disponível",
                "tipo_conto": "Não classificado",
            },
            ensure_ascii=False,
            indent=2,
        )
    print("✓ Análise de sequência concluída")
    return state


def node_formatar_resultado(state: GraphState) -> GraphState:
    """Nó 3: Formata o resultado final."""
    print("\n📊 Etapa 3: Formatando resultado...")
    resultado = "=" * 80 + "\n"
    resultado += "ANÁLISE NARRATOLÓGICA - 33 FUNÇÕES DE VLADIMIR PROPP\n"
    resultado += "=" * 80 + "\n\n"
    # Análise da sequência
    try:
        seq_data = json.loads(state["sequencia_narrativa"])
        resultado += "📈 ESTRUTURA NARRATIVA\n"
        resultado += "─" * 80 + "\n"
        resultado += f"   Sequência: {seq_data.get('sequencia', 'N/A')}\n"
        resultado += f"   Tipo de Conto: {seq_data.get('tipo_conto', 'N/A')}\n"
        resultado += f"   Observações: {seq_data.get('observacoes', 'N/A')}\n\n"
    except (json.JSONDecodeError, KeyError, TypeError):
        pass
    # Funções identificadas
    resultado += "📚 FUNÇÕES NARRATIVAS IDENTIFICADAS\n"
    resultado += "─" * 80 + "\n\n"
    for i, funcao in enumerate(state["funcoes_identificadas"], 1):
        resultado += f"{i}. {funcao.get('simbolo', '?')} - {funcao.get('nome', 'Desconhecida')}\n"
        resultado += f'   Trecho: "{funcao.get("trecho", "N/A")}"\n'
        resultado += f"   Justificativa: {funcao.get('justificativa', 'N/A')}\n\n"
    if not state["funcoes_identificadas"]:
        resultado += "   ℹ️  Nenhuma função narrativa foi identificada\n\n"
    state["resultado_final"] = resultado
    print("✓ Resultado formatado")
    return state


# ====== CONSTRUIR O GRAFO ======
def construir_grafo():
    """Constrói o grafo de análise narratológica."""
    graph = StateGraph(GraphState)
    # Adicionar nós
    graph.add_node("identificar_funcoes", node_identificar_funcoes)
    graph.add_node("analisar_sequencia", node_analisar_sequencia)
    graph.add_node("formatar_resultado", node_formatar_resultado)
    # Adicionar arestas (fluxo)
    graph.add_edge(START, "identificar_funcoes")
    graph.add_edge("identificar_funcoes", "analisar_sequencia")
    graph.add_edge("analisar_sequencia", "formatar_resultado")
    graph.add_edge("formatar_resultado", END)
    return graph.compile()


if __name__ == "__main__":
    from pathlib import Path

    file_path = Path.cwd() / "data" / "cinderela.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        cind = f.read()

    # Inicializar o grafo
    graph = construir_grafo()
    # # Executar o grafo
    # result = graph.run()
    # print(result)

    resultado = graph.invoke(
        {
            "conto": cind,
            "funcoes_identificadas": [],
            "sequencia_narrativa": "",
            "resultado_final": "",
        }
    )
    print("\n" + resultado["resultado_final"])
