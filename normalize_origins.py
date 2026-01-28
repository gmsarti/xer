"""
Script para normalizar valores da coluna 'origem' de folktales/contos.

Estratégia:
- Extrair país principal de "País (Região)" → "País"
- Manter múltiplos países como "País1/País2"
- Mapear regiões históricas para países modernos
- Remover autores/fontes e manter apenas país
- Valores NaN → "Unknown"
"""

import pandas as pd
import numpy as np
import re


# Conjunto de países válidos reconhecidos
VALID_COUNTRIES = {
    "Afghanistan",
    "Albania",
    "Algeria",
    "Antigua",
    "Argentina",
    "Armenia",
    "Australia",
    "Austria",
    "Azerbaijan",
    "Bahamas",
    "Bangladesh",
    "Basque",
    "Belgium",
    "Bohemia",
    "Bolivia",
    "Bosnia",
    "Brazil",
    "Britain",
    "Brittany",
    "Bulgaria",
    "Burkina Faso",
    "Burgenland",
    "Burundi",
    "Cambodia",
    "Cameroon",
    "Canada",
    "Carinthia",
    "Catalonia",
    "Celtic",
    "Chad",
    "Chile",
    "China",
    "Colombia",
    "Congo",
    "Cornwall",
    "Croatia",
    "Cuba",
    "Cyprus",
    "Czechia",
    "Czech Republic",
    "Denmark",
    "East Africa",
    "East Prussia",
    "Ecuador",
    "Egypt",
    "England",
    "Eskimo",
    "Estonia",
    "Ethiopia",
    "Europe",
    "Faroe Islands",
    "Fiji",
    "Finland",
    "Flanders",
    "France",
    "Georgia",
    "Germany",
    "Ghana",
    "Greece",
    "Guam",
    "Guatemala",
    "Guernsey",
    "Guinea",
    "Haiti",
    "Holland",
    "Honduras",
    "Hungary",
    "Iceland",
    "India",
    "Indonesia",
    "Iran",
    "Iraq",
    "Ireland",
    "Isle of Man",
    "Israel",
    "Italy",
    "Jamaica",
    "Japan",
    "Jewish",
    "Jordan",
    "Kashmir",
    "Kenya",
    "Korea",
    "Kurdistan",
    "Laos",
    "Latvia",
    "Lebanon",
    "Liberia",
    "Libya",
    "Lithuania",
    "Luxembourg",
    "Macedonia",
    "Madagascar",
    "Malawi",
    "Malaya",
    "Malaysia",
    "Mali",
    "Malta",
    "Mauritania",
    "Mauritius",
    "Mexico",
    "Middle East",
    "Moldova",
    "Mongolia",
    "Montenegro",
    "Moravia",
    "Morocco",
    "Mozambique",
    "Myanmar",
    "Namibia",
    "Nepal",
    "Netherlands",
    "New Zealand",
    "Nicaragua",
    "Niger",
    "Nigeria",
    "North Africa",
    "Norway",
    "Orkney Islands",
    "Pacific Islands",
    "Pakistan",
    "Palestine",
    "Panama",
    "Papua New Guinea",
    "Paraguay",
    "Persia",
    "Peru",
    "Philippines",
    "Poland",
    "Portugal",
    "Prussia",
    "Romania",
    "Russia",
    "Rwanda",
    "Samoa",
    "Scandinavia",
    "Scotland",
    "Senegal",
    "Serbia",
    "Shetland Islands",
    "Sicily",
    "Sierra Leone",
    "Singapore",
    "Slavic",
    "Slavonic",
    "Slovakia",
    "Slovenia",
    "Somalia",
    "South Africa",
    "Spain",
    "Sri Lanka",
    "Sudan",
    "Swabia",
    "Swahili",
    "Sweden",
    "Switzerland",
    "Syria",
    "Taiwan",
    "Tanzania",
    "Thailand",
    "Tibet",
    "Togo",
    "Transylvania",
    "Trinidad",
    "Tunisia",
    "Turkey",
    "Turkmenistan",
    "Tyrol",
    "Uganda",
    "Ukraine",
    "United Kingdom",
    "Uruguay",
    "USA",
    "Uzbekistan",
    "Venezuela",
    "Vietnam",
    "Wales",
    "Wendish",
    "Yemen",
    "Zambia",
    "Zanzibar",
    "Zimbabwe",
}


