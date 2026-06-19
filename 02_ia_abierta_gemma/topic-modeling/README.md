# Topic modeling con Gemma 4 E4B (AnythingLLM)

Este directorio reúne el proceso y los resultados de **modelado de temas** aplicado a los tres corpus de revistas históricas en español (*Fémina*, *Filipinas* y *El Heraldo de la Mujer*), usando el modelo local **Gemma 4 E4B** a través de **AnythingLLM**.

Se probaron dos modalidades de embedding (*chunk* y *pinned*) para comparar cómo la forma de suministrar el texto al modelo afecta a los tópicos extraídos.

## Estructura de la carpeta

```text
02_ia_abierta_gemma/
├── prompts/
│   ├── prompt-topics-general.txt
│   └── prompt-topics-individual.txt
└── topic-modeling/
    ├── gemma-e4b-chunk/
    │   ├── results-similarity/
    │   │   ├── mallet/
    │   │   │   ├── femina/
    │   │   │   │   ├── 1a-iter.csv
    │   │   │   │   ...
    │   │   │   │   └── 5a-iter.csv
    │   │   │   ├── filipinas/
    │   │   │   │   ├── 1a-iter.csv
    │   │   │   │   ...
    │   │   │   ├── general/
    │   │   │   │   ├── 1a-iter.csv
    │   │   │   │   ...
    │   │   │   └── heraldo-de-la-mujer/
    │   │   │       ├── 1a-iter.csv
    │   │   │       ...
    │   │   └── voyant/
    │   │       ├── femina/
    │   │       │   ├── 1a-iter.csv
    │   │       │   ...
    │   │       ├── filipinas/
    │   │       │   ├── 1a-iter.csv
    │   │       │   ...
    │   │       ├── general/
    │   │       │   ├── 1a-iter.csv
    │   │       │   ...
    │   │       └── heraldo-de-la-mujer/
    │   │           ├── 1a-iter.csv
    │   │           ...
    │   └── topics/
    │       ├── femina/
    │       │   ├── 1a-iter.csv
    │       │   ...
    │       ├── filipinas/
    │       │   ├── 1a-iter.csv
    │       │   ...
    │       ├── general/
    │       │   ├── 1a-iter.csv
    │       │   ...
    │       └── heraldo-de-la-mujer/
    │           ├── 1a-iter.csv
    │           ...
    └── gemma-e4b-pinned/
        ├── results-similarity/
        │   ├── mallet/
        │   │   ├── femina/
        │   │   │   ├── 1a-iter.csv
        │   │   │   ...
        │   │   │   └── 5a-iter.csv
        │   │   ├── filipinas/
        │   │   │   ├── 1a-iter.csv
        │   │   │   ...
        │   │   ├── general/
        │   │   │   ├── 1a-iter.csv
        │   │   │   ...
        │   │   └── heraldo-de-la-mujer/
        │   │       ├── 1a-iter.csv
        │   │       ...
        │   └── voyant/
        │       ├── femina/
        │       │   ├── 1a-iter.csv
        │       │   ...
        │       ├── filipinas/
        │       │   ├── 1a-iter.csv
        │       │   ...
        │       ├── general/
        │       │   ├── 1a-iter.csv
        │       │   ...
        │       └── heraldo-de-la-mujer/
        │           ├── 1a-iter.csv
        │           ...
        └── topics/
            ├── femina/
            │   ├── 1a-iter.csv
            │   ...
            ├── filipinas/
            │   ├── 1a-iter.csv
            │   ...
            ├── general/
            │   ├── 1a-iter.csv
            │   ...
            └── heraldo-de-la-mujer/
                ├── 1a-iter.csv
                ...
```

---

## Flujo de trabajo

### 1. Preparación del corpus

Los textos analizados son los archivos `.txt` de transcripciones generadas con **Transkribus**. Los resultados de este experimento provienen de documentos procesados **individualmente** (no del archivo unificado por revista), y en el caso de *Fémina* se incorporaron documentos adicionales que no forman parte del corpus definitivo del proyecto.

Los resultados aquí recogidos deben interpretarse como **resultados preliminares**, obtenidos en una fase exploratoria anterior a la fijación definitiva del corpus.

