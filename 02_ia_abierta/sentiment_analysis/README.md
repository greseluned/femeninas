# Análisis de sentimientos con RoBERTuito

Esta carpeta contiene el análisis de sentimientos realizado con `pysentimiento` y el modelo **RoBERTuito** sobre tres publicaciones periódicas del corpus:

* **Fémina**
* **Filipinas**
* **El Heraldo de la Mujer**

El análisis forma parte de los experimentos con modelos de lenguaje no generativos aplicados al corpus de prensa femenina hispánica. A diferencia de un análisis léxico basado en diccionarios manuales, este procedimiento utiliza un modelo transformer para clasificar frases en tres categorías de sentimiento:

* `POS`: positivo
* `NEG`: negativo
* `NEU`: neutro

El objetivo es observar cómo se distribuyen los sentimientos en las frases del corpus y cómo varía esa distribución cuando se cruza con una serie de temas de investigación.

## Estructura de la carpeta

```text
sentiment_analysis/
├── config/
├── figures/
├── results/
├── scripts/
└── README.md
```

## `config/`

Esta carpeta contiene los archivos de configuración necesarios para el análisis.

### `temas_keywords.yml`

Archivo con los temas de investigación y las palabras clave utilizadas para detectar esos temas en las frases del corpus.

Ejemplos de temas:

* mujer
* feminismo
* patria
* raza
* educación
* hogar
* religión
* colonialismo

El archivo permite asociar cada frase del corpus a uno o varios temas. Una frase puede aparecer en más de un tema si contiene palabras clave pertenecientes a varias categorías.

Este paso es necesario porque el archivo de sentimientos generado por RoBERTuito clasifica frases, pero no identifica temas por sí mismo.

## `scripts/`

Esta carpeta contiene los scripts utilizados para generar los resultados.

```text
scripts/
├── 01_sentiment_robertuito.py
└── 02_visualizar_sentiment_temas_robertuito.py
```

### `01_sentiment_robertuito.py`

Este script aplica el modelo de análisis de sentimientos de `pysentimiento` a un archivo `.txt` estructurado por frases.

El script procesa cada frase y genera un archivo CSV con:

* identificador de frase;
* documento;
* orden de la frase;
* frase original;
* etiqueta de sentimiento;
* probabilidad de sentimiento positivo;
* probabilidad de sentimiento negativo;
* probabilidad de sentimiento neutro.

Salida esperada para cada documento:

```text
results/femina/sentiment_robertuito_frases.csv
results/filipinas/sentiment_robertuito_frases.csv
results/el_heraldo_mujer/sentiment_robertuito_frases.csv
```

### `02_visualizar_sentiment_temas_robertuito.py`

Este script cruza los resultados del análisis de sentimientos con los temas definidos en `config/temas_keywords.yml`.

El script realiza varias tareas:

1. Lee los CSV generados por `01_sentiment_robertuito.py`.
2. Detecta los temas presentes en cada frase.
3. Crea tablas agregadas por tema, documento y sentimiento.
4. Genera visualizaciones por periódico.
5. Genera una visualización comparativa de los tres periódicos.

Este script no vuelve a calcular el sentimiento. Solo utiliza los resultados ya producidos por RoBERTuito y los cruza con las palabras clave temáticas.

## `results/`

Esta carpeta contiene los resultados tabulares del análisis.

```text
results/
├── el_heraldo_mujer/
├── femina/
├── filipinas/
├── sentiment_robertuito_con_temas_todos.csv
├── sentiment_robertuito_por_tema_y_documento.csv
├── sentiment_robertuito_resumen_tres_periodicos.csv
└── temas_por_documento.csv
```

### Carpetas por documento

Cada subcarpeta contiene los resultados específicos de cada periódico.

```text
results/femina/
results/filipinas/
results/el_heraldo_mujer/
```

El archivo principal de cada carpeta es:

```text
sentiment_robertuito_frases.csv
```

Este archivo contiene la clasificación frase por frase realizada por RoBERTuito.

Columnas principales:

```text
sentence_id
documento
orden_frase
frase
sentimiento
score_pos
score_neg
score_neu
```

### `sentiment_robertuito_con_temas_todos.csv`

Tabla que combina los tres periódicos y añade la detección temática.

Cada fila corresponde a una frase asociada a un tema. Si una misma frase contiene palabras clave de varios temas, puede aparecer repetida una vez por cada tema detectado.

