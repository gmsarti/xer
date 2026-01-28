# Código para Normalização de Origens - Executar no Jupyter Notebook

## Importar módulo de normalização

```python
import sys
sys.path.append('/home/gusarti/pessoal/code/xer')

from normalize_origins import normalize_origin, apply_normalization, analyze_normalization
import pandas as pd
```

## Carregar CSV

```python
# Carregar arquivo CSV
df = pd.read_csv('/home/gusarti/pessoal/code/xer/data/contos_semi_limpos.csv')

print(f"Carregadas {len(df)} linhas")
print(f"Colunas: {df.columns.tolist()}")
```

## Aplicar Normalização

```python
# Aplicar normalização
df_normalized = apply_normalization(df, column='origem', new_column='origem_normalizada')

print("\n✓ Coluna 'origem_normalizada' criada")
```

## Ver Estatísticas

```python
# Analisar resultados
stats = analyze_normalization(df_normalized)

print("="*70)
print("ESTATÍSTICAS DE NORMALIZAÇÃO")
print("="*70)
print(f"Valores únicos originais:     {stats['unique_original']:>6}")
print(f"Valores únicos normalizados:  {stats['unique_normalized']:>6}")
print(f"Cobertura (% mapeados):       {stats['coverage']:>6.2f}%")
print(f"Valores não mapeados:         {stats['unmapped_count']:>6}")
print(f"Valores desconhecidos:        {stats['unknown_count']:>6}")
```

## Top 20 Países

```python
print("\n" + "="*70)
print("TOP 20 PAÍSES/REGIÕES")
print("="*70)
print(stats['distribution'].head(20))
```

## Ver Exemplos de Normalização

```python
print("\n" + "="*70)
print("EXEMPLOS DE NORMALIZAÇÃO")
print("="*70)
print(df_normalized[['origem', 'origem_normalizada']].head(20))
```

## Verificar Valores Não Mapeados

```python
if stats['unmapped_count'] > 0:
    print("\n" + "="*70)
    print(f"VALORES NÃO MAPEADOS ({len(stats['unmapped_values'])})")
    print("="*70)
    for val in sorted(stats['unmapped_values'])[:30]:
        print(f"  - {val}")
```

## Salvar CSV Normalizado

```python
# Salvar arquivo normalizado
output_file = '/home/gusarti/pessoal/code/xer/data/contos_normalizados.csv'
df_normalized.to_csv(output_file, index=False)
print(f"\n✓ Arquivo salvo: {output_file}")
```

## Análise Adicional: Distribuição por País

```python
# Filtrar apenas países válidos (sem "Unknown" e "Other:")
valid_countries = stats['distribution'][
    ~stats['distribution'].index.str.startswith('Other:', na=False) &
    (stats['distribution'].index != 'Unknown')
]

print("\n" + "="*70)
print("PAÍSES VÁLIDOS (excluindo Unknown e Other)")
print("="*70)
print(f"Total de países diferentes: {len(valid_countries)}")
print("\nTop 15:")
for country, count in valid_countries.head(15).items():
    print(f"{country:40} {count:>6}")
```
