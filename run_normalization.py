#!/usr/bin/env python3
"""
Script para aplicar normalização de origens ao CSV de contos.
"""

import pandas as pd
import sys
from pathlib import Path

# Importar funções de normalização
from normalize_origins import (
    normalize_origin,
    apply_normalization,
    analyze_normalization,
)


def main():
    # Caminhos
    input_file = Path("/home/gusarti/pessoal/code/xer/data/contos_semi_limpos.csv")
    output_file = Path("/home/gusarti/pessoal/code/xer/data/contos_normalizados.csv")

    print("=" * 70)
    print("NORMALIZAÇÃO DE ORIGENS - CONTOS")
    print("=" * 70)
    print(f"\nArquivo de entrada: {input_file}")
    print(f"Arquivo de saída: {output_file}")

    # Verificar se arquivo existe
    if not input_file.exists():
        print(f"\n❌ ERRO: Arquivo não encontrado: {input_file}")
        sys.exit(1)

    # Carregar CSV
    print("\n[1/4] Carregando CSV...")
    df = pd.read_csv(input_file)
    print(f"   ✓ Carregadas {len(df)} linhas")
    print(f"   ✓ Colunas: {', '.join(df.columns.tolist())}")

    # Verificar se coluna 'origem' existe
    if "origem" not in df.columns:
        print(f"\n❌ ERRO: Coluna 'origem' não encontrada no CSV")
        print(f"   Colunas disponíveis: {', '.join(df.columns.tolist())}")
        sys.exit(1)

    # Aplicar normalização
    print("\n[2/4] Aplicando normalização...")
    df_normalized = apply_normalization(
        df, column="origem", new_column="origem_normalizada"
    )
    print(f"   ✓ Nova coluna 'origem_normalizada' criada")

    # Analisar resultados
    print("\n[3/4] Analisando resultados...")
    stats = analyze_normalization(df_normalized)

    print(f"\n{'=' * 70}")
    print("ESTATÍSTICAS DE NORMALIZAÇÃO")
    print(f"{'=' * 70}")
    print(f"Valores únicos originais:     {stats['unique_original']:>6}")
    print(f"Valores únicos normalizados:  {stats['unique_normalized']:>6}")
    print(f"Cobertura (% mapeados):       {stats['coverage']:>6.2f}%")
    print(f"Valores não mapeados:         {stats['unmapped_count']:>6}")
    print(f"Valores desconhecidos:        {stats['unknown_count']:>6}")

    # Mostrar top 20 países
    print(f"\n{'=' * 70}")
    print("TOP 20 PAÍSES/REGIÕES")
    print(f"{'=' * 70}")
    for country, count in stats["distribution"].head(20).items():
        print(f"{country:40} {count:>6}")

    # Mostrar valores não mapeados se houver
    if stats["unmapped_count"] > 0:
        print(f"\n{'=' * 70}")
        print(f"VALORES NÃO MAPEADOS ({len(stats['unmapped_values'])} únicos)")
        print(f"{'=' * 70}")
        for val in sorted(stats["unmapped_values"])[:30]:  # Mostrar primeiros 30
            print(f"  - {val}")
        if len(stats["unmapped_values"]) > 30:
            print(f"  ... e mais {len(stats['unmapped_values']) - 30} valores")

    # Mostrar valores Unknown se houver
    if stats["unknown_count"] > 0:
        print(f"\n{'=' * 70}")
        print(
            f"VALORES ORIGINAIS QUE VIRARAM 'Unknown' ({len(stats['unknown_original'])} únicos)"
        )
        print(f"{'=' * 70}")
        for val in sorted(stats["unknown_original"])[:20]:
            print(f"  - {val}")
        if len(stats["unknown_original"]) > 20:
            print(f"  ... e mais {len(stats['unknown_original']) - 20} valores")

    # Salvar CSV normalizado
    print(f"\n[4/4] Salvando CSV normalizado...")
    df_normalized.to_csv(output_file, index=False)
    print(f"   ✓ Arquivo salvo: {output_file}")

    # Exemplos de normalização
    print(f"\n{'=' * 70}")
    print("EXEMPLOS DE NORMALIZAÇÃO (primeiros 10)")
    print(f"{'=' * 70}")
    print(
        df_normalized[["origem", "origem_normalizada"]].head(10).to_string(index=False)
    )

    print(f"\n{'=' * 70}")
    print("✓ PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