# Mapeamento extensivo de valores para países/regiões padronizados
COUNTRY_MAPPING = {
    # Valores inválidos/numéricos
    "1": "Unknown",
    "19": "Unknown",
    "32": "Unknown",
    "I.": "Unknown",
    "nan": "Unknown",
    "Links open in new windows.": "Unknown",
    "Traditional": "Unknown",
    # Obras literárias → Região de origem
    "1001 Nights": "Middle East",
    "1001 Nights(translated by John Payne)": "Middle East",
    "1001 Nights(translated by Richard Burton)": "Middle East",
    "The 1001 Nights": "Middle East",
    "Kalila and Dimna": "India/Persia",
    "Kalilah and Dimnah": "India/Persia",
    "The Jataka": "India",
    "The Jataka Tales": "India",
    "Jataka Tales": "India",
    "Ummagga Jataka": "India",
    "The Panchatantra": "India",
    "The Mahabharata": "India",
    "The Kathasaritsagara": "India",
    "The Udana": "India",
    "The Udāna": "India",
    "Homer,The Odyssey": "Greece",
    "The Masnavi": "Persia",
    "TheMasnavi": "Persia",
    "Rumi,The Masnavi": "Persia",
    "The Romance of the Rose": "France",
    "The Seven Wise Masters": "Middle East",
    "Gesta Romanorum": "Europe",
    "The Quran": "Middle East",
    "TheToledot Yeshu": "Jewish",
    "Suka Saptati; or, Seventy Tales of a Parrot": "India",
    # Autores clássicos
    "Aesop": "Greece",
    "Aesop (Caxton, 1484)": "Greece",
    "Aesop (Jacobs, 1894)": "Greece",
    "Aesop (Jones, 1912)": "Greece",
    "Aesop (L'Estrange, 1692)": "Greece",
    "Aesop (Roger L'Estrange)": "Greece",
    "Anianus (L'Estrange, 1692)": "Greece",
    "Attributed to Aesop": "Greece",
    "Avianus": "Rome",
    "Bidpai": "India",
    "Laurentius Abstemius": "Italy",
    "Petrus Alphonsi": "Spain",
    "Poggio Bracciolini": "Italy",
    "Italy,The Facetiæof Poggio": "Italy",
    # Autores modernos (usar país de origem)
    "Hans Christian Andersen": "Denmark",
    "Charles Perrault": "France",
    "Giambattista Basile": "Italy",
    "Giovanni Battista Basile,Il Pentamerone": "Italy",
    "Giovanni Boccaccio": "Italy",
    "Giovanni Francesco Straparola": "Italy",
    "Giovanni Francesco Straparola,The Facetious Nights": "Italy",
    "Jacob and Wilhelm Grimm": "Germany",
    "Jacob and Wilhelm Grimm, 1812": "Germany",
    "Jacob and Wilhelm Grimm, 1819": "Germany",
    "Jacob and Wilhelm Grimm,Children's and Household Tales": "Germany",
    "Jacob and Wilhelm Grimm,German Legends": "Germany",
    "Ludwig Bechstein": "Germany",
    "Marie de France": "France",
    "Jean de La Fontaine": "France",
    "Geoffrey Chaucer": "England",
    "Sir Thomas Malory": "England",
    "Washington Irving": "USA",
    "Mark Twain": "USA",
    "Ambrose Bierce": "USA",
    "James Thurber": "USA",
    "Leo Tolstoy": "Russia",
    "Martin Luther": "Germany",
    "Gotthold Ephraim Lessing": "Germany",
    "Wilhelm Busch": "Germany",
    "Heinrich Heine": "Germany",
    "Joseph von Eichendorff": "Germany",
    "Ludwig Uhland": "Germany",
    "Clemens Brentano": "Germany",
    "Alfred, Lord Tennyson": "England",
    "William Butler Yeats": "Ireland",
    "Henry Wadsworth Longfellow": "USA",
    "John Godfrey Saxe": "USA",
    "Thomas Parnell": "Ireland",
    "Ramakrishna": "India",
    "Paracelsus": "Switzerland",
    # Grupos étnicos/culturais
    "African American": "USA",
    "African-American": "USA",
    "African-America (Joel Chandler Harris)": "USA",
    "African American, Joel Chandler Harris": "USA",
    "Joel Chandler Harris": "USA",
    "Irish-American": "USA",
    "Native American (Cherokee)": "USA",
    "Native American (Chickasaw)": "USA",
    "Native American (Zuni)": "USA",
    "Eskimo": "Arctic",
    "Basque": "Spain/France",
    "Celtic": "Celtic",
    "Slavic": "Slavic",
    "Slavonic": "Slavonic",
    "Jewish": "Jewish",
    "Wendish": "Germany",
    # Native American específicos
    "Nez Percé": "USA",
    "Okanagon": "Canada/USA",
    "Passamaquoddy": "USA/Canada",
    "Salish": "Canada/USA",
    "Skidi Pawnee": "USA",
    "Thompson (Ntlakyapamuk)": "Canada",
    "Tsimshian": "Canada",
    # Filipinas - grupos étnicos
    "Bagobo (Mindanao)": "Philippines",
    "Bilaan (Mindanao)": "Philippines",
    "Bukidnon (Mindanao)": "Philippines",
    "Igorot": "Philippines",
    "Mandaya (Mindanao)": "Philippines",
    "Philippines (Ilocano)": "Philippines",
    "Tagalog": "Philippines",
    # Regiões históricas/geográficas → Países modernos
    "Bavaria": "Germany",
    "Bavaria (Lower Franconia)": "Germany",
    "Bavaria (Oberbayern)": "Germany",
    "East Prussia": "Germany/Poland",
    "Prussia": "Germany",
    "Bohemia": "Czech Republic",
    "Moravia": "Czech Republic",
    "Transylvania": "Romania",
    "Tyrol": "Austria",
    "Tyrol / Bavaria": "Austria/Germany",
    "Carinthia (Kärnten)": "Austria",
    "Burgenland, Austria": "Austria",
    "Bukovina": "Romania/Ukraine",
    "Alsace (Germany / France)": "France/Germany",
    "Sicily": "Italy",
    "Tuscany": "Italy",
    "Swabia": "Germany",
    "Flanders": "Belgium",
    # Regiões britânicas
    "Cornwall": "England",
    "Cornwall, England": "England",
    "Devonshire": "England",
    "Yorkshire": "England",
    "Yorkshire, England": "England",
    "North Yorkshire": "England",
    "South Yorkshire": "England",
    "Lancashire": "England",
    "Norfolk": "England",
    "Oxfordshire": "England",
    "Gloucestershire": "England",
    "Herefordshire": "England",
    "Hertfordshire": "England",
    "Shropshire": "England",
    "Somerset": "England",
    "Sussex": "England",
    "County Durham": "England",
    "Northumberland": "England",
    "Northumbria": "England",
    "Cheshire": "England",
    "Derbyshire": "England",
    "Forfarshire, Scotland": "Scotland",
    "Roxburghshire, Scotland": "Scotland",
    "Orkney Islands": "Scotland",
    "Orkney Islands (Sanday)": "Scotland",
    "Orkney Islands, Scotland": "Scotland",
    "Shetland Islands": "Scotland",
    "Shetland\nIslands": "Scotland",
    "Shetland and Orkney\nIslands": "Scotland",
    "Isle of Man": "Isle of Man",
    "Guernsey": "England",
    # Suíça - cantões
    "Canton Bern": "Switzerland",
    "Bernese Oberland": "Switzerland",
    "St. Gallen": "Switzerland",
    "Unterwalden": "Switzerland",
    "Mount Pilatus": "Switzerland",
    # Áustria específica
    "Innsbruck": "Austria",
    "Salzburg": "Austria",
    # Alemanha específica
    "Rügen, Germany": "Germany",
    "Rügen. Germany": "Germany",
    # Ilhas
    "Faroe Islands": "Denmark",
    # África específica
    "Africa, Swahili": "East Africa",
    "Swahili": "East Africa",
    "North Africa (Kabyl)": "North Africa",
    "French North Africa": "North Africa",
    "Zanzibar": "Tanzania",
    # Índia - regiões
    "Kashmir": "India",
    "Sri Lanka (Northwestern Province)": "Sri Lanka",
    "Telugu Folktale": "India",
    # EUA específico
    "USA (Alabama)": "USA",
    "USA (Florida)": "USA",
    "USA (Idaho)": "USA",
    "USA (North Carolina)": "USA",
    "USA (Virginia)": "USA",
    "USA -- Georgia": "USA",
    "Georgia, USA": "USA",
    "North Carolina, USA": "USA",
    "New York, USA": "USA",
    "Pennsylvania, as recorded by Elsie Clews Parsons": "USA",
    "French Louisiana": "USA",
    "Children's Story, USA": "USA",
    # Países com múltiplas grafias
    "Holand": "Netherlands",
    "Holland": "Netherlands",
    "Czechia": "Czech Republic",
    # Especiais
    "Europe": "Europe",
    "Scandinavia": "Scandinavia",
    "Antigua, British West Indies": "Antigua",
    "Brampton Hunt": "England",
    # Textos religiosos/mitológicos
    "A Buddhist Parable": "India",
    "FromThe Prose Eddaof Snorri Sturluson": "Iceland",
    "FromThe Prose Eddaof Snorri Sturluson (Iceland)": "Iceland",
    "The First Book of Kings": "Middle East",
    "Geoffrey of Monmouth": "England",
    "The Account of Geoffrey of Monmouth": "England",
    "Roger of Wendover": "England",
    "Strabo": "Greece",
    "Jacques de Vitry": "France",
    # Atribuições específicas
    "Attributed to Nasreddin Hodja": "Turkey",
    "Attributed to Richard the Lionheart (Richard Coeur de Lion)": "England",
    # Compilações
    "Abstracted from the Faust Chapbook of 1587": "Germany",
    "A Voyage to New South Wales(1795)": "Australia",
    "A Christmastime Play Performed in Steyr, Austria": "Austria",
    "A Modern Fable": "Unknown",
    # Revistas/Publicações
    "Blackwood's Edinburgh Magazine, 1821)": "Scotland",
    'The Cruise of Her Majesty\'s Ship "Bacchante,"1881': "England",
    # Múltiplas origens já formatadas
    "Austria / Germany": "Austria/Germany",
    "Austria / Italy": "Austria/Italy",
    "Austria-Hungary": "Austria/Hungary",
    "Austria/Italy": "Austria/Italy",
    "Czech Republic / Austria": "Czech Republic/Austria",
    "England/Australia": "England/Australia",
    "France / Germany": "France/Germany",
    "Germany / Austria": "Germany/Austria",
    "Germany / Poland": "Germany/Poland",
    "Germany/Denmark": "Germany/Denmark",
    "Germany/Switzerland": "Germany/Switzerland",
    "India / Pakiston": "India/Pakistan",
    "India/Persia": "India/Persia",
    "Italy/Austria": "Italy/Austria",
    "Spain/France": "Spain/France",
    "Switzerland/Germany": "Switzerland/Germany",
    "Tibet/Nepal": "Tibet/Nepal",
    "USA/Canada": "USA/Canada",
    "Wales (and Brittany)": "Wales/Brittany",
}