### 2. Modelado de temas con Gemma 4 E4B

El modelado se realizó en **AnythingLLM** con el modelo local **Gemma 4 E4B**, usando la configuración predeterminada de la plataforma: ventana de contexto de 4 fragmentos de 1000 tokens cada uno. Se emplearon dos prompts distintos según el alcance del análisis, disponibles en `prompts/`:

- `prompt-topics-individual.txt` — para el análisis por revista individual
- `prompt-topics-general.txt` — para el análisis del corpus combinado

Ambos prompts solicitaban la salida en formato tabla con cuatro campos por tópico:

- `nombre-tópico`: etiqueta descriptiva del tema
- `palabras-clave`: 8 palabras representativas
- `porcentaje-presencia`: peso estimado del tópico en el corpus
- `fragmentos`: al menos dos fragmentos textuales representativos **por tópico**, tomados directamente de los documentos analizados.

Se abrió un **chat independiente por iteración**, sin reutilizar contexto entre sesiones, para garantizar la independencia de cada ejecución. Cuando la respuesta estaba incompleta o no respetaba el formato solicitado, se regeneró dentro del mismo chat hasta obtener un resultado válido.

Se realizaron **5 iteraciones por revista** (*Fémina*, *Filipinas*, *El Heraldo de la Mujer*) y **5 iteraciones adicionales sobre el corpus general** (las tres revistas combinadas), 20 ejecuciones por modalidad en total. El objetivo de las iteraciones múltiples es evaluar la **estabilidad del modelo**: cuanto más consistentes sean los tópicos entre iteraciones, más robustos se consideran los resultados.

Los resultados brutos de cada iteración se almacenan en `topics/<revista>/Xa-iter.csv`.

### 3. Modalidades de embedding: *chunk* vs. *pinned*

El flujo de modelado descrito arriba se ejecutó en dos modalidades distintas, que se diferencian exclusivamente en la forma en que AnythingLLM suministra el texto al modelo:

| Modalidad | Descripción | Carpeta |
|---|---|---|
| **chunk** | El texto se divide en fragmentos y el modelo accede solo a los chunks más relevantes para cada consulta mediante búsqueda por similitud semántica | `gemma-e4b-chunk/` |
| **pinned** | El documento completo se fija en el contexto del chat, haciendo el texto íntegro visible para el modelo en cada iteración | `gemma-e4b-pinned/` |

La comparación entre ambas modalidades permite valorar en qué medida la granularidad del acceso al texto influye en los tópicos extraídos y en la coherencia temática de los resultados.

> **Limitación conocida:** En la modalidad *pinned*, el análisis del corpus general (`gemma-e4b-pinned/general/`) solo cuenta con **3 iteraciones completas** en lugar de 5, debido a problemas técnicos durante la ejecución. Los resultados de esa subcarpeta deben tomarse con cautela al comparar la estabilidad con el resto de subcorpora.

### 4. Validación: similitud con referencias externas

Para validar los tópicos obtenidos, se calculó su similitud con dos conjuntos de referencia de palabras clave extraídas independientemente del mismo corpus:

- **Voyant Tools**: palabras clave estadísticas extraídas mediante la herramienta de análisis de texto Voyant.
- **MALLET**: palabras clave obtenidas con el modelo LDA clásico de MALLET.

La comparación se realizó mediante dos métricas de similitud coseno complementarias:

| Métrica | Descripción |
|---|---|
| **Similitud léxica** | Comparación directa de los vectores de palabras clave (representación bag-of-words) |
| **Similitud semántica** | Comparación de embeddings generados con `paraphrase-multilingual-MiniLM-L12-v2` (sentence-transformers), que captura proximidad de significado más allá de la coincidencia exacta de términos |

En ambos casos, cada tópico extraído por Gemma se empareja con el tópico de referencia más similar (dirección Gemma → referencia). Los resultados se guardan en `results-similarity/voyant/<revista>/Xa-iter.csv` y `results-similarity/mallet/<revista>/Xa-iter.csv` para la modalidad *chunk*, y en las carpetas equivalentes bajo `relation-similarity/` para la modalidad *pinned*.

---