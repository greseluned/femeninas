```python
# -*- coding: utf-8 -*-
"""
Prepara los textos del corpus para su importación en MALLET.

El script toma un archivo de texto continuo, normaliza los saltos de línea
y separa el contenido por frases. El resultado es un archivo en el que cada
frase ocupa una línea, lo que permite usar la frase como unidad documental
en el modelado de temas.
"""

from pathlib import Path
import re

# Ejecutar este script desde cualquier ubicación.
# Las rutas se calculan de forma relativa a la ubicación del propio script:
# 01_hd_clasicas/topic_modeling/mallet/scripts/preparar_texto.py

BASE_DIR = Path(__file__).resolve().parents[1]

MERGED_DIR = BASE_DIR / "corpus_merged"
SALIDA_DIR = BASE_DIR / "corpus_por_frases"

SALIDA_DIR.mkdir(exist_ok=True)

periodicos = ["femina", "filipinas", "heraldo"]

for periodico in periodicos:
    ruta_entrada = MERGED_DIR / f"{periodico}_merged.txt"
    ruta_salida = SALIDA_DIR / f"{periodico}_por_frases.txt"

    with open(ruta_entrada, "r", encoding="utf-8") as f:
        texto = f.read()

    # 1. Reemplaza saltos de línea internos por espacios.
    texto_continuo = re.sub(r"\s*\n\s*", " ", texto)

    # 2. Reemplaza múltiples espacios por uno solo.
    texto_continuo = re.sub(r"\s+", " ", texto_continuo)

    # 3. Separa por frases usando el punto seguido de espacio
    # y respetando mayúsculas, signos iniciales y letras acentuadas.
    frases = re.sub(
        r"\.\s+(?=[A-ZÁÉÍÓÚÑ¿¡])",
        ".\n",
        texto_continuo
    )

    # 4. Guarda el resultado listo para MALLET.
    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write(frases)

    print(f"Archivo procesado: {ruta_salida}")
```
