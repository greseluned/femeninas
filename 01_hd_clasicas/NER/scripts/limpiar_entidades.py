from pathlib import Path
import re
import pandas as pd
import unicodedata
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True, help="Carpeta con los CSV/TSV de entrada")
parser.add_argument("--output", required=True, help="Carpeta donde se guardarán los archivos limpios")
args = parser.parse_args()

INPUT_DIR = Path(args.input)
OUTPUT_DIR = Path(args.output)
OUTPUT_DIR.mkdir(exist_ok=True)


# Nombre de la columna que quieres limpiar.
# Si tus archivos tienen otro nombre, cámbialo aquí.
PREFERRED_ENTITY_COLUMNS = [
    "entity_normalizada",
    "entity_original",
    "entity",
    "text",
    "Column4",
    "Column3",
]


# Stop-words o partículas que normalmente deben quedar en minúscula
# dentro de nombres propios.
LOWERCASE_WORDS = {
    # Español
    "a", "ante", "bajo", "con", "contra", "de", "del", "desde",
    "durante", "e", "el", "en", "entre", "hacia", "hasta", "la",
    "las", "lo", "los", "para", "por", "según", "sin", "sobre",
    "tras", "u", "y",

    # Francés
    "à", "au", "aux", "chez", "d", "de", "des", "du", "en", "et",
    "la", "le", "les", "l",

    # Inglés
    "and", "of", "the", "for", "in", "on", "at", "by", "to",

    # Italiano / portugués
    "da", "das", "de", "del", "della", "di", "do", "dos", "e",

    # Alemán / neerlandés
    "am", "an", "auf", "der", "die", "das", "den", "dem", "des",
    "im", "in", "und", "van", "von", "zu", "zum", "zur",
}


# Formas de tratamiento y títulos.
# Puedes ampliar esta lista según vayas detectando más casos.
HONORIFICS = [
    # Español
    "sr", "sr.", "sra", "sra.", "srta", "srta.", "señor", "señora",
    "señorita", "senor", "senora", "senorita",
    "d", "d.", "don", "doña", "dona",
    "dr", "dr.", "dra", "dra.", "doctor", "doctora",
    "lic", "lic.", "ing", "ing.", "prof", "prof.", "profa", "profa.",
    "fr", "fr.", "fray", "sor", "hno", "hna",
    "padre", "madre", "reverendo", "reverenda", "rvdo", "rvdo.",

    # Inglés
    "mr", "mr.", "mrs", "mrs.", "ms", "ms.", "miss",
    "sir", "madam", "madame", "lady", "lord",
    "dr", "dr.", "prof", "prof.", "rev", "rev.",

    # Francés
    "m", "m.", "mme", "mme.", "mlle", "mlle.",
    "monsieur", "madame", "mademoiselle",
    "docteur", "professeur",

    # Italiano
    "sig", "sig.", "sigra", "sig.ra", "signor", "signora", "signorina",
    "dott", "dott.", "dottssa", "dott.ssa",

    # Portugués
    "sr", "sr.", "sra", "sra.", "srta", "srta.",
    "senhor", "senhora", "senhorita",
    "dr", "dr.", "dra", "dra.",

    # Alemán
    "herr", "frau", "fräulein", "fraulein", "dr", "dr.", "prof", "prof.",

    # Neerlandés
    "dhr", "dhr.", "mevr", "mevr.", "mevrouw", "meneer",

    # Religiosos / eclesiásticos frecuentes
    "monseñor", "monsenor", "msgr", "msgr.", "mgr", "mgr.",
    "obispo", "arzobispo", "cardenal", "papa",
]


def strip_accents_for_matching(text: str) -> str:
    """
    Devuelve una versión sin acentos para comparar,
    pero no se usa para reemplazar el texto original.
    """
    text = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in text if unicodedata.category(ch) != "Mn")


def remove_quotes(text: str) -> str:
    """
    Elimina comillas rectas, latinas y tipográficas.
    """
    if pd.isna(text):
        return text

    text = str(text)
    return (
        text.replace('"', "")
            .replace("'", "")
            .replace("“", "")
            .replace("”", "")
            .replace("‘", "")
            .replace("’", "")
            .replace("«", "")
            .replace("»", "")
            .strip()
    )


def build_honorific_regex():
    """
    Construye un patrón para eliminar formas de tratamiento.
    Se aplica sobre todo al principio de la entidad, que es donde
    suelen aparecer: 'Sra. María...', 'Doña Linda...', etc.
    """
    escaped = []

    for h in HONORIFICS:
        h = h.strip()
        h_no_accents = strip_accents_for_matching(h)

        # Permitimos que los puntos sean opcionales:
        # sr. / sr / s r no, solo sr o sr.
        pattern = re.escape(h_no_accents).replace(r"\.", r"\.?")
        escaped.append(pattern)

    joined = "|".join(sorted(set(escaped), key=len, reverse=True))

    # Elimina uno o varios tratamientos al comienzo.
    return re.compile(
        rf"^\s*(?:{joined})(?:\s+|,\s*|:\s*|\.\s*)+",
        flags=re.IGNORECASE
    )


HONORIFIC_START_RE = build_honorific_regex()


