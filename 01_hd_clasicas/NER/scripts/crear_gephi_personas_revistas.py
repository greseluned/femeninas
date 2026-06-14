from pathlib import Path
import re
import json
import urllib.parse
import urllib.request
import pandas as pd


FILES = [
    r"C:\Users\Rocio\nuevo_corpus\entidades\entidades-femina-wikidata.tsv",
    r"C:\Users\Rocio\nuevo_corpus\entidades\entities-heraldo-wikidata.tsv",
    r"C:\Users\Rocio\nuevo_corpus\entidades\entidades-filipinas-wikidata.tsv",
]

OUTPUT_DIR = Path(r"C:\Users\Rocio\nuevo_corpus\entidades\gephi")
OUTPUT_DIR.mkdir(exist_ok=True)

ENTITY_COL = "entity_normalized_clean"

# Si hay casos que quieres forzar manualmente, añádelos aquí.
# La clave puede ser el QID o el texto original.
MANUAL_OVERRIDES = {
    # Autores y figuras clásicas
    "Q535": "Victor Hugo",
    "Q859": "Platón",
    "Q1398": "Horacio",
    "Q397": "Virgilio",
    "Q5682": "Homero",
    "Q996": "Aristóteles",
    "Q43353": "Ovidio",
    "Q41155": "Dante Alighieri",
    "Q5592": "William Shakespeare",
    "Q5685": "Miguel de Cervantes",

    # Si tienes localizado el QID exacto de Pascual H. Poblete, añádelo aquí:
    # "QXXXXXX": "Pascual H. Poblete",

    # Correcciones por texto, por si no hay QID
    "Victor Hugo": "Victor Hugo",
    "Виктор Гюго": "Victor Hugo",
    "Horace": "Horacio",
    "Virgil": "Virgilio",
    "Plato": "Platón",
    "Mary": "Virgen María",
    "Harlequin": "Arlequín",
}


def get_magazine_name(file_path: Path) -> str:
    stem = file_path.stem
    stem = re.sub(r"^(entidades|entities)-", "", stem, flags=re.IGNORECASE)
    stem = re.sub(r"-wikidata$", "", stem, flags=re.IGNORECASE)
    return stem.strip().title()


def clean_entity_value(value):
    if pd.isna(value):
        return ""

    value = str(value).strip()
    value = re.sub(r"\s+", " ", value)
    return value


def make_safe_id(prefix: str, value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"\s+", "_", value)
    value = re.sub(r"[^\w\-áéíóúüñ]", "", value, flags=re.IGNORECASE)
    return f"{prefix}_{value}"


def find_qid_column(df: pd.DataFrame):
    """
    Intenta encontrar una columna que contenga QIDs de Wikidata.
    Funciona con nombres habituales exportados desde OpenRefine.
    """
    preferred_names = [
        "wikidata_qid",
        "qid",
        "QID",
        "recon.match.id",
        "entity_qid",
        "wikidata_id",
        "id_wikidata",
    ]

    for col in preferred_names:
        if col in df.columns:
            return col

    # Si no encuentra una columna por nombre, busca una columna cuyos valores
    # parezcan QIDs: Q123, Q4567, etc.
    qid_pattern = re.compile(r"^Q\d+$")

    for col in df.columns:
        sample = df[col].dropna().astype(str).str.strip()
        sample = sample[sample != ""].head(50)

        if len(sample) == 0:
            continue

        matches = sample.apply(lambda x: bool(qid_pattern.match(x))).sum()

        if matches >= max(1, len(sample) * 0.5):
            return col

    return None


def extract_qid(value):
    """
    Extrae un QID aunque venga mezclado con URL u otro texto.
    """
    if pd.isna(value):
        return ""

    value = str(value).strip()
    match = re.search(r"\bQ\d+\b", value)

    if match:
        return match.group(0)

    return ""


def fetch_wikidata_labels_es(qids):
    """
    Consulta Wikidata y devuelve etiquetas en español.
    Si Wikidata no responde o no hay etiqueta española, no sustituye nada.
    """
    import time
    from urllib.error import HTTPError, URLError

    qids = sorted(set(qid for qid in qids if qid))

    labels = {}

    if not qids:
        return labels

    batch_size = 30

    for i in range(0, len(qids), batch_size):
        batch = qids[i:i + batch_size]

        params = {
            "action": "wbgetentities",
            "ids": "|".join(batch),
            "props": "labels",
            "languages": "es",
            "format": "json",
        }

        url = "https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode(params)

        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": (
                    "gephi-personas-revistas/1.0 "
                    "(research script; contact: rocio.ocasanova@gmail.com)"
                )
            }
        )

        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                data = json.loads(response.read().decode("utf-8"))

        except HTTPError as e:
            print(f"  Aviso: Wikidata devolvió HTTP {e.code}. Se conservarán los nombres locales para este lote.")
            continue

        except URLError as e:
            print(f"  Aviso: no se pudo conectar con Wikidata: {e}. Se conservarán los nombres locales para este lote.")
            continue

        except TimeoutError:
            print("  Aviso: la consulta a Wikidata tardó demasiado. Se conservarán los nombres locales para este lote.")
            continue

        entities = data.get("entities", {})

        for qid, item in entities.items():
            if "missing" in item:
                continue

            item_labels = item.get("labels", {})

            if "es" in item_labels:
                label = item_labels["es"].get("value", "").strip()
                if label:
                    labels[qid] = label

        time.sleep(0.2)

    return labels

