import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from sentence_transformers import SentenceTransformer
from umap import UMAP


# =====================================================
# RUTAS
# =====================================================

BASE_DIR = Path(__file__).resolve().parents[1]

RESULTS_DIR = BASE_DIR / "results"
GRAFICAS_DIR = RESULTS_DIR / "graficas"

ARCHIVO_DOCUMENTOS = RESULTS_DIR / "documentos_con_topicos.csv"
ARCHIVO_TOPICOS = RESULTS_DIR / "topicos_bertopic.csv"

SALIDA_PNG = GRAFICAS_DIR / "mapa_topicos_puntos.png"
SALIDA_CSV = RESULTS_DIR / "coordenadas_topicos_puntos.csv"

GRAFICAS_DIR.mkdir(parents=True, exist_ok=True)


# =====================================================
# CONFIGURACIÓN
# =====================================================

MODELO_EMBEDDINGS = "paraphrase-multilingual-MiniLM-L12-v2"

# Si tienes muchos documentos, puedes poner un límite para hacer una prueba rápida.
# Por ejemplo: LIMITE_DOCUMENTOS = 1000
LIMITE_DOCUMENTOS = None

# Número máximo de tópicos que se etiquetan en la gráfica
MAX_TOPICOS_ETIQUETADOS = 15


# =====================================================
# CARGA DE DATOS
# =====================================================

df = pd.read_csv(ARCHIVO_DOCUMENTOS)
df_topicos = pd.read_csv(ARCHIVO_TOPICOS)

if "texto" not in df.columns:
    raise ValueError("No encuentro la columna 'texto' en documentos_con_topicos.csv")

if "topic" not in df.columns:
    raise ValueError("No encuentro la columna 'topic' en documentos_con_topicos.csv")

df = df.dropna(subset=["texto"]).copy()
df["texto"] = df["texto"].astype(str)
df["topic"] = df["topic"].astype(int)

if LIMITE_DOCUMENTOS is not None:
    df = df.sample(n=min(LIMITE_DOCUMENTOS, len(df)), random_state=42).copy()

docs = df["texto"].tolist()

print(f"Documentos/chunks cargados: {len(docs)}")
print("Tópicos encontrados:")
print(df["topic"].value_counts().sort_index())


# =====================================================
# CREAR ETIQUETAS DE TÓPICOS
# =====================================================

def obtener_palabras_topico(row):
    """
    Obtiene palabras asociadas al tópico desde topicos_bertopic.csv.
    Usa Representation si existe; si no, usa Name.
    """
    if "Representation" in row and pd.notna(row["Representation"]):
        valor = str(row["Representation"])
        valor = (
            valor.replace("[", "")
            .replace("]", "")
            .replace("'", "")
            .replace('"', "")
        )
        palabras = [p.strip() for p in valor.split(",") if p.strip()]
        return ", ".join(palabras[:5])

    if "Name" in row and pd.notna(row["Name"]):
        nombre = str(row["Name"])
        partes = nombre.split("_")
        if len(partes) > 1:
            return ", ".join(partes[1:6])
        return nombre

    return ""


# Normalizar nombre de columna
if "Topic" in df_topicos.columns:
    df_topicos = df_topicos.rename(columns={"Topic": "topic"})

if "topic" not in df_topicos.columns:
    raise ValueError("No encuentro la columna 'topic' o 'Topic' en topicos_bertopic.csv")

df_topicos["topic"] = df_topicos["topic"].astype(int)
df_topicos["palabras_topico"] = df_topicos.apply(obtener_palabras_topico, axis=1)

topic_to_words = dict(zip(df_topicos["topic"], df_topicos["palabras_topico"]))


# =====================================================
# EMBEDDINGS Y REDUCCIÓN A 2D
# =====================================================

print()
print("Calculando embeddings...")
embedding_model = SentenceTransformer(MODELO_EMBEDDINGS)

embeddings = embedding_model.encode(
    docs,
    show_progress_bar=True,
    batch_size=32
)

print()
print("Reduciendo a 2D con UMAP...")

umap_2d = UMAP(
    n_neighbors=15,
    n_components=2,
    min_dist=0.05,
    metric="cosine",
    random_state=42
)

coords = umap_2d.fit_transform(embeddings)

df["x"] = coords[:, 0]
df["y"] = coords[:, 1]
df["palabras_topico"] = df["topic"].map(topic_to_words)

df.to_csv(SALIDA_CSV, index=False, encoding="utf-8-sig")

print(f"Coordenadas guardadas en: {SALIDA_CSV}")


# =====================================================
# GRÁFICA DE PUNTOS
# =====================================================

plt.figure(figsize=(14, 10))

topicos = sorted(df["topic"].unique())

# Dibujar primero el tópico -1, si existe, como ruido
if -1 in topicos:
    df_ruido = df[df["topic"] == -1]
    plt.scatter(
        df_ruido["x"],
        df_ruido["y"],
        s=18,
        alpha=0.25,
        label="Ruido / sin tópico (-1)"
    )

# Dibujar el resto de tópicos
for topic in topicos:
    if topic == -1:
        continue

    df_t = df[df["topic"] == topic]

    palabras = topic_to_words.get(topic, "")
    label = f"Tópico {topic}: {palabras}" if palabras else f"Tópico {topic}"

    plt.scatter(
        df_t["x"],
        df_t["y"],
        s=28,
        alpha=0.75,
        label=label
    )


# =====================================================
# ETIQUETAR CENTROS DE LOS TÓPICOS PRINCIPALES
# =====================================================

conteo_topicos = (
    df[df["topic"] != -1]
    .groupby("topic")
    .size()
    .sort_values(ascending=False)
    .head(MAX_TOPICOS_ETIQUETADOS)
)

for topic in conteo_topicos.index:
    df_t = df[df["topic"] == topic]

    centro_x = df_t["x"].median()
    centro_y = df_t["y"].median()

    palabras = topic_to_words.get(topic, "")
    etiqueta = f"{topic}"
    if palabras:
        etiqueta = f"{topic}\n{palabras}"

    plt.text(
        centro_x,
        centro_y,
        etiqueta,
        fontsize=9,
        ha="center",
        va="center",
        bbox=dict(
            boxstyle="round,pad=0.3",
            facecolor="white",
            edgecolor="gray",
            alpha=0.8
        )
    )


# =====================================================
# FORMATO
# =====================================================

plt.title(
    "Mapa semántico de tópicos con BERTopic",
    fontsize=18
)

plt.suptitle(
    "Cada punto representa un fragmento de 200-300 palabras; la cercanía indica similitud semántica aproximada",
    fontsize=11,
    y=0.93
)

plt.xlabel("Dimensión UMAP 1")
plt.ylabel("Dimensión UMAP 2")

plt.xticks([])
plt.yticks([])

# Si hay muchos tópicos, la leyenda puede ocupar demasiado.
# Por eso la ponemos fuera de la gráfica.
plt.legend(
    loc="center left",
    bbox_to_anchor=(1.02, 0.5),
    fontsize=8,
    frameon=False,
    markerscale=1.2
)

plt.tight_layout()

plt.savefig(SALIDA_PNG, dpi=300, bbox_inches="tight")
plt.close()

print(f"Gráfica creada: {SALIDA_PNG}")
print("Proceso terminado.")