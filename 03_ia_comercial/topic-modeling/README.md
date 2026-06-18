# Topic modeling

Este directorio reúne el proceso y los resultados de **modelado de temas** aplicado a los tres corpus de revistas históricas en español (*Fémina*, *Filipinas* y *El Heraldo de la Mujer*).

## Estructura de la carpeta

```text
topic_modeling/
└── gemini-3-flash-preview/
    ├── results-similarity/
    │   ├── mallet/
    │   |   ├── fémina/
    |   |   |   ├── 1a-iter.csv
    |   |   |   ├── 2a-iter.csv
    |   |   |   ...
    |   |   |   └── 5a-iter.csv
    |   |   ├── filipinas/
    |   |   |   ├── 1a-iter.csv
    |   |   |   ...
    |   |   ├── general/
    |   |   |   ├── 1a-iter.csv
    |   |   |   ...
    |   |   └── heraldo/
    |   |       ├── 1a-iter.csv
    |   |       ...
    │   └── voyant/
    │       ├── fémina/
    |       |   ├── 1a-iter.csv
    |       |   ...
    |       ├── filipinas/
    |       |   ├── 1a-iter.csv
    |       |   ...
    |       ├── general/
    |       |   ├── 1a-iter.csv
    |       |   ...
    |       └── heraldo/
    |           ├── 1a-iter.csv
    |           ...
    └── topics/
        ├── fémina/
        |   ├── 1a-iter.csv
        |   |   ...
        ├── filipinas/
        |   ├── 1a-iter.csv
        |   |   ...
        ├── general/
        |   ├── 1a-iter.csv
        |   |   ...
        └── heraldo/
            ├── 1a-iter.csv
            ...
```

---

## Flujo de trabajo

### 1. Preparación del corpus

Los textos analizados son los archivos `.txt` de transcripciones generadas con **Transkribus**, posteriormente unidos y reconstruidos mediante un script de Python que combina los archivos y repara artefactos de OCR habitaules como guones de partición de palabra (`-`, `¬`). El resultado es un único archivo de texto por revista, listo para el análisis.

### 2. Modelado de temas con Gemini

El modelado se realizó en **Google AI Studio** con el modelo **Gemini 2.0 Flash Preview**, usando la configuración predeterminada de la plataforma. Se empleó el mismo prompt para todas las iteraciones y publicaciones, disponible en `03_ia_comercial/prompts/prompt-topic.txt`. El prompt solicitaba la salida en formato CSV con tres campos por tópico:

- `nombre-tópico`: etiqueta descriptiva del tema
- `palabras-clave`: 8 palabras representativas
- `porcentaje-presencia`: peso estimado del tópico en el corpus

Se abrió un **chat independiente por iteración**, sin reutilizar contexto entre sesiones, para garantizar la independencia de cada ejecución. Cuando la respuesta estaba incompleta o no respetaba el formato solicitado, se regeneró dentro del mismo chat hasta obtener un resultado válido.

Se realizaron **5 iteraciones por revista** (*Fémina*, *Filipinas*, *El Heraldo de la Mujer*) y **5 iteraciones adicionales sobre el corpus general** (las tres revistas combinadas), totalizando 20 ejecuciones. El objetivo de las iteraciones múltiples es evaluar la **estabilidad del modelo**: cuanto más consistentes sean los tópicos entre iteraciones, más robustos se consideran los resultados.

Los resultados brutos de cada iteración se almacenan en `topics/<revista>/Xa-iter.csv`.

### 3. Validación: similitud con referencias externas

Para validar los tópicos obtenidos, se calculó su similitud con dos conjuntos de referencia de palabras clave extraídas independientemente del mismo corpus:

- **Voyant Tools**: palabras clave estadísticas extraídas mediante la herramienta de análisis de texto Voyant.
- **MALLET**: palabras clave obtenidas con el modelo LDA clásico de MALLET.

La comparación se realizó mediante dos métricas de similitud coseno complementarias:

| Métrica | Descripción |
|---|---|
| **Similitud léxica** | Comparación directa de los vectores de palabras clave (representación bag-of-words) |
| **Similitud semántica** | Comparación de embeddings generados con `paraphrase-multilingual-MiniLM-L12-v2` (sentence-transformers), que captura proximidad de significado más allá de la coincidencia exacta de términos |

En ambos casos, cada tópico LDA se empareja con el tópico de referencia más similar (dirección LDA → referencia). Los resultados se guardan en `results-similarity/voyant/<revista>/Xa-iter.csv` y `results-similarity/mallet/<revista>/Xa-iter.csv` respectivamente.