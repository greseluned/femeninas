# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 19:28:05 2026

@author: Rocio
"""

import argparse
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def save_barh(df, x_col, y_col, title, xlabel, output_path):
    df = df.sort_values(x_col, ascending=True)

    plt.figure(figsize=(10, 6))
    plt.barh(df[y_col], df[x_col])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def main():
    parser = argparse.ArgumentParser(
        description="Genera gráficos para un documento a partir de las tablas agregadas."
    )
    parser.add_argument("--results", required=True, help="Carpeta de resultados del documento.")
    parser.add_argument("--figures", required=True, help="Carpeta donde guardar figuras.")
    parser.add_argument("--document", required=True, help="Nombre del documento.")

    args = parser.parse_args()

    results_dir = Path(args.results)
    figures_dir = Path(args.figures)
    figures_dir.mkdir(parents=True, exist_ok=True)

    menciones_path = results_dir / "menciones_temas_por_documento.csv"
    polaridad_tema_path = results_dir / "polaridad_por_tema_y_documento.csv"

    menciones = pd.read_csv(menciones_path)
    polaridad_tema = pd.read_csv(polaridad_tema_path)

    # 1. Frecuencia de temas
    save_barh(
        df=menciones,
        x_col="n_frases_tema",
        y_col="tema",
        title=f"{args.document}: menciones por tema",
        xlabel="Número de frases asociadas al tema",
        output_path=figures_dir / "frecuencia_temas.png"
    )

    # 2. Polaridad media por tema
    polaridad_sorted = polaridad_tema.sort_values("media_polaridad_normalizada", ascending=True)

    plt.figure(figsize=(10, 6))
    plt.barh(polaridad_sorted["tema"], polaridad_sorted["media_polaridad_normalizada"])
    plt.axvline(0, linestyle="--", linewidth=1)
    plt.title(f"{args.document}: polaridad léxica media por tema")
    plt.xlabel("Polaridad media normalizada")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(figures_dir / "polaridad_media_por_tema.png", dpi=300)
    plt.close()

    # 3. Distribución positiva / negativa / neutra por tema
    dist = polaridad_tema[
        ["tema", "n_positivas", "n_negativas", "n_neutras"]
    ].copy()

    dist = dist.set_index("tema")
    dist = dist.sort_values("n_positivas", ascending=False)

    ax = dist.plot(kind="bar", figsize=(12, 6))
    ax.set_title(f"{args.document}: distribución de polaridad por tema")
    ax.set_xlabel("Tema")
    ax.set_ylabel("Número de frases")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(figures_dir / "distribucion_polaridad_por_tema.png", dpi=300)
    plt.close()

    print(f"Figuras creadas en: {figures_dir}")
    print("- frecuencia_temas.png")
    print("- polaridad_media_por_tema.png")
    print("- distribucion_polaridad_por_tema.png")


if __name__ == "__main__":
    main()