import sqlite3
import re
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'contos.sqlite')

# Ensure path is correct (relative to this script location)
if not os.path.isfile(DB_PATH):
    raise FileNotFoundError(f"Database not found at {DB_PATH}")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Helper to get or create classification id
def get_or_create_classification(name, framework, description=None):
    cur.execute("SELECT classificacao_id FROM classificacoes WHERE nome_classificacao = ? AND framework = ?", (name, framework))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute(
        "INSERT INTO classificacoes (nome_classificacao, framework, descricao) VALUES (?,?,?)",
        (name, framework, description),
    )
    return cur.lastrowid

# 1️⃣ Classify ATU from URL (pattern typeXXXX.html -> ATU XXXX)
atu_pattern = re.compile(r"type(\d{3,4})\.html", re.IGNORECASE)
cur.execute("SELECT id, url FROM tales")
for tale_id, url in cur.fetchall():
    match = atu_pattern.search(url)
    if match:
        atu_num = match.group(1)
        atu_name = f"ATU {atu_num}"
        class_id = get_or_create_classification(atu_name, "ATU")
        # link if not already linked
        cur.execute(
            "SELECT 1 FROM conto_classificacao WHERE conto_id = ? AND classificacao_id = ?",
            (tale_id, class_id),
        )
        if not cur.fetchone():
            cur.execute(
                "INSERT INTO conto_classificacao (conto_id, classificacao_id) VALUES (?,?)",
                (tale_id, class_id),
            )

# 2️⃣ Simple Booker classification based on title keywords
booker_rules = [
    (re.compile(r"chapeuzinho|lobo|ferro|lobo mau", re.IGNORECASE), "Superando o Monstro"),
    (re.compile(r"cinderela|fada madrinha|sapato", re.IGNORECASE), "De Pobre a Rico"),
    (re.compile(r"viagem|caminho|rota|journey", re.IGNORECASE), "Viagem e Retorno"),
    (re.compile(r"princesa|resgate|salvo", re.IGNORECASE), "Renascimento"),
]
cur.execute("SELECT id, titulo FROM tales")
for tale_id, titulo in cur.fetchall():
    for pattern, booker_name in booker_rules:
        if pattern.search(titulo):
            class_id = get_or_create_classification(booker_name, "Booker")
            cur.execute(
                "SELECT 1 FROM conto_classificacao WHERE conto_id = ? AND classificacao_id = ?",
                (tale_id, class_id),
            )
            if not cur.fetchone():
                cur.execute(
                    "INSERT INTO conto_classificacao (conto_id, classificacao_id) VALUES (?,?)",
                    (tale_id, class_id),
                )
            break  # assign first matching Booker category

# 3️⃣ Propp role classification (very simple keyword based)
propp_rules = [
    (re.compile(r"lobo|vilão|agressor|bruxa", re.IGNORECASE), "Vilão"),
    (re.compile(r"herói|filho|enteada|príncipe|princesa", re.IGNORECASE), "Herói"),
    (re.compile(r"doador|item mágico|velha", re.IGNORECASE), "Doador"),
    (re.compile(r"auxiliar|fada madrinha|animais falantes", re.IGNORECASE), "Auxiliar"),
]
cur.execute("SELECT id, titulo FROM tales")
for tale_id, titulo in cur.fetchall():
    for pattern, role in propp_rules:
        if pattern.search(titulo):
            class_id = get_or_create_classification(role, "Propp_Papel")
            cur.execute(
                "SELECT 1 FROM conto_classificacao WHERE conto_id = ? AND classificacao_id = ?",
                (tale_id, class_id),
            )
            if not cur.fetchone():
                cur.execute(
                    "INSERT INTO conto_classificacao (conto_id, classificacao_id) VALUES (?,?)",
                    (tale_id, class_id),
                )
            # continue checking for other possible roles

conn.commit()
conn.close()
print("Classification completed.")
