# Análisis léxico de polaridad

Esta carpeta contiene los archivos necesarios para realizar un **análisis léxico de polaridad** sobre los tres periódicos del corpus:

* **Fémina**
* **Filipinas**
* **El Heraldo de la Mujer**

El análisis se realiza por separado para cada documento. Su objetivo es identificar qué temas aparecen en cada periódico y qué tipo de vocabulario valorativo —positivo, negativo o neutro— se asocia a esos temas.

A diferencia de un análisis de sentimientos basado en modelos de lenguaje, este procedimiento no utiliza BETO, transformers ni modelos generativos. Se basa en listas explícitas de palabras clave y lexicones manuales de polaridad. Por ello, se considera una aproximación de **Humanidades Digitales clásicas**, transparente, reproducible e interpretable.

## Objetivo

El análisis busca responder preguntas como:

* ¿Qué temas aparecen con más frecuencia en cada periódico?
* ¿Qué temas se asocian con más vocabulario positivo o negativo?
* ¿Existen diferencias entre las revistas en la forma de tratar temas como mujer, patria, educación, religión, feminismo, raza o colonialismo?
* ¿Qué limitaciones tiene un análisis léxico aplicado a prensa histórica con OCR?

El análisis no pretende determinar el “sentimiento real” de los textos, sino medir la presencia de vocabulario valorativo en frases asociadas a temas concretos.

## Estructura de la carpeta

```text
sentiment/
├── config/
├── figures/
├── intermediate/
├── results/
└── scripts/
```

## `config/`

Contiene los archivos de configuración del análisis.

### `temas_keywords.yml`

Lista los temas de investigación y las palabras clave utilizadas para detectarlos en las frases del corpus.

Ejemplo de temas:

* mujer
* feminismo
* patria
* raza
* educación
* hogar
* religión
* colonialismo

Este archivo sirve para identificar qué frases mencionan cada tema. Una misma frase puede asociarse a más de un tema si contiene palabras clave de varias categorías.

### `lexicon_positivo.yml`

Contiene el lexicón manual de términos con polaridad positiva.

Ejemplos de términos positivos:

* amor
* virtud
* libertad
* esperanza
* progreso
* justicia
* cultura
* belleza
* dignidad
* triunfo

Este archivo se utiliza para contar cuántas palabras positivas aparecen en cada frase.

### `lexicon_negativo.yml`

Contiene el lexicón manual de términos con polaridad negativa.

Ejemplos de términos negativos:

* dolor
* tristeza
* opresión
* esclavitud
* guerra
* sufrimiento
* miseria
* injusticia
* imperialismo
* muerte

Este archivo se utiliza para contar cuántas palabras negativas aparecen en cada frase.

## `scripts/`

Contiene los scripts que ejecutan el análisis. Están numerados según el orden recomendado de ejecución.

### `01_crear_tabla_frases.py`

Convierte un archivo `.txt` estructurado por frases en una tabla `.csv`.

Entrada esperada:

```text
por_frases/femina_por_frases.txt
por_frases/filipinas_por_frases.txt
por_frases/heraldo_por_frases.txt
```

Salida esperada:

```text
intermediate/femina/frases_corpus.csv
intermediate/filipinas/frases_corpus.csv
intermediate/heraldo/frases_corpus.csv
```

Cada fila de la tabla corresponde a una frase e incluye:

* identificador de frase;
* nombre del documento;
* orden de la frase;
* frase original.

### `02_limpiar_frases.py`

Limpia y normaliza las frases para facilitar el análisis léxico.

Este script:

* pasa el texto a minúsculas;
* elimina puntuación;
* normaliza tildes;
* calcula el número de palabras;
* elimina frases demasiado cortas.

Salida esperada:

```text
intermediate/femina/frases_limpias.csv
intermediate/filipinas/frases_limpias.csv
intermediate/heraldo/frases_limpias.csv
```

La tabla conserva tanto la frase original como la frase normalizada.

### `03_detectar_temas.py`

Detecta los temas presentes en cada frase a partir del archivo:

```text
config/temas_keywords.yml
```

Salida esperada:

```text
intermediate/femina/frases_con_temas.csv
intermediate/filipinas/frases_con_temas.csv
intermediate/heraldo/frases_con_temas.csv
```

Cada fila indica una frase, el tema detectado y la palabra clave que ha activado la detección.

Si una frase contiene palabras clave de varios temas, aparece repetida una vez por cada tema.

### `04_calcular_polaridad_lexica.py`

Calcula la polaridad léxica de cada frase a partir de los archivos:

```text
config/lexicon_positivo.yml
config/lexicon_negativo.yml
```

Para cada frase calcula:

* número de palabras positivas;
* número de palabras negativas;
* polaridad bruta;
* polaridad normalizada;
* etiqueta de polaridad: positiva, negativa o neutra;
* palabras positivas detectadas;
* palabras negativas detectadas.

La polaridad bruta se calcula así:

```text
polaridad_bruta = número de palabras positivas - número de palabras negativas
```

La polaridad normalizada se calcula así:

```text
polaridad_normalizada = polaridad_bruta / número total de palabras de la frase
```