# Prefixos comuns a serem removidos
PREFIXES_TO_REMOVE = [
    "Retold by ",
    "Attributed to ",
    "As recorded by ",
    "Abstracted from ",
    "Translated by ",
    "From",
    "An excerpt from ",
]


def normalize_origin(value):
    """
    Normaliza valores da coluna origem para nomes de países/regiões padronizados.

    Args:
        value: Valor original da coluna origem (pode ser NaN, string, etc.)

    Returns:
        str: País/região padronizado ou categoria especial
    """
    # Tratar NaN
    if pd.isna(value):
        return "Unknown"

    # Converter para string e limpar
    value = str(value).strip()

    # Casos vazios
    if not value or value.lower() == "nan":
        return "Unknown"

    # Aplicar mapeamento direto primeiro (mais rápido)
    if value in COUNTRY_MAPPING:
        return COUNTRY_MAPPING[value]

    # Remover prefixos comuns
    original_value = value
    for prefix in PREFIXES_TO_REMOVE:
        if value.startswith(prefix):
            value = value[len(prefix) :].strip()
            # Tentar mapeamento após remover prefixo
            if value in COUNTRY_MAPPING:
                return COUNTRY_MAPPING[value]

    # Padrão: "País (Região)" ou "País (Detalhes)"
    if "(" in value:
        country = value.split("(")[0].strip()
        # Verificar se o país é válido
        if country in VALID_COUNTRIES:
            return country
        # Tentar mapeamento do país extraído
        if country in COUNTRY_MAPPING:
            return COUNTRY_MAPPING[country]

    # Padrão: "País, Autor/Fonte/Coletor"
    if "," in value:
        parts = value.split(",")
        country = parts[0].strip()
        # Verificar se o país é válido
        if country in VALID_COUNTRIES:
            return country
        # Tentar mapeamento do país extraído
        if country in COUNTRY_MAPPING:
            return COUNTRY_MAPPING[country]

    # Padrão: múltiplos países com "/"
    if "/" in value and " / " not in value:
        # Já foi coberto por mapeamentos diretos ou precisa ser adicionado
        # Nós preferimos manter como está se não está no mapeamento
        countries = [c.strip() for c in value.split("/")]
        # Verificar se todos são países válidos
        if all(c in VALID_COUNTRIES for c in countries):
            return value

    # Se chegou aqui, não conseguimos mapear
    # Verificar se o valor em si é um país válido
    if value in VALID_COUNTRIES:
        return value

    # Caso especial: remover aspas, quebras de linha, etc.
    clean_value = re.sub(r"[\n\r\t]+", " ", value).strip()
    if clean_value != value:
        return normalize_origin(clean_value)

    # Se não conseguimos mapear, retornar como "Other" para revisão
    # Podemos também logar isso para debug
    return f"Other: {original_value[:50]}"