def build_canonical_entity(row, qid_col, wikidata_labels):
    original_entity = clean_entity_value(row.get(ENTITY_COL, ""))

    qid = ""
    if qid_col:
        qid = extract_qid(row.get(qid_col, ""))

    # 1. Corrección manual por QID
    if qid and qid in MANUAL_OVERRIDES:
        return MANUAL_OVERRIDES[qid]

    # 2. Etiqueta española de Wikidata, solo si existe
    if qid and qid in wikidata_labels and wikidata_labels[qid]:
        return wikidata_labels[qid]

    # 3. Corrección manual por texto
    if original_entity in MANUAL_OVERRIDES:
        return MANUAL_OVERRIDES[original_entity]

    # 4. Fallback: valor limpio original
    return original_entity


all_rows = []

for file in FILES:
    file_path = Path(file)
    magazine = get_magazine_name(file_path)

    print(f"Leyendo: {file_path.name} → revista: {magazine}")

    df = pd.read_csv(
        file_path,
        sep="\t",
        dtype=str,
        encoding="utf-8-sig",
        keep_default_na=False
    )

    if ENTITY_COL not in df.columns:
        raise ValueError(
            f"El archivo {file_path.name} no tiene la columna '{ENTITY_COL}'. "
            f"Columnas disponibles: {list(df.columns)}"
        )

    # Filtrar solo personas si existe una columna type.
    possible_type_cols = ["type", "Type", "label", "Label", "entity_type"]
    type_col = next((col for col in possible_type_cols if col in df.columns), None)

    if type_col:
        df = df[df[type_col].str.upper().str.strip() == "PER"].copy()

    qid_col = find_qid_column(df)

    if qid_col:
        print(f"  Columna QID detectada: {qid_col}")
        df["_wikidata_qid"] = df[qid_col].apply(extract_qid)
    else:
        print("  No se ha detectado columna QID. Se usará entity_normalized_clean.")
        df["_wikidata_qid"] = ""

    qids = df["_wikidata_qid"].dropna().astype(str).tolist()
    wikidata_labels = fetch_wikidata_labels_es(qids)

    print(f"  QIDs con etiqueta recuperada: {len(wikidata_labels)}")

    df["entity_canonical_es"] = df.apply(
        lambda row: build_canonical_entity(row, "_wikidata_qid", wikidata_labels),
        axis=1
    )

    for _, row in df.iterrows():
        entity = clean_entity_value(row["entity_canonical_es"])
        qid = clean_entity_value(row["_wikidata_qid"])

        if not entity:
            continue

        all_rows.append({
            "revista": magazine,
            "persona": entity,
            "wikidata_qid": qid,
            "entity_original_clean": clean_entity_value(row[ENTITY_COL])
        })


combined = pd.DataFrame(all_rows)

combined = combined[
    (combined["revista"].str.strip() != "") &
    (combined["persona"].str.strip() != "")
].copy()


# Tabla combinada para revisar
combined_output = OUTPUT_DIR / "personas_revistas_combinado_es.tsv"
combined.to_csv(
    combined_output,
    sep="\t",
    index=False,
    encoding="utf-8-sig"
)


# Aristas para Gephi
edges = (
    combined
    .groupby(["revista", "persona", "wikidata_qid"])
    .size()
    .reset_index(name="Weight")
)

edges["Source"] = edges["revista"].apply(lambda x: make_safe_id("revista", x))

# Para personas reconciliadas, usamos el QID como ID estable.
# Para personas sin QID, usamos el nombre.
edges["Target"] = edges.apply(
    lambda row: f"persona_{row['wikidata_qid']}"
    if row["wikidata_qid"]
    else make_safe_id("persona", row["persona"]),
    axis=1
)

edges["Type"] = "Undirected"
edges["Label"] = edges["revista"] + " — " + edges["persona"]

edges_gephi = edges[["Source", "Target", "Type", "Weight", "Label", "revista"]]

edges_output = OUTPUT_DIR / "gephi_edges_personas_revistas_es.csv"
edges_gephi.to_csv(
    edges_output,
    index=False,
    encoding="utf-8-sig"
)


# Nodos para Gephi
magazines = combined["revista"].drop_duplicates().sort_values()

magazine_nodes = pd.DataFrame({
    "Id": magazines.apply(lambda x: make_safe_id("revista", x)),
    "Label": magazines,
    "node_type": "revista"
})

person_rows = (
    combined[["persona", "wikidata_qid"]]
    .drop_duplicates()
    .sort_values("persona")
)

person_rows["Id"] = person_rows.apply(
    lambda row: f"persona_{row['wikidata_qid']}"
    if row["wikidata_qid"]
    else make_safe_id("persona", row["persona"]),
    axis=1
)

person_nodes = pd.DataFrame({
    "Id": person_rows["Id"],
    "Label": person_rows["persona"],
    "node_type": "persona",
    "wikidata_qid": person_rows["wikidata_qid"]
})

nodes = pd.concat([magazine_nodes, person_nodes], ignore_index=True)

nodes_output = OUTPUT_DIR / "gephi_nodes_personas_revistas_es.csv"
nodes.to_csv(
    nodes_output,
    index=False,
    encoding="utf-8-sig"
)


print("\nArchivos creados:")
print(f"  Tabla combinada revisable: {combined_output}")
print(f"  Aristas Gephi:             {edges_output}")
print(f"  Nodos Gephi:               {nodes_output}")

print("\nResumen:")
print(f"  Filas combinadas:          {len(combined)}")
print(f"  Aristas revista-persona:   {len(edges_gephi)}")
print(f"  Nodos totales:             {len(nodes)}")
print(f"  Revistas:                  {magazine_nodes['Label'].nunique()}")
print(f"  Personas únicas:           {person_nodes['Label'].nunique()}")