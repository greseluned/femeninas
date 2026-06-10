import argparse
import pandas as pd
from pathlib import Path


def read_sentences(txt_path: Path) -> list[str]:
    text = txt_path.read_text(encoding="utf-8", errors="ignore")
    lines = [line.strip() for line in text.splitlines()]
    sentences = [line for line in lines if line]
    return sentences


def main():
    parser = argparse.ArgumentParser(
        description="Convierte un TXT estructurado por frases en una tabla CSV."
    )
    parser.add_argument("--input", required=True, help="Ruta al archivo TXT.")
    parser.add_argument("--document", required=True, help="Nombre del documento: Femina, Filipinas o Heraldo.")
    parser.add_argument("--output", required=True, help="Ruta del CSV de salida.")

    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    sentences = read_sentences(input_path)

    rows = []
    for i, sentence in enumerate(sentences, start=1):
        rows.append({
            "sentence_id": f"{args.document.lower()}_{i:06d}",
            "documento": args.document,
            "orden_frase": i,
            "frase_original": sentence
        })

    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False, encoding="utf-8")

    print(f"Archivo creado: {output_path}")
    print(f"Número de frases: {len(df)}")


if __name__ == "__main__":
    main()