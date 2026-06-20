import pandas as pd

from bertopic import BERTopic
from sentence_transformers import SentenceTransformer

from sklearn.feature_extraction.text import CountVectorizer
from umap import UMAP
from hdbscan import HDBSCAN


# =========================
# CONFIGURACIÓN
# =========================

INPUT_CSV = "corpus_revistas_chunks.csv"

OUTPUT_DOCS = "documentos_con_topicos.csv"
OUTPUT_TOPICS = "topicos_bertopic.csv"
OUTPUT_REVISTAS = "topicos_por_revista.csv"


# =========================
# STOPWORDS EN ESPAÑOL
# =========================

stopwords_es = [
    "a", "al", "algo", "algunas", "algunos", "ante", "antes", "como", "con",
    "contra", "cual", "cuando", "de", "del", "desde", "donde", "durante",
    "e", "el", "ella", "ellas", "ellos", "en", "entre", "era", "erais",
    "eran", "eras", "eres", "es", "esa", "esas", "ese", "eso", "esos",
    "esta", "estaba", "estaban", "estado", "estais", "estamos", "estan",
    "estar", "estará", "estas", "este", "esto", "estos", "estoy", "fue",
    "fueron", "ha", "había", "habían", "han", "hasta", "hay", "la", "las",
    "le", "les", "lo", "los", "más", "me", "mi", "mis", "mucho", "muy",
    "no", "nos", "nosotras", "nosotros", "nuestra", "nuestras", "nuestro",
    "nuestros", "o", "os", "otra", "otras", "otro", "otros", "para", "pero",
    "poco", "por", "porque", "que", "quien", "quienes", "se", "sea", "ser",
    "si", "sí", "sin", "sobre", "sois", "somos", "son", "soy", "su", "sus",
    "también", "tanto", "te", "teneis", "tenemos", "tener", "tengo", "ti",
    "tiene", "tienen", "todo", "todos", "tu", "tus", "un", "una", "unas",
    "uno", "unos", "vosotras", "vosotros", "vuestra", "vuestras", "vuestro",
    "vuestros", "y", "ya"
]

# Puedes añadir aquí ruido propio del OCR o de la prensa.
stopwords_extra = [
    "página", "pag", "núm", "num", "número", "numero",
    "revista", "señor", "señora", "señorita",
    "dicho", "dicha", "dichos", "dichas",
    "así", "pues", "tan", "vez", "cada",
    "usted", "ustedes"
]

stopwords_total = stopwords_es + stopwords_extra


# =========================
# CARGA DE DATOS
# =========================

df = pd.read_csv(INPUT_CSV)

df = df.dropna(subset=["texto"]).copy()
df["texto"] = df["texto"].astype(str)

# Eliminamos chunks demasiado cortos
df["n_palabras_reales"] = df["texto"].str.split().str.len()
df = df[df["n_palabras_reales"] >= 100].copy()

docs = df["texto"].tolist()

print(f"Documentos/chunks cargados: {len(docs)}")
print(df.groupby("revista").size())


# =========================
# MODELOS
# =========================

embedding_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

vectorizer_model = CountVectorizer(
    stop_words=stopwords_total,
    lowercase=True,
    ngram_range=(1, 2),
    min_df=2,
    max_df=0.85
)

umap_model = UMAP(
    n_neighbors=10,
    n_components=5,
    min_dist=0.0,
    metric="cosine",
    random_state=42
)

hdbscan_model = HDBSCAN(
    min_cluster_size=5,
    min_samples=1,
    metric="euclidean",
    cluster_selection_method="eom",
    prediction_data=True
)


topic_model = BERTopic(
    embedding_model=embedding_model,
    vectorizer_model=vectorizer_model,
    umap_model=umap_model,
    hdbscan_model=hdbscan_model,
    language="multilingual",
    min_topic_size=5,
    nr_topics=None,
    calculate_probabilities=True,
    verbose=True
)


# =========================
# ENTRENAMIENTO
# =========================

topics, probs = topic_model.fit_transform(docs)

df["topic"] = topics

topic_info = topic_model.get_topic_info()

print()
print("Resumen de tópicos:")
print(topic_info.head(30))


# =========================
# EXPORTAR RESULTADOS
# =========================

df.to_csv(OUTPUT_DOCS, index=False, encoding="utf-8-sig")
topic_info.to_csv(OUTPUT_TOPICS, index=False, encoding="utf-8-sig")


# Distribución de tópicos por revista
tabla_revistas = (
    df[df["topic"] != -1]
    .groupby(["revista", "topic"])
    .size()
    .reset_index(name="n_chunks")
)

tabla_revistas["porcentaje_en_revista"] = (
    tabla_revistas
    .groupby("revista")["n_chunks"]
    .transform(lambda x: x / x.sum() * 100)
)

tabla_revistas.to_csv(OUTPUT_REVISTAS, index=False, encoding="utf-8-sig")


# =========================
# MOSTRAR PALABRAS POR TÓPICO
# =========================

print()
print("Palabras principales por tópico:")
for topic_id in sorted(set(topics)):
    if topic_id == -1:
        continue

    print(f"\nTópico {topic_id}")
    palabras = topic_model.get_topic(topic_id)

    if palabras:
        for palabra, peso in palabras[:12]:
            print(f"  {palabra}: {peso:.4f}")


print()
print("Archivos creados:")
print(f"- {OUTPUT_DOCS}")
print(f"- {OUTPUT_TOPICS}")
print(f"- {OUTPUT_REVISTAS}")