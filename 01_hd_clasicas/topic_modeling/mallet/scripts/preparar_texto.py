# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 11:40:41 2026

@author: Rocio
"""

import os
import re

ruta_entrada = "C:/Users/Rocio/nuevo_corpus/merged/heraldo_merged.txt"
ruta_salida = "C:/Users/Rocio/nuevo_corpus/por_frases/heraldo_por_frases.txt"

with open(ruta_entrada, "r", encoding="utf-8") as f:
    texto = f.read()

# 1. Reemplaza saltos de línea internos por espacios (une las columnas rotas)
texto_continuo = re.sub(r'\s*\n\s*', ' ', texto)

# 2. Reemplaza múltiples espacios por uno solo
texto_continuo = re.sub(r'\s+', ' ', texto_continuo)

# 3. Separa por frases usando el punto seguido de espacio (y respetando mayúsculas)
# Esto añade un salto de línea (\n) después de cada punto
frases = re.sub(r'\.\s+(?=[A-ZÁÉÍÓÚÑ¿¡])', '.\n', texto_continuo)

# Guarda el resultado listo para MALLET
with open(ruta_salida, "w", encoding="utf-8") as f:
    f.write(frases)

print("¡Archivo procesado! Cada frase real ahora ocupa una línea.")