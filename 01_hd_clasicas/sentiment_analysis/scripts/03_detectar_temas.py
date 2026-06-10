# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 19:26:18 2026

@author: Rocio
"""

import argparse
import re
import yaml
import pandas as pd
from pathlib import Path
import unicodedata


def remove_accents(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text)
    return "".join(char for char in normalized if unicodedata.category(char) != "Mn")


def normalize_keyword(keyword: str) -> str:
    keyword = keyword.lower()
    keyword = remove_accents(keyword)
    keyword = re.sub(r"[^a-zñáéíóúü0-9\s]", " ", keyword)
    keyword = re.sub(r"\s+", " ", keyword).strip()
    return keyword


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def keyword_in_text(keyword: str, text: str) -> bool:
    pattern = r"\b" + re.escape(keyword) + r"\b"
    return re.search(pattern, text) is not None


def main():
    parser = argparse.ArgumentParser(
        description="Detecta temas en frases mediante listas de palabras clave."
    )
    parser.add_argument("--input", required=True, help="CSV de frases limpias.")
    parser.add_argument("--topics", required=True, help="Archivo YAML con temas y palabras clave.")
    parser.add_argument("--output", required=True, help="CSV de salida con frases y temas detectados.")
    parser.add_argument(
        "--include_no_topic",
        action="store_true",
        help="Incluye frases sin tema detectado con tema='sin_tema'."
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    topics_path = Path(args.topics)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)
    topics = load_yaml(topics_path)

    rows = []

    for _, row in df.iterrows():
        text = str(row["frase_normalizada"])
        found_any = False

        for tema, keywords in topics.items():
            for keyword in keywords:
                normalized_keyword = normalize_keyword(keyword)
                if normalized_keyword and keyword_in_text(normalized_keyword, text):
                    found_any = True
                    rows.append({
                        "sentence_id": row["sentence_id"],
                        "documento": row["documento"],
                        "orden_frase": row["orden_frase"],
                        "tema": tema,
                        "keyword_detectada": keyword,
                        "frase_original": row["frase_original"],
                        "frase_normalizada": row["frase_normalizada"],
                        "n_palabras": row["n_palabras"]
                    })

        if args.include_no_topic and not found_any:
            rows.append({
                "sentence_id": row["sentence_id"],
                "documento": row["documento"],
                "orden_frase": row["orden_frase"],
                "tema": "sin_tema",
                "keyword_detectada": "",
                "frase_original": row["frase_original"],
                "frase_normalizada": row["frase_normalizada"],
                "n_palabras": row["n_palabras"]
            })

    out_df = pd.DataFrame(rows)
    out_df.to_csv(output_path, index=False, encoding="utf-8")

    print(f"Archivo creado: {output_path}")
    print(f"Filas con tema detectado: {len(out_df)}")
    print("Temas detectados:")
    if len(out_df) > 0:
        print(out_df["tema"].value_counts())


if __name__ == "__main__":
    main()