Columnas principales:

```text
sentence_id
documento
orden_frase
frase
tema
keyword_detectada
sentimiento
score_pos
score_neg
score_neu
```

Esta es la tabla central para revisar el cruce entre sentimiento y temas.

### `sentiment_robertuito_por_tema_y_documento.csv`

Tabla agregada que resume el número de frases por:

* documento;
* tema;
* sentimiento.

Sirve para comparar cómo se distribuyen los sentimientos asociados a cada tema en los tres periódicos.

Ejemplo de interpretación:

```text
documento | tema | sentimiento | n_frases
Fémina | patria | NEG | 25
Fémina | patria | POS | 18
Filipinas | educación | NEU | 40
```

### `temas_por_documento.csv`

Tabla que resume cuántas frases se han asociado a cada tema en cada periódico.

Sirve para identificar los temas más frecuentes por publicación.

### `sentiment_robertuito_resumen_tres_periodicos.csv`

Tabla de resumen general de los tres periódicos.

Agrupa el número de frases según:

* documento;
* sentimiento.

Sirve para comparar la distribución general de sentimientos entre **Fémina**, **Filipinas** y **El Heraldo de la Mujer**.

## `figures/`

Esta carpeta contiene las visualizaciones generadas a partir de los resultados.

```text
figures/
├── el_heraldo_mujer/
├── femina/
├── filipinas/
└── resumen_tres_periodicos_sentiment_robertuito.png
```

### Carpetas por documento

Cada carpeta contiene gráficos específicos de cada periódico:

```text
figures/femina/
figures/filipinas/
figures/el_heraldo_mujer/
```

Cada una puede contener:

```text
polaridad_por_temas_robertuito.png
temas_mas_frecuentes.png
```

### `polaridad_por_temas_robertuito.png`

Gráfico que muestra la distribución de sentimientos por tema dentro de un periódico.

Permite observar, por ejemplo, si las frases asociadas a `patria`, `mujer`, `educación` o `colonialismo` son clasificadas mayoritariamente como positivas, negativas o neutras.

### `temas_mas_frecuentes.png`

Gráfico que muestra los temas más frecuentes en cada periódico según las palabras clave definidas en `config/temas_keywords.yml`.

### `resumen_tres_periodicos_sentiment_robertuito.png`

Gráfico comparativo general de los tres periódicos.

Muestra la distribución global de sentimientos en las frases temáticas de cada publicación.

## Cómo ejecutar el análisis

Desde la carpeta `sentiment_analysis/`, ejecutar primero el análisis de sentimiento para cada periódico.

### 1. Análisis de sentimiento frase por frase

```powershell
python scripts\01_sentiment_robertuito.py --input "por_frases\femina_por_frases.txt" --document "femina" --output "results\femina\sentiment_robertuito_frases.csv"
```

```powershell
python scripts\01_sentiment_robertuito.py --input "por_frases\filipinas_por_frases.txt" --document "filipinas" --output "results\filipinas\sentiment_robertuito_frases.csv"
```

```powershell
python scripts\01_sentiment_robertuito.py --input "por_frases\heraldo_por_frases.txt" --document "el_heraldo_mujer" --output "results\el_heraldo_mujer\sentiment_robertuito_frases.csv"
```

Las rutas pueden variar según la localización real de los archivos `.txt` en el repositorio.

### 2. Visualización y cruce con temas

Una vez generados los tres CSV de sentimiento, ejecutar:

```powershell
python scripts\02_visualizar_sentiment_temas_robertuito.py --femina "results\femina\sentiment_robertuito_frases.csv" --filipinas "results\filipinas\sentiment_robertuito_frases.csv" --heraldo "results\el_heraldo_mujer\sentiment_robertuito_frases.csv" --topics "config\temas_keywords.yml" --outfig "figures" --outresults "results"
```

Este comando genera:

* tablas agregadas en `results/`;
* gráficos por documento en `figures/femina/`, `figures/filipinas/` y `figures/el_heraldo_mujer/`;
* un gráfico comparativo general en `figures/`.

## Dependencias

Dependencias principales:

```text
pandas
pyyaml
matplotlib
pysentimiento
```

Instalación recomendada:

```powershell
python -m pip install pandas pyyaml matplotlib pysentimiento
```