Salida esperada:

```text
intermediate/femina/frases_con_polaridad.csv
intermediate/filipinas/frases_con_polaridad.csv
intermediate/heraldo/frases_con_polaridad.csv
```

### `05_agregar_resultados.py`

Cruza los temas detectados con la polaridad léxica y genera tablas agregadas.

Salidas esperadas:

```text
results/femina/
results/filipinas/
results/heraldo/
```

Dentro de cada carpeta se generan varios archivos:

```text
frases_con_temas_y_polaridad.csv
menciones_temas_por_documento.csv
polaridad_por_documento.csv
polaridad_por_tema_y_documento.csv
ejemplos_revision_manual.csv
```

### `06_generar_graficos.py`

Genera gráficos a partir de las tablas agregadas.

Salidas esperadas:

```text
figures/femina/
figures/filipinas/
figures/heraldo/
```

Cada carpeta contiene gráficos como:

```text
frecuencia_temas.png
polaridad_media_por_tema.png
distribucion_polaridad_por_tema.png
```

## `intermediate/`

Contiene archivos intermedios generados durante el proceso.

Esta carpeta permite comprobar todos los pasos del análisis y facilita la reproducibilidad.

Estructura esperada:

```text
intermediate/
├── femina/
├── filipinas/
└── heraldo/
```

Cada subcarpeta puede contener:

```text
frases_corpus.csv
frases_limpias.csv
frases_con_temas.csv
frases_con_polaridad.csv
```

Estos archivos no son resultados finales, pero son fundamentales para revisar cómo se ha pasado del corpus original a las tablas agregadas.

## `results/`

Contiene los resultados tabulares finales del análisis.

Estructura esperada:

```text
results/
├── femina/
├── filipinas/
└── heraldo/
```

Cada subcarpeta contiene:

### `frases_con_temas_y_polaridad.csv`

Tabla central del análisis. Cruza cada frase temática con su polaridad léxica.

Columnas principales:

* `sentence_id`
* `documento`
* `tema`
* `keyword_detectada`
* `frase_original`
* `n_positivo`
* `n_negativo`
* `polaridad_bruta`
* `polaridad_normalizada`
* `etiqueta_polaridad`
* `palabras_positivas_detectadas`
* `palabras_negativas_detectadas`

### `menciones_temas_por_documento.csv`

Resume cuántas frases se asocian a cada tema en cada documento.

Sirve para comparar la presencia relativa de los temas.

### `polaridad_por_documento.csv`

Resume la polaridad general de cada periódico.

Incluye:

* número total de frases;
* número de frases positivas;
* número de frases negativas;
* número de frases neutras;
* porcentajes;
* media de polaridad.

### `polaridad_por_tema_y_documento.csv`

Resume la polaridad de cada tema dentro de cada periódico.

Es la tabla más importante para la comparación posterior entre documentos.

Permite observar, por ejemplo, si el tema `patria` aparece con más vocabulario negativo en un periódico y con más vocabulario positivo en otro.

### `ejemplos_revision_manual.csv`

Contiene ejemplos de frases seleccionadas para revisión cualitativa.

Este archivo es importante porque permite comprobar manualmente si la clasificación léxica funciona bien o si hay problemas de contexto, ironía, OCR o ambigüedad.

## `figures/`

Contiene las visualizaciones generadas a partir de los resultados.

Estructura esperada:

```text
figures/
├── femina/
├── filipinas/
└── heraldo/
```

Cada subcarpeta puede contener:

### `frecuencia_temas.png`

Gráfico de frecuencia de temas en el documento.

### `polaridad_media_por_tema.png`

Gráfico de polaridad media normalizada por tema.

### `distribucion_polaridad_por_tema.png`

Gráfico de distribución de frases positivas, negativas y neutras por tema.

## Dependencias

Dependencias mínimas:

```text
pandas
pyyaml
matplotlib
```

Instalación:

```powershell
python -m pip install pandas pyyaml matplotlib
```

## Interpretación de los resultados

Los resultados deben interpretarse como una medida de **polaridad léxica**, no como análisis semántico profundo.

Una frase se considera positiva si contiene más términos del lexicón positivo que del negativo; negativa si contiene más términos negativos que positivos; y neutra si no contiene términos valorativos o si los conteos se equilibran.

Este método tiene la ventaja de ser transparente y reproducible, pero presenta limitaciones:

* no capta ironía;
* no resuelve ambigüedades contextuales;
* depende de la calidad del OCR;
* puede verse afectado por frases muy largas;
* puede interpretar como positivas o negativas palabras que en determinados contextos históricos tienen otro matiz;
* no distingue entre voz editorial, cita, ficción, poema o anuncio.

Por ello, los resultados cuantitativos deben contrastarse con la revisión manual de ejemplos.

## Decisiones metodológicas

El lexicón positivo y negativo ha sido elaborado manualmente a partir de una exploración preliminar del corpus. No debe considerarse un recurso externo validado, sino una herramienta interpretativa y revisable. Todas las listas se conservan en `config/` para que cualquier persona pueda inspeccionarlas, modificarlas o reutilizarlas.