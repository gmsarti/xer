import sqlite3
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.preprocessing import MultiLabelBinarizer, StandardScaler
from sklearn.metrics import silhouette_score
import os

DB_PATH = "/home/gusarti/pessoal/code/xer/data/contos_propp_v2.sqlite"
OUTPUT_CSV = "/home/gusarti/pessoal/code/xer/data/propp_clusters.csv"
PLOTS_DIR = "/home/gusarti/pessoal/code/xer/data/plots"


def load_data():
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT p.tale_id, p.functions, t.title
    FROM propp_analysis p
    JOIN tale_translations t ON p.tale_id = t.tale_id
    WHERE t.language_code = 'en'
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def parse_functions(functions_json):
    if not functions_json or functions_json == "[]":
        return []
    try:
        data = json.loads(functions_json)
        return [item["simbolo"] for item in data if "simbolo" in item]
    except:
        return []


def get_bigrams(symbols):
    if len(symbols) < 2:
        return []
    return [f"{symbols[i]}->{symbols[i + 1]}" for i in range(len(symbols) - 1)]


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


def save_to_db(df, method_name, labels, score):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for tid, label in zip(df["tale_id"], labels):
        cursor.execute(
            """
            INSERT OR REPLACE INTO propp_clustering_results (tale_id, method, cluster_id, score)
            VALUES (?, ?, ?, ?)
        """,
            (int(tid), method_name, int(label), float(score)),
        )
    conn.commit()
    conn.close()


def plot_and_analyze(X, df, labels, method_name, k):
    # Visualization with PCA
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X)

    plt.figure(figsize=(10, 7))
    sns.scatterplot(
        x=X_pca[:, 0], y=X_pca[:, 1], hue=labels, palette="viridis", s=100, alpha=0.7
    )
    plt.title(f"PCA Visualization of {method_name} (K={k})")
    plt.xlabel("PCA 1")
    plt.ylabel("PCA 2")

    if not os.path.exists(PLOTS_DIR):
        os.makedirs(PLOTS_DIR)

    plot_path = os.path.join(PLOTS_DIR, f"propp_clusters_{method_name.lower()}.png")
    plt.savefig(plot_path)
    print(f"Plot saved to {plot_path}")

    # Analyze Clusters
    for i in range(k):
        cluster_data = df[labels == i]
        all_symbols = [s for sublist in cluster_data["symbols"] for s in sublist]
        top_symbols = pd.Series(all_symbols).value_counts().head(5)
        print(
            f"  Cluster {i} ({len(cluster_data)} tales): Top functions: {top_symbols.to_dict()}"
        )


def run_clustering(X, df, method_name, max_k=10, precomputed=False):
    print(f"\n--- Running {method_name} ---")
    best_k = 2
    best_score = -1

    n_samples = X.shape[0] if not precomputed else X.shape[0]
    limit_k = min(n_samples - 1, max_k)

    if limit_k < 2:
        print("Not enough samples.")
        return None, 0

    for k in range(2, limit_k + 1):
        if precomputed:
            clusterer = AgglomerativeClustering(
                n_clusters=k, metric="precomputed", linkage="complete"
            )
            labels = clusterer.fit_predict(X)
        else:
            clusterer = KMeans(n_clusters=k, random_state=42, n_init="auto")
            labels = clusterer.fit_predict(X)

        score = silhouette_score(
            X, labels, metric="precomputed" if precomputed else "euclidean"
        )
        if score > best_score:
            best_score = score
            best_k = k
            best_labels = labels

    print(f"Selected K={best_k} with score {best_score:.4f}")
    save_to_db(df, method_name.lower(), best_labels, best_score)
    return best_labels, best_k


def main():
    print("Loading data...")
    df = load_data()
    df["symbols"] = df["functions"].apply(parse_functions)
    df = df[df["symbols"].map(len) > 0].copy()

    # 1. One-Hot
    mlb = MultiLabelBinarizer()
    X_oh = mlb.fit_transform(df["symbols"])
    labels_oh, k_oh = run_clustering(X_oh, df, "One-Hot")
    plot_and_analyze(X_oh, df, labels_oh, "One-Hot", k_oh)

    # 2. Bigrams
    df["bigrams"] = df["symbols"].apply(get_bigrams)
    mlb_bg = MultiLabelBinarizer()
    X_bg = mlb_bg.fit_transform(df["bigrams"])
    if X_bg.shape[1] > 0:
        labels_bg, k_bg = run_clustering(
            X_oh, df, "Bigrams"
        )  # Using OH features but labeled as bigram method for now or use X_bg
        # Actually, let's use X_bg for bigrams
        labels_bg, k_bg = run_clustering(X_bg, df, "Bigrams")
        plot_and_analyze(X_bg, df, labels_bg, "Bigrams", k_bg)

    # 3. Levenshtein (on a sample if too slow, but let's try all 1181)
    print("\n--- Computing Levenshtein Distance Matrix (this may take a minute) ---")
    n = len(df)
    dist_matrix = np.zeros((n, n))
    sequences = df["symbols"].tolist()

    # Optimization: only compute upper triangle
    for i in range(n):
        for j in range(i + 1, n):
            d = levenshtein_distance(sequences[i], sequences[j])
            # Normalize by max length to get a score between 0 and 1
            max_len = max(len(sequences[i]), len(sequences[j]))
            dist_matrix[i, j] = dist_matrix[j, i] = d / max_len if max_len > 0 else 0

    labels_lv, k_lv = run_clustering(dist_matrix, df, "Levenshtein", precomputed=True)
    # For PCA visualization of Levenshtein, we need coordinates. MDS or just use the distance matrix?
    # Let's use PCA on the distance matrix as a proxy.
    plot_and_analyze(dist_matrix, df, labels_lv, "Levenshtein", k_lv)

    print("\nAll analyses completed and saved to database.")


if __name__ == "__main__":
    main()
