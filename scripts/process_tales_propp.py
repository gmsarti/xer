import sys
import os
import getpass
import pandas as pd
import json
import time
from pathlib import Path
from tqdm import tqdm

# --- Path Setup ---
# Add project root to sys.path to allow importing 'xer'
# Assuming script is in <project_root>/scripts/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

try:
    from xer.classification.estrut_narrativa_propp import (
        construir_grafo as build_structure_graph,
    )
    from xer.classification.personagens_propp import (
        construir_grafo as build_character_graph,
    )
except ImportError as e:
    print(f"Error importing xer modules: {e}")
    print("Ensure you are running from the project root or 'xer' is in python path.")
    sys.exit(1)

# --- Configuration ---
INPUT_FILENAME = "20260117_1328_contos_classificados.csv"
OUTPUT_FILENAME = "20260117_1900_contos_propp.csv"

# Ensure we have the API key
print("Checking environment variables...")
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

if not os.environ.get("DEEPSEEK_API_KEY"):
    print("ERROR: DEEPSEEK_API_KEY environment variable not set.")
    print("Please set it in your environment or a .env file.")
    # Option to input manually
    key_input = getpass.getpass(
        "Or enter API key for DeepSeek now (leave empty to exit): "
    )
    if key_input.strip():
        os.environ["DEEPSEEK_API_KEY"] = key_input.strip()
    else:
        print("Exiting...")
        exit(1)

# Paths
DATA_DIR = PROJECT_ROOT / "data"
INPUT_PATH = DATA_DIR / INPUT_FILENAME
OUTPUT_PATH = DATA_DIR / OUTPUT_FILENAME


def process_row(structure_graph, character_graph, text: str):
    """Processes a single text through both Propp graphs."""

    if not text or not text.strip():
        return {}, {}

    # 1. Structure Analysis
    try:
        struct_inputs = {
            "conto": text,
            "funcoes_identificadas": [],
            "sequencia_narrativa": "",
            "resultado_final": "",
        }
        struct_result = structure_graph.invoke(struct_inputs)

        # Parse output
        funcoes = struct_result.get("funcoes_identificadas", [])
        sequencia_raw = struct_result.get("sequencia_narrativa", "{}")

        # Try to parse sequence JSON if it's a string, or keep as is if dict (invoke might return state dicts)
        if isinstance(sequencia_raw, str):
            try:
                sequencia_data = json.loads(sequencia_raw)
            except json.JSONDecodeError:
                sequencia_data = {
                    "sequencia": "",
                    "tipo_conto": "Erro parse",
                    "observacoes": str(sequencia_raw),
                }
        else:
            sequencia_data = sequencia_raw

        structure_data = {
            "propp_structure_functions": json.dumps(funcoes, ensure_ascii=False),
            "propp_structure_sequence": sequencia_data.get("sequencia", ""),
            "propp_structure_type": sequencia_data.get("tipo_conto", ""),
            "propp_structure_notes": sequencia_data.get("observacoes", ""),
        }
    except Exception as e:
        print(f"Error in structure analysis: {e}")
        structure_data = {
            "propp_structure_functions": "[]",
            "propp_structure_sequence": "ERROR",
            "propp_structure_type": "ERROR",
            "propp_structure_notes": str(e),
        }

    # 2. Character Analysis
    try:
        char_inputs = {
            "conto": text,
            "personagens": [],
            "classificacoes": {},
            "justificativas": {},
            "resultado_final": "",
        }
        char_result = character_graph.invoke(char_inputs)

        roles = char_result.get("classificacoes", {})
        justifications = char_result.get("justificativas", {})
        characters = char_result.get("personagens", [])

        character_data = {
            "propp_characters_list": json.dumps(characters, ensure_ascii=False),
            "propp_characters_roles": json.dumps(roles, ensure_ascii=False),
            "propp_characters_justification": json.dumps(
                justifications, ensure_ascii=False
            ),
        }
    except Exception as e:
        print(f"Error in character analysis: {e}")
        character_data = {
            "propp_characters_list": "[]",
            "propp_characters_roles": "{}",
            "propp_characters_justification": "{}",
        }

    return structure_data, character_data


def main():
    print(f"Loading data from {INPUT_PATH}...")
    if not INPUT_PATH.exists():
        print(f"Error: Input file not found at {INPUT_PATH}")
        return

    df = pd.read_csv(INPUT_PATH)
    total_rows = len(df)
    print(f"Found {total_rows} rows to process.")

    # Check for existing output to resume
    start_index = 0
    mode = "w"
    header = True

    if OUTPUT_PATH.exists():
        print(f"Output file found at {OUTPUT_PATH}. Resuming...")
        try:
            df_existing = pd.read_csv(OUTPUT_PATH)
            start_index = len(df_existing)
            mode = "a"
            header = False
            print(f"Resuming from index {start_index}")
        except Exception as e:
            print(f"Could not read existing output file: {e}. Starting fresh.")

    if start_index >= total_rows:
        print("All rows already processed.")
        return

    # Initialize Graphs
    print("Initializing Propp Graphs (this may take a moment)...")
    structure_graph = build_structure_graph()
    character_graph = build_character_graph()

    # Iterate and process
    print("Starting processing...")

    df_to_process = df.iloc[start_index:].copy()

    for idx, row in tqdm(
        df_to_process.iterrows(),
        total=len(df_to_process),
        initial=start_index,
        unit="story",
    ):
        text = (
            row.get("clean_text_EN", "")
            or row.get("full_text_EN", "")
            or row.get("title", "")
        )

        struct_data, char_data = process_row(
            structure_graph, character_graph, str(text)
        )

        # Update row with new data
        for key, value in struct_data.items():
            row[key] = value
        for key, value in char_data.items():
            row[key] = value

        row_df = pd.DataFrame([row])

        try:
            row_df.to_csv(OUTPUT_PATH, mode=mode, header=header, index=False)
        except Exception as e:
            print(f"Failed to save row {idx}: {e}")
            continue

        mode = "a"
        header = False

        # Optional sleep
        # time.sleep(0.1)

    print(f"Processing complete. Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
