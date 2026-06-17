import argparse
import re
import unicodedata
from pathlib import Path

import pandas as pd
import yaml
import matplotlib.pyplot as plt


# ------------------------------------------------------------
# Funciones auxiliares
# ------------------------------------------------------------

def remove_accents(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text)
    return "".join(char for char in normalized if unicodedata.category(char) != "Mn")


def normalize_text(text: str) -> str:
    text = str(text).lower()
    text = remove_accents(text)
    text = re.sub(r"[^a-zñ0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_topics(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        topics = yaml.safe_load(f)
    if not isinstance(topics, dict):
        raise ValueError("El archivo de temas debe tener formato diccionario YAML.")
    return topics


def keyword_in_text(keyword: str, text: str) -> bool:
    keyword_norm = normalize_text(keyword)
    if not keyword_norm:
        return False
    pattern = r"\b" + re.escape(keyword_norm) + r"\b"
    return re.search(pattern, text) is not None


def detect_topics_for_sentence(sentence: str, topics: dict) -> list[tuple[str, str]]:
    sentence_norm = normalize_text(sentence)
    detected = []

    for topic, keywords in topics.items():
        for keyword in keywords:
            if keyword_in_text(keyword, sentence_norm):
                detected.append((topic, keyword))

    return detected


def sentiment_label_to_spanish(label: str) -> str:
    mapping = {
        "POS": "positivo",
        "NEG": "negativo",
        "NEU": "neutro",
        "positivo": "positivo",
        "negativo": "negativo",
        "neutro": "neutro",
    }
    return mapping.get(str(label), str(label))


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# Crear tabla con temas
# ------------------------------------------------------------

def create_sentiment_topics_table(df: pd.DataFrame, topics: dict, include_no_topic: bool = False) -> pd.DataFrame:
    rows = []

    for _, row in df.iterrows():
        sentence = row["frase"]
        detected_topics = detect_topics_for_sentence(sentence, topics)

        if not detected_topics and include_no_topic:
            detected_topics = [("sin_tema", "")]

        for topic, keyword in detected_topics:
            rows.append({
                "sentence_id": row["sentence_id"],
                "documento": row["documento"],
                "orden_frase": row["orden_frase"],
                "frase": row["frase"],
                "tema": topic,
                "keyword_detectada": keyword,
                "sentimiento": sentiment_label_to_spanish(row["sentimiento"]),
                "score_pos": row.get("score_pos", None),
                "score_neg": row.get("score_neg", None),
                "score_neu": row.get("score_neu", None),
            })

    return pd.DataFrame(rows)


# ------------------------------------------------------------
# Gráfico 1: polaridad por temas para un periódico
# ------------------------------------------------------------

def plot_sentiment_by_topic(df_topics: pd.DataFrame, document: str, output_path: Path):
    if df_topics.empty:
        print(f"No hay datos temáticos para {document}. No se crea gráfico de polaridad por temas.")
        return

    counts = (
        df_topics.groupby(["tema", "sentimiento"])
        .size()
        .reset_index(name="n_frases")
    )

    pivot = counts.pivot_table(
        index="tema",
        columns="sentimiento",
        values="n_frases",
        fill_value=0
    )

    for col in ["positivo", "negativo", "neutro"]:
        if col not in pivot.columns:
            pivot[col] = 0

    pivot["total"] = pivot[["positivo", "negativo", "neutro"]].sum(axis=1)
    pivot = pivot.sort_values("total", ascending=False)

    plot_df = pivot[["positivo", "negativo", "neutro"]]

    ax = plot_df.plot(kind="bar", figsize=(12, 7))

    ax.set_title(f"{document}: distribución de sentimiento por tema")
    ax.set_xlabel("Tema")
    ax.set_ylabel("Número de frases")
    ax.legend(title="Sentimiento")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Gráfico creado: {output_path}")


# ------------------------------------------------------------
# Gráfico 2: temas más utilizados por periódico
# ------------------------------------------------------------

def plot_top_topics(df_topics: pd.DataFrame, document: str, output_path: Path, top_n: int = 15):
    if df_topics.empty:
        print(f"No hay datos temáticos para {document}. No se crea gráfico de temas.")
        return

    topic_counts = (
        df_topics.groupby("tema")["sentence_id"]
        .nunique()
        .reset_index(name="n_frases")
        .sort_values("n_frases", ascending=False)
        .head(top_n)
        .sort_values("n_frases", ascending=True)
    )

    plt.figure(figsize=(10, 7))
    plt.barh(topic_counts["tema"], topic_counts["n_frases"])
    plt.title(f"{document}: temas más frecuentes")
    plt.xlabel("Número de frases asociadas al tema")
    plt.ylabel("Tema")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Gráfico creado: {output_path}")


# ------------------------------------------------------------
# Gráfico 3: resumen de los tres periódicos
# ------------------------------------------------------------

def plot_summary_three_documents(all_topics_df: pd.DataFrame, output_path: Path):
    if all_topics_df.empty:
        print("No hay datos temáticos globales. No se crea gráfico resumen.")
        return

    resumen = (
        all_topics_df.groupby(["documento", "sentimiento"])
        .size()
        .reset_index(name="n_frases")
    )

    pivot = resumen.pivot_table(
        index="documento",
        columns="sentimiento",
        values="n_frases",
        fill_value=0
    )

    for col in ["positivo", "negativo", "neutro"]:
        if col not in pivot.columns:
            pivot[col] = 0

    pivot = pivot[["positivo", "negativo", "neutro"]]

    ax = pivot.plot(kind="bar", figsize=(10, 6))

    ax.set_title("Resumen comparativo: sentimiento en frases temáticas")
    ax.set_xlabel("Periódico")
    ax.set_ylabel("Número de frases")
    ax.legend(title="Sentimiento")

    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Gráfico creado: {output_path}")


# ------------------------------------------------------------
# Tablas agregadas
# ------------------------------------------------------------

def save_aggregated_tables(df_topics: pd.DataFrame, output_dir: Path):
    ensure_dir(output_dir)

    if df_topics.empty:
        return

    # Tabla 1: sentimiento por tema y documento
    sentiment_topic_doc = (
        df_topics.groupby(["documento", "tema", "sentimiento"])
        .size()
        .reset_index(name="n_frases")
    )

    sentiment_topic_doc.to_csv(
        output_dir / "sentiment_robertuito_por_tema_y_documento.csv",
        index=False,
        encoding="utf-8"
    )

    # Tabla 2: temas por documento
    topics_doc = (
        df_topics.groupby(["documento", "tema"])["sentence_id"]
        .nunique()
        .reset_index(name="n_frases")
        .sort_values(["documento", "n_frases"], ascending=[True, False])
    )

    topics_doc.to_csv(
        output_dir / "temas_por_documento.csv",
        index=False,
        encoding="utf-8"
    )

    # Tabla 3: resumen por documento y sentimiento
    sentiment_doc = (
        df_topics.groupby(["documento", "sentimiento"])
        .size()
        .reset_index(name="n_frases")
    )

    sentiment_doc.to_csv(
        output_dir / "sentiment_robertuito_resumen_tres_periodicos.csv",
        index=False,
        encoding="utf-8"
    )

    print(f"Tablas agregadas guardadas en: {output_dir}")


# ------------------------------------------------------------
# Programa principal
# ------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Genera visualizaciones de sentimiento RoBERTuito por temas."
    )

    parser.add_argument(
        "--femina",
        required=True,
        help="CSV sentiment_robertuito_frases.csv de Fémina."
    )

    parser.add_argument(
        "--filipinas",
        required=True,
        help="CSV sentiment_robertuito_frases.csv de Filipinas."
    )

    parser.add_argument(
        "--heraldo",
        required=True,
        help="CSV sentiment_robertuito_frases.csv de El Heraldo de la Mujer."
    )

    parser.add_argument(
        "--topics",
        required=True,
        help="Archivo YAML con temas y palabras clave."
    )

    parser.add_argument(
        "--outfig",
        required=True,
        help="Carpeta donde se guardarán los gráficos."
    )

    parser.add_argument(
        "--outresults",
        required=True,
        help="Carpeta donde se guardarán tablas agregadas."
    )

    parser.add_argument(
        "--top_n",
        type=int,
        default=15,
        help="Número de temas a mostrar en los gráficos de temas frecuentes."
    )

    parser.add_argument(
        "--include_no_topic",
        action="store_true",
        help="Incluye frases sin tema como 'sin_tema'. Por defecto se excluyen."
    )

    args = parser.parse_args()

    topics = load_topics(Path(args.topics))

    files = {
        "Fémina": Path(args.femina),
        "Filipinas": Path(args.filipinas),
        "El Heraldo de la Mujer": Path(args.heraldo),
    }

    figures_dir = Path(args.outfig)
    results_dir = Path(args.outresults)

    ensure_dir(figures_dir)
    ensure_dir(results_dir)

    all_topics_tables = []

    for document_name, csv_path in files.items():
        print(f"\nProcesando {document_name}: {csv_path}")

        df = pd.read_csv(csv_path)

        required_columns = {"sentence_id", "documento", "orden_frase", "frase", "sentimiento"}
        missing = required_columns - set(df.columns)

        if missing:
            raise ValueError(
                f"Faltan columnas en {csv_path}: {missing}. "
                "El CSV debe proceder de sentiment_robertuito_frases.csv."
            )

        df_topics = create_sentiment_topics_table(
            df,
            topics,
            include_no_topic=args.include_no_topic
        )

        safe_name = (
            document_name.lower()
            .replace("é", "e")
            .replace(" ", "_")
            .replace("la_", "")
            .replace("de_", "")
        )

        document_results_dir = results_dir / safe_name
        document_figures_dir = figures_dir / safe_name

        ensure_dir(document_results_dir)
        ensure_dir(document_figures_dir)

        # Guardar tabla con temas de cada documento
        df_topics.to_csv(
            document_results_dir / "sentiment_robertuito_con_temas.csv",
            index=False,
            encoding="utf-8"
        )

        # Gráfico de sentimiento por tema
        plot_sentiment_by_topic(
            df_topics=df_topics,
            document=document_name,
            output_path=document_figures_dir / "polaridad_por_temas_robertuito.png"
        )

        # Gráfico de temas más frecuentes
        plot_top_topics(
            df_topics=df_topics,
            document=document_name,
            output_path=document_figures_dir / "temas_mas_frecuentes.png",
            top_n=args.top_n
        )

        all_topics_tables.append(df_topics)

    # Tabla global
    all_topics_df = pd.concat(all_topics_tables, ignore_index=True)

    all_topics_df.to_csv(
        results_dir / "sentiment_robertuito_con_temas_todos.csv",
        index=False,
        encoding="utf-8"
    )

    # Tablas agregadas globales
    save_aggregated_tables(all_topics_df, results_dir)

    # Gráfico resumen global
    plot_summary_three_documents(
        all_topics_df=all_topics_df,
        output_path=figures_dir / "resumen_tres_periodicos_sentiment_robertuito.png"
    )

    print("\nProceso completado.")


if __name__ == "__main__":
    main()