def apply_normalization(df, column="origem", new_column="origem_normalizada"):
    """
    Aplica normalização à coluna de origem do DataFrame.

    Args:
        df: DataFrame pandas
        column: Nome da coluna com dados originais
        new_column: Nome da nova coluna para dados normalizados

    Returns:
        DataFrame com nova coluna normalizada
    """
    df = df.copy()
    df[new_column] = df[column].apply(normalize_origin)
    return df


def analyze_normalization(
    df, original_column="origem", normalized_column="origem_normalizada"
):
    """
    Analisa os resultados da normalização.

    Args:
        df: DataFrame com colunas original e normalizada
        original_column: Nome da coluna original
        normalized_column: Nome da coluna normalizada

    Returns:
        dict com estatísticas e valores não mapeados
    """
    results = {}

    # Contagem de valores únicos
    results["unique_original"] = df[original_column].nunique()
    results["unique_normalized"] = df[normalized_column].nunique()

    # Distribuição dos valores normalizados
    results["distribution"] = df[normalized_column].value_counts()

    # Valores que caíram em "Other"
    other_mask = df[normalized_column].str.startswith("Other:", na=False)
    results["unmapped_count"] = other_mask.sum()
    results["unmapped_values"] = df[other_mask][original_column].unique()

    # Valores Unknown
    unknown_mask = df[normalized_column] == "Unknown"
    results["unknown_count"] = unknown_mask.sum()
    results["unknown_original"] = df[unknown_mask][original_column].unique()

    # Cobertura
    mapped_mask = ~other_mask & ~unknown_mask
    results["coverage"] = (mapped_mask.sum() / len(df)) * 100

    return results


if __name__ == "__main__":
    # Exemplo de uso
    print("Script de normalização de origens carregado.")
    print(f"Total de mapeamentos diretos: {len(COUNTRY_MAPPING)}")
    print(f"Total de países válidos: {len(VALID_COUNTRIES)}")
    print("\nExemplos de normalização:")

    test_cases = [
        "England (Cornwall)",
        "Germany, Jacob and Wilhelm Grimm",
        "Bavaria",
        "Aesop",
        np.nan,
        "Austria / Germany",
        "1001 Nights",
        "Native American (Cherokee)",
    ]

    for case in test_cases:
        normalized = normalize_origin(case)
        print(f"  {case!r:50} → {normalized!r}")
