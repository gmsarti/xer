import csv
import sqlite3
import ast
import json
import os
import sys

# Increase CSV field size limit for large text blobs
csv.field_size_limit(sys.maxsize)

CSV_PATH = "/home/gusarti/pessoal/code/xer/data/20260117_1900_contos_propp.csv"
DB_PATH = "/home/gusarti/pessoal/code/xer/data/contos_propp_v2.sqlite"
SCHEMA_PATH = "/home/gusarti/pessoal/code/xer/data/init_propp_db.sql"


def parse_list(val):
    if not val or val == "[]":
        return []
    try:
        return ast.literal_eval(val)
    except:
        return []


def migrate():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Initialize schema
    with open(SCHEMA_PATH, "r") as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)
    print("Schema initialized.")

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            # 1. Insert into tales
            cursor.execute(
                """
                INSERT INTO tales (url, author, source, region)
                VALUES (?, ?, ?, ?)
            """,
                (row["url"], row["author"], row["source"], row["region"]),
            )
            tale_id = cursor.lastrowid

            # 2. Insert into tale_translations (English)
            cursor.execute(
                """
                INSERT INTO tale_translations (
                    tale_id, language_code, title, story_body, moral, 
                    word_count, reading_time, flesch_reading_ease, dale_chall_readability
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    tale_id,
                    "en",
                    row["title"],
                    row["clean_text_EN"],
                    row["moral"],
                    row["word_count"],
                    row["reading_time"],
                    row["flesch_reading_ease"],
                    row["dale_chall_readability"],
                ),
            )

            # 3. Handle Tags
            tags_list = parse_list(row["tags"])
            for tag_name in tags_list:
                # Check if tag exists
                cursor.execute(
                    'SELECT tag_id FROM tag_translations WHERE name = ? AND language_code = "en"',
                    (tag_name,),
                )
                tag_row = cursor.fetchone()
                if tag_row:
                    tag_id = tag_row[0]
                else:
                    cursor.execute("INSERT INTO tags DEFAULT VALUES")
                    tag_id = cursor.lastrowid
                    cursor.execute(
                        "INSERT INTO tag_translations (tag_id, language_code, name) VALUES (?, ?, ?)",
                        (tag_id, "en", tag_name),
                    )

                # Link tag to tale
                cursor.execute(
                    "INSERT OR IGNORE INTO tale_tags (tale_id, tag_id) VALUES (?, ?)",
                    (tale_id, tag_id),
                )

            # 4. Handle Entities
            entities_list = parse_list(row["entities"])
            for entity_name in entities_list:
                cursor.execute(
                    "INSERT INTO entities (tale_id, type) VALUES (?, ?)",
                    (tale_id, "unknown"),
                )
                entity_id = cursor.lastrowid
                cursor.execute(
                    "INSERT INTO entity_translations (entity_id, language_code, name) VALUES (?, ?, ?)",
                    (entity_id, "en", entity_name),
                )

            # 5. Analysis Metadata
            cursor.execute(
                """
                INSERT INTO analysis_metadata (tale_id, image_prompt, voice_profile, mood)
                VALUES (?, ?, ?, ?)
            """,
                (tale_id, row["image_prompt"], row["voice_profile"], row["mood"]),
            )

            # 6. Booker Analysis
            cursor.execute(
                """
                INSERT INTO booker_analysis (tale_id, archetype, confidence, analysis)
                VALUES (?, ?, ?, ?)
            """,
                (
                    tale_id,
                    row["booker_archetype"],
                    row["booker_confidence"],
                    row["booker_analysis"],
                ),
            )

            # 7. Propp Analysis
            cursor.execute(
                """
                INSERT INTO propp_analysis (
                    tale_id, functions, sequence, type, notes, 
                    characters_list, characters_roles, characters_justification
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    tale_id,
                    row["propp_structure_functions"],
                    row["propp_structure_sequence"],
                    row["propp_structure_type"],
                    row["propp_structure_notes"],
                    row["propp_characters_list"],
                    row["propp_characters_roles"],
                    row["propp_characters_justification"],
                ),
            )

    conn.commit()
    conn.close()
    print(f"Migration completed. Database saved to {DB_PATH}")


if __name__ == "__main__":
    migrate()
