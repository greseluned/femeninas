import pandas as pd
import re
from pathlib import Path


# =========================
# CONFIGURACIÓN
# =========================

INPUT_FOLDER = "textos_revistas"
OUTPUT_CSV = "corpus_revistas_chunks.csv"

MIN_WORDS = 200
MAX_WORDS = 300


# =========================
# FUNCIONES
# =========================

def limpiar_espacios(texto):
    """
    Normaliza espacios, saltos de línea y tabulaciones.
    """
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()


def obtener_nombre_revista(nombre_archivo):
    """
    Extrae el nombre de la revista a partir del nombre del archivo.
    Ejemplos:
    filipinas_merged.txt -> Filipinas
    femina_merged.txt -> Fémina
    heraldo_merged.txt -> El Heraldo de la Mujer
    """
    nombre = nombre_archivo.lower()

    if "filipinas" in nombre:
        return "Filipinas"
    elif "femina" in nombre or "fémina" in nombre:
        return "Fémina"
    elif "heraldo" in nombre:
        return "El Heraldo de la Mujer"
    else:
        return Path(nombre_archivo).stem


def crear_chunks(texto, min_words=200, max_words=300):
    """
    Divide un texto en fragmentos de entre 200 y 300 palabras.

    Estrategia:
    - Crea fragmentos de máximo 300 palabras.
    - Si el último fragmento queda por debajo de 200 palabras,
      se une al fragmento anterior.
    """
    texto = limpiar_espacios(texto)
    palabras = texto.split()

    if len(palabras) == 0:
        return []

    if len(palabras) < min_words:
        return [" ".join(palabras)]

    chunks = []

    for i in range(0, len(palabras), max_words):
        chunk = palabras[i:i + max_words]
        chunks.append(chunk)

    if len(chunks) > 1 and len(chunks[-1]) < min_words:
        chunks[-2].extend(chunks[-1])
        chunks = chunks[:-1]

    return [" ".join(chunk) for chunk in chunks]


# =========================
# PROCESAMIENTO
# =========================

input_path = Path(INPUT_FOLDER)

if not input_path.exists():
    raise FileNotFoundError(f"No existe la carpeta: {INPUT_FOLDER}")

txt_files = sorted(input_path.glob("*.txt"))

if not txt_files:
    raise FileNotFoundError(f"No se han encontrado archivos .txt en: {INPUT_FOLDER}")

rows = []

for file_path in txt_files:
    revista = obtener_nombre_revista(file_path.name)

    with open(file_path, "r", encoding="utf-8") as f:
        texto = f.read()

    chunks = crear_chunks(texto, MIN_WORDS, MAX_WORDS)

    for chunk_num, chunk_text in enumerate(chunks, start=1):
        rows.append({
            "chunk_id": f"{file_path.stem}_{chunk_num:04d}",
            "revista": revista,
            "archivo_origen": file_path.name,
            "chunk_num": chunk_num,
            "n_palabras": len(chunk_text.split()),
            "texto": chunk_text
        })

df_chunks = pd.DataFrame(rows)

df_chunks.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")

print(f"Archivo creado: {OUTPUT_CSV}")
print(f"Archivos procesados: {len(txt_files)}")
print(f"Chunks creados: {len(df_chunks)}")
print()
print(df_chunks.groupby("revista")["chunk_id"].count())
print()
print(df_chunks.head())