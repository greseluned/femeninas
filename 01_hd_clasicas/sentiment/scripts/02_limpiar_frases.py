# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 18:50:43 2026

@author: Rocio
"""

import argparse
import re
import unicodedata
import pandas as pd
from pathlib import Path


def remove_accents(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text)
    return "".join(char for char in normalized if unicodedata.category(char) != "Mn")


def normalize_text(text: str) -> str:
    text = text.lower()
    text = remove_accents(text)
    text = re.sub(r"[^a-zñáéíóúü0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def count_words(text: str) -> int:
    if not text:
        return 0
    return len(text.split())


def main():
    parser = argparse.ArgumentParser(
        description="Limpia y normaliza una tabla de frases."
    )
    parser.add_argument("--input", required=True, help="CSV creado por 01_crear_tabla_frases.py.")
    parser.add_argument("--output", required=True, help="CSV de salida con frases normalizadas.")
    parser.add_argument("--min_words", type=int, default=3, help="Número mínimo de palabras por frase.")

    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)

    df["frase_normalizada"] = df["frase_original"].fillna("").apply(normalize_text)
    df["n_palabras"] = df["frase_normalizada"].apply(count_words)

    df = df[df["n_palabras"] >= args.min_words].copy()

    df.to_csv(output_path, index=False, encoding="utf-8")

    print(f"Archivo creado: {output_path}")
    print(f"Frases conservadas: {len(df)}")


if __name__ == "__main__":
    main()