import os
import getpass
import pandas as pd
from pathlib import Path
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from tqdm import tqdm
import time

# --- Configuration ---
INPUT_FILENAME = "20260115_1403_contos_metadados_basicos.csv"
OUTPUT_FILENAME = "20260117_1328_contos_classificados.csv"

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

# Paths - making them robust relative to the script location
# Assuming structure:
# project_root/
#   data/
#   scripts/process_tales_incremental.py
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
INPUT_PATH = DATA_DIR / INPUT_FILENAME
OUTPUT_PATH = DATA_DIR / OUTPUT_FILENAME


# --- Data Models ---
class StoryClassifications(BaseModel):
    """Extract classifications from story text for media/SEO."""

    image_prompt: str = Field(
        description="Vivid scene description for Midjourney/DALL-E cover image (50-100 words)."
    )
    voice_profile: str = Field(
        description="TTS voice suggestion like 'Old wise man', 'Cheerful child'."
    )
    mood: str = Field(
        description="Primary feeling for soundtrack: Terror, Epic, Melancholic, Joyful, etc."
    )
    tags: List[str] = Field(
        description="5-10 thematic keywords for SEO, comma-separated."
    )
    moral: str = Field(
        description="Core lesson/moral of the story (1 sentence, school-friendly)."
    )
    entities: List[str] = Field(
        description="Mythical creatures mentioned: Fadas, Goblins, Dragões, etc."
    )

    # Booker's 7 Plots
    booker_archetype: Literal[
        "Overcoming the Monster",
        "Rags to Riches",
        "The Quest",
        "Voyage and Return",
        "Comedy",
        "Tragedy",
        "Rebirth",
    ] = Field(
        description="The narrative archetype based on Christopher Booker's 7 Basic Plots."
    )
    booker_confidence: float = Field(
        description="Confidence level in the archetype classification (0.0 to 1.0)",
        ge=0.0,
        le=1.0,
    )
    booker_analysis: str = Field(
        description="Brief justification for the archetype classification."
    )


# --- LLM Setup ---
BOOKER_PLOTS_DESC = """
Classify the story into one of Christopher Booker's 7 Basic Plots:

1. **Overcoming the Monster**: Protagonist sets out to defeat an antagonistic force (human or beast) which threatens the protagonist and/or protagonist's homeland.
2. **Rags to Riches**: The poor protagonist acquires power, wealth, and/or a mate, loses it all and gains it back growing as a person as a result.
3. **The Quest**: The protagonist and some companions set out to acquire an important object or to get to a location, facing many obstacles and temptations along the way.
4. **Voyage and Return**: The protagonist goes to a strange land and, after overcoming the threats it poses to him or her, returns with nothing but experience.
5. **Comedy**: Light and humorous character with a happy or cheerful ending; a dramatic work in which the central motif is the triumph over adverse circumstance, resulting in a successful or happy conclusion.
6. **Tragedy**: The protagonist is a hero with one major character flaw or great mistake which is ultimately their undoing. Their unfortunate end evokes pity at their folly and the fall of a fundamentally 'good' character.
7. **Rebirth**: During the course of the story, an important event forces the main character to change their ways and often become a better person.
"""


def setup_chain():
    # Initialize the DeepSeek model
    # Note: Using `ChatDeepSeek` or standard OpenAI-compatible client if LangChain's specific integration varies.
    # The notebook used `init_chat_model("deepseek-chat", model_provider="deepseek", ...)`
    # Here we use a standard approach or the specific one if available.
    # Provided notebook code used `init_chat_model`, assuming we have recent langchain installed.
    # We will replicate the notebook's approach for compatibility.

    from langchain.chat_models import init_chat_model

    llm = init_chat_model("deepseek-chat", model_provider="deepseek", temperature=0)
    structured_llm = llm.with_structured_output(StoryClassifications)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                f"""Analyze this story text and extract ONLY the classifications in the exact schema format.
        Use `clean_text_EN` primarily, fall back to `title` if needed. Be precise and concise.
        
        {BOOKER_PLOTS_DESC}""",
            ),
            ("human", "{text}"),
        ]
    )

    return prompt | structured_llm


