# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 19:27:30 2026

@author: Rocio
"""

import argparse
import pandas as pd
from pathlib import Path


def percentage(part, total):
    if total == 0:
        return 0
    return round((part / total) * 100, 2)


def main():
    parser = argparse.ArgumentParser(
        description="Cruza temas y polaridad y genera tablas agregadas."
    )
    parser.add_argument("--topics", required=True, help="CSV de frases con temas.")
    parser.add_argument("--polarity", required=True, help="CSV de frases con polaridad.")
    parser.add_argument("--outdir", required=True, help="Carpeta de resultados.")

    args = parser.parse_args()

    topics_path = Path(args.topics)
    polarity_path = Path(args.polarity)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    topics_df = pd.read_csv(topics_path)
    polarity_df = pd.read_csv(polarity_path)

    merged = topics_df.merge(
        polarity_df[
            [
                "sentence_id",
                "n_positivo",
                "n_negativo",
                "polaridad_bruta",
                "polaridad_normalizada",
                "etiqueta_polaridad",
                "palabras_positivas_detectadas",
                "palabras_negativas_detectadas"
            ]
        ],
        on="sentence_id",
        how="left"
    )

    merged_path = outdir / "frases_con_temas_y_polaridad.csv"
    merged.to_csv(merged_path, index=False, encoding="utf-8")

    documento = merged["documento"].iloc[0] if len(merged) > 0 else "documento"

    # 1. Menciones de temas
    menciones_tema = (
        merged.groupby(["documento", "tema"])
        .agg(
            n_frases_tema=("sentence_id", "nunique"),
            n_menciones_keywords=("keyword_detectada", "count")
        )
        .reset_index()
        .sort_values(["documento", "n_frases_tema"], ascending=[True, False])
    )

    total_frases_con_tema = merged["sentence_id"].nunique()
    menciones_tema["porcentaje_sobre_frases_con_tema"] = menciones_tema["n_frases_tema"].apply(
        lambda x: percentage(x, total_frases_con_tema)
    )

    menciones_tema.to_csv(
        outdir / "menciones_temas_por_documento.csv",
        index=False,
        encoding="utf-8"
    )

    # 2. Polaridad por documento completo
    polarity_total = pd.read_csv(polarity_path)

    total_sentences = len(polarity_total)
    counts = polarity_total["etiqueta_polaridad"].value_counts().to_dict()

    polaridad_documento = pd.DataFrame([{
        "documento": documento,
        "n_frases": total_sentences,
        "n_positivas": counts.get("positiva", 0),
        "n_negativas": counts.get("negativa", 0),
        "n_neutras": counts.get("neutra", 0),
        "porcentaje_positivas": percentage(counts.get("positiva", 0), total_sentences),
        "porcentaje_negativas": percentage(counts.get("negativa", 0), total_sentences),
        "porcentaje_neutras": percentage(counts.get("neutra", 0), total_sentences),
        "media_polaridad_bruta": round(polarity_total["polaridad_bruta"].mean(), 4),
        "media_polaridad_normalizada": round(polarity_total["polaridad_normalizada"].mean(), 6)
    }])

    polaridad_documento.to_csv(
        outdir / "polaridad_por_documento.csv",
        index=False,
        encoding="utf-8"
    )

    # 3. Polaridad por tema
    polaridad_tema = (
        merged.groupby(["documento", "tema"])
        .agg(
            n_frases=("sentence_id", "nunique"),
            media_polaridad_bruta=("polaridad_bruta", "mean"),
            media_polaridad_normalizada=("polaridad_normalizada", "mean"),
            total_positivo=("n_positivo", "sum"),
            total_negativo=("n_negativo", "sum")
        )
        .reset_index()
    )

    label_counts = (
        merged.groupby(["documento", "tema", "etiqueta_polaridad"])
        .size()
        .reset_index(name="count")
        .pivot_table(
            index=["documento", "tema"],
            columns="etiqueta_polaridad",
            values="count",
            fill_value=0
        )
        .reset_index()
    )

    for col in ["positiva", "negativa", "neutra"]:
        if col not in label_counts.columns:
            label_counts[col] = 0

    polaridad_tema = polaridad_tema.merge(
        label_counts,
        on=["documento", "tema"],
        how="left"
    )

    polaridad_tema = polaridad_tema.rename(columns={
        "positiva": "n_positivas",
        "negativa": "n_negativas",
        "neutra": "n_neutras"
    })

    polaridad_tema["porcentaje_positivas"] = polaridad_tema.apply(
        lambda row: percentage(row["n_positivas"], row["n_frases"]),
        axis=1
    )
    polaridad_tema["porcentaje_negativas"] = polaridad_tema.apply(
        lambda row: percentage(row["n_negativas"], row["n_frases"]),
        axis=1
    )
    polaridad_tema["porcentaje_neutras"] = polaridad_tema.apply(
        lambda row: percentage(row["n_neutras"], row["n_frases"]),
        axis=1
    )

    polaridad_tema = polaridad_tema.sort_values(
        ["documento", "n_frases"],
        ascending=[True, False]
    )

    polaridad_tema.to_csv(
        outdir / "polaridad_por_tema_y_documento.csv",
        index=False,
        encoding="utf-8"
    )

    # 4. Ejemplos para revisión manual
    ejemplos = (
        merged.sort_values(
            ["tema", "etiqueta_polaridad", "polaridad_bruta"],
            ascending=[True, True, False]
        )
        .groupby(["tema", "etiqueta_polaridad"])
        .head(10)
    )

    ejemplos.to_csv(
        outdir / "ejemplos_revision_manual.csv",
        index=False,
        encoding="utf-8"
    )

    print(f"Archivos creados en: {outdir}")
    print(f"- {merged_path}")
    print("- menciones_temas_por_documento.csv")
    print("- polaridad_por_documento.csv")
    print("- polaridad_por_tema_y_documento.csv")
    print("- ejemplos_revision_manual.csv")


if __name__ == "__main__":
    main()