Si hubiera problemas relacionados con `torch` o `transformers`, instalar también:

```powershell
python -m pip install torch transformers
```

## Metodología

El análisis de sentimientos se realizó con `pysentimiento`, una biblioteca Python para minería de opinión y tareas de Social NLP. La biblioteca ofrece modelos preentrenados para análisis de sentimiento, detección de emociones, discurso de odio e ironía en varias lenguas, incluido el español. :contentReference[oaicite:0]{index=0}

Para el español, este experimento utiliza RoBERTuito a través de `pysentimiento`. RoBERTuito es un modelo transformer de la familia RoBERTa, preentrenado sobre más de 500 millones de tuits en español y diseñado para texto generado por usuarios en redes sociales. :contentReference[oaicite:1]{index=1}

Dado que el corpus de este proyecto está formado por prensa histórica de comienzos del siglo XX, el uso de RoBERTuito debe entenderse como un experimento exploratorio. El modelo no fue entrenado específicamente para prensa histórica, OCR ni español literario-periodístico de principios del siglo XX, por lo que los resultados deben contrastarse mediante revisión manual de ejemplos.El análisis se realiza en dos fases:

### Fase 1: clasificación de sentimiento

Cada periódico se analiza frase por frase con `pysentimiento`. El modelo asigna a cada frase una etiqueta:

* `POS`
* `NEG`
* `NEU`

y una puntuación para cada clase:

* `score_pos`
* `score_neg`
* `score_neu`

### Fase 2: cruce con temas

Después, las frases se cruzan con los temas definidos en `temas_keywords.yml`.

Este segundo paso permite estudiar la distribución de sentimientos no solo por documento, sino también por tema.

Por ejemplo:

* sentimiento asociado a `mujer`;
* sentimiento asociado a `patria`;
* sentimiento asociado a `educación`;
* sentimiento asociado a `colonialismo`;
* sentimiento asociado a `feminismo`.

## Limitaciones

Este análisis debe interpretarse como un experimento exploratorio.

El modelo utilizado por `pysentimiento` está entrenado sobre textos contemporáneos y no específicamente sobre prensa histórica de comienzos del siglo XX. Por ello, los resultados pueden verse afectados por:

* errores de OCR;
* segmentación imperfecta de frases;
* español histórico;
* usos retóricos, religiosos o literarios del lenguaje;
* presencia de anuncios;
* frases excesivamente largas;
* diferencias entre sentimiento textual y valoración política, moral o estética;
* ironía o ambivalencia discursiva.

Por estas razones, los resultados cuantitativos deben contrastarse con una revisión manual de ejemplos.

## Interpretación de los resultados

Los gráficos no deben leerse como una medición definitiva de la actitud ideológica de cada periódico. Indican cómo un modelo de sentimiento clasifica las frases del corpus.

La interpretación debe tener en cuenta:

* qué frases han sido asociadas a cada tema;
* qué palabra clave activó esa asociación;
* qué probabilidad asignó el modelo a cada etiqueta;
* si el OCR afecta a la frase;
* si la frase pertenece a un artículo, poema, anuncio, sumario o sección editorial.

La tabla más importante para revisar estos casos es:

```text
results/sentiment_robertuito_con_temas_todos.csv
```

## Reproducibilidad

Para reproducir el análisis es necesario conservar:

* los archivos `.txt` estructurados por frases;
* los scripts de `scripts/`;
* el archivo `config/temas_keywords.yml`;
* los CSV generados en `results/`;
* las versiones de las dependencias utilizadas.

Los resultados pueden variar si cambia la versión de `pysentimiento`, `transformers`, `torch` o el modelo descargado.

## Bibliografía

Pérez, Juan Manuel, Mariela Rajngewerc, Juan Carlos Giudici, Damián A. Furman, Franco Luque, Laura Alonso Alemany y María Vanina Martínez. “pysentimiento: A Python Toolkit for Opinion Mining and Social NLP Tasks”. arXiv, 2021. https://doi.org/10.48550/arXiv.2106.09462 

Pérez, Juan Manuel, Damián A. Furman, Laura Alonso Alemany y Franco Luque. “RoBERTuito: A Pre-Trained Language Model for Social Media Text in Spanish”. *Proceedings of the Language Resources and Evaluation Conference*, 2022. https://aclanthology.org/2022.lrec-1.785/