def remove_initial_honorifics(text: str) -> str:
    """
    Elimina tratamientos al principio de la entidad.
    Repite el proceso por si hay varios:
    'Sra. Dra. María...' -> 'María...'
    """
    if pd.isna(text):
        return text

    original = str(text).strip()

    # Para hacer matching sin acentos, necesitamos mapear de forma sencilla.
    # Como los tratamientos están al comienzo, podemos trabajar con una copia
    # sin acentos y calcular cuántos caracteres se eliminan.
    current = original

    while True:
        comparable = strip_accents_for_matching(current)
        match = HONORIFIC_START_RE.match(comparable)

        if not match:
            break

        cut = match.end()
        current = current[cut:].strip()

    return current


def is_all_caps_entity(text: str) -> bool:
    """
    Considera que una entidad está en mayúsculas si tiene letras
    y todas las letras con distinción de caso están en mayúsculas.
    """
    if pd.isna(text):
        return False

    text = str(text).strip()
    letters = [ch for ch in text if ch.isalpha()]

    if not letters:
        return False

    return all(not ch.islower() for ch in letters)


def smart_title_word(word: str, position: int) -> str:
    """
    Capitaliza una palabra, respetando:
    - partículas en minúscula si no son la primera palabra
    - iniciales: A. B. C.
    - palabras con guion: María-Luisa
    """

    clean = word.strip()

    if not clean:
        return clean

    # Mantener iniciales tipo A. o M.
    if re.fullmatch(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]\.", clean):
        return clean.upper()

    # Separar puntuación inicial/final
    prefix_match = re.match(r"^[^\wÁÉÍÓÚÜÑáéíóúüñ]+", clean)
    suffix_match = re.search(r"[^\wÁÉÍÓÚÜÑáéíóúüñ]+$", clean)

    prefix = prefix_match.group(0) if prefix_match else ""
    suffix = suffix_match.group(0) if suffix_match else ""

    core = clean[len(prefix):]
    if suffix:
        core = core[:-len(suffix)]

    if not core:
        return clean

    core_lower = core.lower()

    if position > 0 and core_lower in LOWERCASE_WORDS:
        new_core = core_lower
    else:
        # Maneja nombres compuestos con guion
        parts = core_lower.split("-")
        new_core = "-".join(
            p[:1].upper() + p[1:] if p else p
            for p in parts
        )

    return prefix + new_core + suffix


def smart_title(text: str) -> str:
    """
    Convierte una entidad en mayúsculas a título con partículas en minúscula.
    """
    if pd.isna(text):
        return text

    words = str(text).split()
    return " ".join(
        smart_title_word(word, i)
        for i, word in enumerate(words)
    )


def clean_entity(text: str) -> str:
    """
    Limpieza completa de la entidad.
    """
    if pd.isna(text):
        return text

    text = str(text).strip()

    # 1. Quitar comillas
    text = remove_quotes(text)

    # 2. Quitar tratamientos iniciales
    text = remove_initial_honorifics(text)

    # 3. Normalizar espacios
    text = re.sub(r"\s+", " ", text).strip()

    # 4. Si todo está en mayúsculas, aplicar capitalización inteligente
    if is_all_caps_entity(text):
        text = smart_title(text)

    # 5. Limpiar espacios antes de puntos y comas
    text = re.sub(r"\s+([.,;:])", r"\1", text)

    return text.strip()


def detect_separator(file_path: Path) -> str:
    """
    Detecta si el archivo parece CSV o TSV.
    """
    sample = file_path.read_text(encoding="utf-8-sig", errors="replace")[:5000]

    tabs = sample.count("\t")
    commas = sample.count(",")

    if tabs > commas:
        return "\t"
    return ","


def choose_entity_column(df: pd.DataFrame) -> str:
    """
    Elige la columna de entidades.
    Primero busca nombres esperados.
    Si no los encuentra, usa la última columna.
    """
    for col in PREFERRED_ENTITY_COLUMNS:
        if col in df.columns:
            return col

    return df.columns[-1]


def process_file(file_path: Path):
    sep = detect_separator(file_path)

    df = pd.read_csv(
        file_path,
        sep=sep,
        dtype=str,
        encoding="utf-8-sig",
        keep_default_na=False
    )

    entity_col = "entity_normalized"
    clean_col = "entity_normalized_clean"

    if entity_col not in df.columns:
        raise ValueError(
            f"El archivo {file_path.name} no tiene una columna llamada '{entity_col}'. "
            f"Columnas disponibles: {list(df.columns)}"
        )

    df[clean_col] = df[entity_col].apply(clean_entity)

    output_path = OUTPUT_DIR / f"{file_path.stem}_limpio.tsv"

    df.to_csv(
        output_path,
        sep="\t",
        index=False,
        encoding="utf-8-sig"
    )

    print(f"Procesado: {file_path.name}")
    print(f"  Columna limpiada: {entity_col}")
    print(f"  Nueva columna creada: {clean_col}")
    print(f"  Archivo guardado: {output_path}")


def main():
    files = list(INPUT_DIR.glob("*.csv")) + list(INPUT_DIR.glob("*.tsv")) + list(INPUT_DIR.glob("*.txt"))

    if not files:
        print(f"No se encontraron archivos CSV/TSV/TXT en {INPUT_DIR.resolve()}")
        return

    for file_path in files:
        process_file(file_path)


if __name__ == "__main__":
    main()