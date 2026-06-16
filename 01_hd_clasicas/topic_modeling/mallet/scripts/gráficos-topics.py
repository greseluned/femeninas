from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Ejecutar este script desde:
# 01_hd_clasicas/topic_modeling/mallet

BASE_DIR = Path(__file__).resolve().parents[1]

CLAVES_DIR = BASE_DIR / "claves_topicos"
COMPOSICION_DIR = BASE_DIR / "composicion_documentos"
GRAFICOS_DIR = BASE_DIR / "graficos"

GRAFICOS_DIR.mkdir(exist_ok=True)

periodicos = ["femina", "filipinas", "heraldo"]

for periodico in periodicos:
    archivo_claves = CLAVES_DIR / f"claves_topicos_{periodico}.txt"
    archivo_composicion = COMPOSICION_DIR / f"composicion_documentos_{periodico}.txt"
    archivo_salida = GRAFICOS_DIR / f"grafico_topicos_{periodico}.png"

    # Leer claves de tópicos
    topicos = {}
    with open(archivo_claves, "r", encoding="utf-8") as f:
        for linea in f:
            partes = linea.strip().split("\t")
            if len(partes) >= 3:
                topic_id = int(partes[0])
                palabras = partes[2]
                topicos[topic_id] = palabras

    # Leer composición documental
    df = pd.read_csv(
        archivo_composicion,
        sep="\t",
        header=None,
        comment="#"
    )

    # En los archivos de MALLET, las dos primeras columnas suelen ser:
    # 0 = identificador del documento
    # 1 = nombre/ruta del documento
    # A partir de la columna 2 aparecen pares topic_id / peso
    topic_scores = {topic_id: 0 for topic_id in topicos.keys()}
    topic_counts = {topic_id: 0 for topic_id in topicos.keys()}

    for _, row in df.iterrows():
        valores = row.iloc[2:].dropna().tolist()

        for i in range(0, len(valores), 2):
            topic_id = int(valores[i])
            peso = float(valores[i + 1])

            if topic_id in topic_scores:
                topic_scores[topic_id] += peso
                topic_counts[topic_id] += 1

    prevalencias = {
        topic_id: topic_scores[topic_id] / topic_counts[topic_id]
        for topic_id in topic_scores
        if topic_counts[topic_id] > 0
    }

    datos = pd.DataFrame({
        "topic_id": list(prevalencias.keys()),
        "prevalencia": list(prevalencias.values()),
        "palabras": [topicos[topic_id] for topic_id in prevalencias.keys()]
    })

    datos = datos.sort_values("prevalencia", ascending=True)

    plt.figure(figsize=(10, 6))
    plt.barh(
        datos["palabras"],
        datos["prevalencia"]
    )
    plt.xlabel("Proporción en el corpus (media de presencia por frase)")
    plt.ylabel("Tópico")
    plt.title(f"Prevalencia de tópicos en {periodico}")
    plt.tight_layout()
    plt.savefig(archivo_salida, dpi=300)
    plt.close()

    print(f"Gráfico guardado: {archivo_salida}")