import sqlite3
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
from scipy.stats import chi2_contingency
import os

DB_PATH = "/home/gusarti/pessoal/code/xer/data/contos_propp_v2.sqlite"
PLOTS_DIR = "/home/gusarti/pessoal/code/xer/data/plots/insights"


def load_data():
    conn = sqlite3.connect(DB_PATH)
    # Load tales, their regional data, and their existing clusters
    query = """
    SELECT t.id as tale_id, t.region, t.author, p.functions, p.characters_roles, 
           r.cluster_id as main_cluster_id
    FROM tales t
    JOIN propp_analysis p ON t.id = p.tale_id
    JOIN propp_clustering_results r ON t.id = r.tale_id
    WHERE r.method = 'levenshtein'
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def parse_json(val):
    if not val or val == "[]":
        return []
    try:
        return json.loads(val)
    except:
        return []


def levenshtein_distance(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros((size_x, size_y))
    for x in range(size_x):
        matrix[x, 0] = x
    for y in range(size_y):
        matrix[0, y] = y
    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x - 1] == seq2[y - 1]:
                matrix[x, y] = matrix[x - 1, y - 1]
            else:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1, matrix[x - 1, y - 1] + 1, matrix[x, y - 1] + 1
                )
    return matrix[size_x - 1, size_y - 1]


def perform_subclustering(df):
    print(
        "\n--- Phase 1: Sub-clustering (Drill-down on largest Levenshtein cluster) ---"
    )
    # Identify the largest cluster
    largest_cluster_id = df["main_cluster_id"].value_counts().idxmax()
    sub_df = df[df["main_cluster_id"] == largest_cluster_id].copy()
    print(f"Drilling down into Cluster {largest_cluster_id} ({len(sub_df)} tales)...")

    # Compute Distance Matrix for sub-cluster
    n = len(sub_df)
    dist_matrix = np.zeros((n, n))
    sequences = [
        [item["simbolo"] for item in parse_json(f)] for f in sub_df["functions"]
    ]

    for i in range(n):
        for j in range(i + 1, n):
            d = levenshtein_distance(sequences[i], sequences[j])
            max_len = max(len(sequences[i]), len(sequences[j]))
            dist_matrix[i, j] = dist_matrix[j, i] = d / max_len if max_len > 0 else 0

    # Cluster
    best_k = 3
    clusterer = AgglomerativeClustering(
        n_clusters=best_k, metric="precomputed", linkage="complete"
    )
    sub_df["sub_cluster_id"] = clusterer.fit_predict(dist_matrix)

    # Save back to DB
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for tid, sub_id in zip(sub_df["tale_id"], sub_df["sub_cluster_id"]):
        cursor.execute(
            """
            INSERT OR REPLACE INTO propp_clustering_results (tale_id, method, cluster_id, score)
            VALUES (?, ?, ?, ?)
        """,
            (int(tid), f"levenshtein_sub_{largest_cluster_id}", int(sub_id), 0.0),
        )
    conn.commit()
    conn.close()
    print(f"Sub-clusters saved as 'levenshtein_sub_{largest_cluster_id}'.")
    return sub_df


def analyze_correlation(df):
    print("\n--- Phase 2: Correlation Analysis (Region vs Clusters) ---")
    # Clean regions (group rare ones into 'Other')
    df["region_clean"] = (
        df["region"]
        .fillna("Unknown")
        .apply(lambda x: x if df["region"].value_counts()[x] > 10 else "Other")
    )

    contingency = pd.crosstab(df["region_clean"], df["main_cluster_id"])
    chi2, p, dof, ex = chi2_contingency(contingency)
    print(f"Chi-squared Test (Region vs Levenshtein Clusters): p-value = {p:.4f}")

    plt.figure(figsize=(12, 6))
    sns.heatmap(contingency, annot=True, fmt="d", cmap="YlGnBu")
    plt.title("Heatmap: Region vs Levenshtein Clusters")
    plt.savefig(os.path.join(PLOTS_DIR, "correlation_region_heatmap.png"))
    print(f"Correlation plot saved to {PLOTS_DIR}")


def analyze_character_roles(df):
    print("\n--- Phase 3: Character Roles Analysis ---")
    role_data = []
    for idx, row in df.iterrows():
        roles = parse_json(row["characters_roles"])
        for role, name in roles.items():
            role_data.append({"cluster": row["main_cluster_id"], "role": role})

    roles_df = pd.DataFrame(role_data)
    if roles_df.empty:
        print("No character roles found.")
        return

    # Normalize counts per cluster
    pivot = pd.crosstab(roles_df["cluster"], roles_df["role"], normalize="index")

    pivot.plot(kind="bar", stacked=True, figsize=(12, 6), colormap="tab20")
    plt.title("Character Role Distribution by Levenshtein Cluster")
    plt.ylabel("Proportion")
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "character_roles_dist.png"))
    print(f"Character roles plot saved to {PLOTS_DIR}")


def generate_transition_graphs(df):
    print("\n--- Phase 4: Transition Graphs (Network Visualization) ---")
    import networkx as nx

    for cluster_id in df["main_cluster_id"].unique():
        cluster_df = df[df["main_cluster_id"] == cluster_id]
        G = nx.DiGraph()

        for functions_json in cluster_df["functions"]:
            symbols = [item["simbolo"] for item in parse_json(functions_json)]
            if len(symbols) < 2:
                continue
            for i in range(len(symbols) - 1):
                u, v = symbols[i], symbols[i + 1]
                if G.has_edge(u, v):
                    G[u][v]["weight"] += 1
                else:
                    G.add_edge(u, v, weight=1)

        # Plot top transitions
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(G, k=0.5)

        # Filter weak edges for clarity
        edges = [
            (u, v)
            for u, v, d in G.edges(data=True)
            if d["weight"] > len(cluster_df) * 0.1
        ]

        nx.draw_networkx_nodes(G, pos, node_size=700, node_color="skyblue")
        nx.draw_networkx_labels(G, pos)
        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=edges,
            width=[G[u][v]["weight"] * 0.1 for u, v in edges],
            arrowsize=20,
        )

        plt.title(f"Narrative Flow Graph - Cluster {cluster_id}")
        plt.savefig(
            os.path.join(PLOTS_DIR, f"transition_graph_cluster_{cluster_id}.png")
        )
        plt.close()
    print(f"Transition graphs saved to {PLOTS_DIR}")


def main():
    if not os.path.exists(PLOTS_DIR):
        os.makedirs(PLOTS_DIR)

    print("Loading data for advanced insights...")
    df = load_data()

    if df.empty:
        print("No data found to analyze.")
        return

    # Phase 1: Sub-clustering (Subgrafos)
    sub_df = perform_subclustering(df)

    # Phase 2: Correlation
    analyze_correlation(df)

    # Phase 3: Character Roles
    analyze_character_roles(df)

    # Phase 4: Transition Graphs (Grafos)
    generate_transition_graphs(df)

    print("\nAll insights generated successfully.")


if __name__ == "__main__":
    main()