# --- Processing Logic ---
def classify_text(chain, text: str):
    """Invokes the chain for a single text."""
    if not text or not text.strip():
        return {f: "" for f in StoryClassifications.model_fields}, 0.0, 0, 0

    # Truncate to avoid context window issues just in case, though deepseek has large context
    short_text = text[:4000]

    try:
        result = chain.invoke({"text": short_text})

        # Calculate costs (approximate based on notebook provided values)
        input_tokens = 0
        output_tokens = 0
        total_cost_usd = 0.0

        if hasattr(result, "usage_metadata") and result.usage_metadata:
            # This depends on if 'usage_metadata' is populated on the Pydantic object
            # (usually it's on the message response, structured output might hide it).
            # If `with_structured_output` returns the Pydantic model directly, the metadata might be lost
            # unless we use include_raw=True, but let's stick to the notebook loop logic if possible.
            # In the notebook: `result.usage_metadata` was accessed.
            pass

        # NOTE: When using `with_structured_output`, the result is the Pydantic object.
        # To get usage, we often need to rely on callbacks or the response metadata if attached.
        # The notebook code checked `result.usage_metadata`, which implies the object returned
        # had that attribute attached by the specific langchain integration used.

        # We'll try to extract it safely
        usage = getattr(result, "usage_metadata", {}) or {}
        input_tokens = usage.get("input_tokens", 0)
        output_tokens = usage.get("output_tokens", 0)

        input_cost = input_tokens / 1e6 * 0.14
        output_cost = output_tokens / 1e6 * 0.28
        total_cost_usd = input_cost + output_cost

        return result.model_dump(), total_cost_usd, input_tokens, output_tokens

    except Exception as e:
        print(f"Error processing text: {e}")
        return {f: "" for f in StoryClassifications.model_fields}, 0.0, 0, 0


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
        # Read existing file to count processed rows
        # We assume the order matches exactly. To be safer, we could join on ID,
        # but for this script we will assume append-only integrity.
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

    # Setup LLM Chain
    print("Initializing LLM...")
    chain = setup_chain()

    # Define columns to add
    new_cols = list(StoryClassifications.model_fields.keys()) + [
        "classification_cost_usd",
        "input_tokens",
        "output_tokens",
    ]

    # Iterate and process
    print("Starting processing...")

    # We slice the dataframe to only process remaining rows
    df_to_process = df.iloc[start_index:].copy()

    # We will process row by row and append to CSV
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

        classifications, cost, in_tok, out_tok = classify_text(chain, str(text))

        # Update row with new data
        for key, value in classifications.items():
            row[key] = value
        row["classification_cost_usd"] = round(cost, 6)
        row["input_tokens"] = in_tok
        row["output_tokens"] = out_tok

        # Create a single-row DataFrame to append
        row_df = pd.DataFrame([row])

        # Append to CSV
        # We generally want to include all columns from the original DF plus the new ones.
        # Since we modified 'row' directly (which is a Series from the DF), it has all fields.
        # However, for the very first write (if mode='w'), we need to ensure the schema is stable.
        # If we are appending, the columns must match.

        # Careful: 'row' in iterrows doesn't preserve strict types always, but for CSV it's fine.
        # We should ensure the new columns exist in the row logic.

        # Save to file
        try:
            row_df.to_csv(OUTPUT_PATH, mode=mode, header=header, index=False)
        except Exception as e:
            print(f"Failed to save row {idx}: {e}")
            continue

        # After the first write, we are always appending and don't need header
        mode = "a"
        header = False

        # Optional: Sleep to Rate Limit if needed
        time.sleep(0.1)

    print("Processing complete.")


if __name__ == "__main__":
    main()
