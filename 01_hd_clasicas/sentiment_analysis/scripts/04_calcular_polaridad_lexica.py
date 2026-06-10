# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 19:27:00 2026

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


def normalize_term(term: str) -> str:
    term = term.lower()
    term = remove_accents(term)
    term = re.sub(r"[^a-zñáéíóúü0-9\s]", " ", term)
    term = re.sub(r"\s+", " ", term).strip()
    return term


def load_lexicon(path: Path, key: str) -> list[str]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    terms = data.get(key, [])
    return [normalize_term(term) for term in terms]


def count_terms(text: str, terms: list[str]) -> tuple[int, list[str]]:
    found = []
    count = 0

    for term in terms:
        if not term:
            continue
        pattern = r"\b" + re.escape(term) + r"\b"
        matches = re.findall(pattern, text)
        if matches:
            count += len(matches)
            found.append(term)

    return count, sorted(set(found))


def label_polarity(score: int) -> str:
    if score > 0:
        return "positiva"
    if score < 0:
        return "negativa"
    return "neutra"


def main():
    parser = argparse.ArgumentParser(
        description="Calcula polaridad léxica por frase."
    )
    parser.add_argument("--input", required=True, help="CSV de frases limpias.")
    parser.add_argument("--positive", required=True, help="YAML con léxico positivo.")
    parser.add_argument("--negative", required=True, help="YAML con léxico negativo.")
    parser.add_argument("--output", required=True, help="CSV de salida con polaridad por frase.")

    args = parser.parse_args()

    input_path = Path(args.input)
    positive_path = Path(args.positive)
    negative_path = Path(args.negative)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)

    positive_terms = load_lexicon(positive_path, "positivo")
    negative_terms = load_lexicon(negative_path, "negativo")

    rows = []

    for _, row in df.iterrows():
        text = str(row["frase_normalizada"])

        n_pos, pos_found = count_terms(text, positive_terms)
        n_neg, neg_found = count_terms(text, negative_terms)

        raw_score = n_pos - n_neg
        n_words = int(row["n_palabras"]) if row["n_palabras"] else 0
        normalized_score = raw_score / n_words if n_words > 0 else 0

        rows.append({
            "sentence_id": row["sentence_id"],
            "documento": row["documento"],
            "orden_frase": row["orden_frase"],
            "frase_original": row["frase_original"],
            "frase_normalizada": row["frase_normalizada"],
            "n_palabras": n_words,
            "n_positivo": n_pos,
            "n_negativo": n_neg,
            "polaridad_bruta": raw_score,
            "polaridad_normalizada": normalized_score,
            "etiqueta_polaridad": label_polarity(raw_score),
            "palabras_positivas_detectadas": "; ".join(pos_found),
            "palabras_negativas_detectadas": "; ".join(neg_found)
        })

    out_df = pd.DataFrame(rows)
    out_df.to_csv(output_path, index=False, encoding="utf-8")

    print(f"Archivo creado: {output_path}")
    print(out_df["etiqueta_polaridad"].value_counts())


if __name__ == "__main__":
    main()