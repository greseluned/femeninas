import argparse
from pathlib import Path

import pandas as pd
from pysentimiento import create_analyzer


def read_sentences(txt_path: Path) -> list[str]:
    text = txt_path.read_text(encoding="utf-8", errors="ignore")
    lines = [line.strip() for line in text.splitlines()]
    return [line for line in lines if line]


def main():
    parser = argparse.ArgumentParser(
        description="Análisis de sentimientos con pysentimiento/RoBERTuito."
    )
    parser.add_argument("--input", required=True, help="Ruta al archivo TXT estructurado por frases.")
    parser.add_argument("--document", required=True, help="Nombre del documento.")
    parser.add_argument("--output", required=True, help="Ruta del CSV de salida.")
    parser.add_argument("--batch_size", type=int, default=32, help="Tamaño de lote.")

    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Leyendo frases de: {input_path}")
    sentences = read_sentences(input_path)

    print(f"Número de frases: {len(sentences)}")
    print("Cargando analizador de sentimientos de pysentimiento...")
    analyzer = create_analyzer(task="sentiment", lang="es")

    rows = []

    for start in range(0, len(sentences), args.batch_size):
        batch = sentences[start:start + args.batch_size]

        for i, sentence in enumerate(batch, start=start + 1):
            result = analyzer.predict(sentence)

            # result.output suele ser POS, NEG o NEU
            # result.probas contiene las probabilidades por etiqueta
            probas = result.probas

            rows.append({
                "sentence_id": f"{args.document.lower()}_{i:06d}",
                "documento": args.document,
                "orden_frase": i,
                "frase": sentence,
                "sentimiento": result.output,
                "score_pos": probas.get("POS", None),
                "score_neg": probas.get("NEG", None),
                "score_neu": probas.get("NEU", None)
            })

        print(f"Procesadas {min(start + args.batch_size, len(sentences))} / {len(sentences)} frases")

    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False, encoding="utf-8")

    print(f"Archivo creado: {output_path}")


if __name__ == "__main__":
    main()