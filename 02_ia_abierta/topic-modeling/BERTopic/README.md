# Topic modeling con BERTopic sobre revistas feministas hispanas

Este repositorio contiene un flujo de trabajo para aplicar **modelado de tópicos con BERTopic** a un corpus de revistas feministas hispanas. El objetivo es comparar los temas predominantes en tres publicaciones periódicas históricas:

* *Fémina*
* *Filipinas*
* *El Heraldo de la Mujer*

El procedimiento parte de documentos de texto completos, los divide en fragmentos de 200-300 palabras, aplica BERTopic y genera tablas y visualizaciones con los tópicos más relevantes por revista.

## Estructura del proyecto

La organización de carpetas es la siguiente:

```text
02_ia_abierta/
└── topic-modeling/
    └── BERTopic/
        ├── corpus/
        │   ├── textos_revistas/
        │   │   ├── femina_merged.txt
        │   │   ├── filipinas_merged.txt
        │   │   └── heraldo_merged.txt
        │   └── corpus_revistas_chunks.csv
        │
        ├── results/
        │   ├── graficas/
        │   │   ├── top_10_topicos_el_heraldo_de_la_mujer.png
        │   │   ├── top_10_topicos_femina.png
        │   │   └── top_10_topicos_filipinas.png
        │   │
        │   ├── documentos_con_topicos.csv
        │   ├── topicos_bertopic.csv
        │   └── topicos_por_revista.csv
        │
        └── scripts/
            ├── dividir_textos_chunks.py
            ├── graficas_topicos_revista.py
            └── script_bertopic_ajustado.py
```

## Descripción del flujo de trabajo

El proceso consta de tres pasos principales:

1. **Preparación del corpus**

   * Se parte de tres archivos `.txt`, uno por revista.
   * Cada archivo contiene el texto completo de una revista o conjunto de números.
   * Los textos se dividen en fragmentos de entre 200 y 300 palabras.

2. **Modelado de tópicos**

   * Se aplica BERTopic sobre los fragmentos generados.
   * BERTopic utiliza modelos de lenguaje basados en embeddings para agrupar textos semánticamente próximos.
   * Los tópicos se representan mediante palabras clave.

3. **Visualización de resultados**

   * Se calcula la distribución de tópicos por revista.
   * Se generan tres gráficas, una por revista, con los diez tópicos más relevantes y sus palabras asociadas.

## 1. Preparación del corpus

Los textos originales deben colocarse en:

```text
corpus/textos_revistas/
```

Los nombres de archivo esperados son, por ejemplo:

```text
femina_merged.txt
filipinas_merged.txt
heraldo_merged.txt
```

El nombre del archivo se utiliza para identificar la revista correspondiente.

Para dividir los textos en fragmentos, ejecutar:

```bash
python scripts/dividir_textos_chunks.py
```

Este script genera el archivo:

```text
corpus/corpus_revistas_chunks.csv
```

El CSV resultante contiene una fila por fragmento y conserva información básica como:

* `chunk_id`
* `revista`
* `archivo_origen`
* `chunk_num`
* `n_palabras`
* `texto`

## 2. Modelado de tópicos con BERTopic

Una vez generado el archivo `corpus_revistas_chunks.csv`, se ejecuta el script de BERTopic:

```bash
python scripts/script_bertopic_ajustado.py
```

Este script aplica BERTopic al conjunto de fragmentos y genera varios archivos de resultados en la carpeta:

```text
results/
```

Los principales archivos de salida son:

```text
results/documentos_con_topicos.csv
results/topicos_bertopic.csv
results/topicos_por_revista.csv
```

### `documentos_con_topicos.csv`

Contiene cada fragmento del corpus junto con el tópico asignado por BERTopic.

Columnas principales:

* `chunk_id`
* `revista`
* `archivo_origen`
* `chunk_num`
* `n_palabras`
* `texto`
* `topic`

### `topicos_bertopic.csv`

Contiene la información general de cada tópico identificado por BERTopic.

Incluye, según la configuración de BERTopic:

* identificador del tópico;
* número de documentos asociados;
* nombre automático del tópico;
* palabras representativas;
* representación del tópico.

### `topicos_por_revista.csv`

Resume la presencia de cada tópico en cada revista.

Columnas habituales:

* `revista`
* `topic`
* `n_chunks`
* `porcentaje_en_revista`

Este archivo permite comparar qué tópicos son más relevantes en cada publicación.

## 3. Generación de gráficas

Para generar visualizaciones de los diez tópicos más relevantes por revista, ejecutar:

```bash
python scripts/graficas_topicos_revista.py
```

Este script utiliza los archivos:

```text
results/topicos_por_revista.csv
results/topicos_bertopic.csv
```

y genera tres imágenes en:

```text
results/graficas/
```

Las gráficas resultantes son:

```text
results/graficas/top_10_topicos_femina.png
results/graficas/top_10_topicos_filipinas.png
results/graficas/top_10_topicos_el_heraldo_de_la_mujer.png
```

Cada gráfica muestra:

* los diez tópicos más relevantes de una revista;
* el peso relativo de cada tópico;
* las palabras asociadas a cada tópico.

## Requisitos

El flujo de trabajo se ha probado con Python y requiere las siguientes bibliotecas:

```bash
pip install pandas matplotlib bertopic sentence-transformers umap-learn hdbscan scikit-learn
```

También puede instalarse en un entorno de Conda:

```bash
conda create -n bertopic_env python=3.10
conda activate bertopic_env
pip install pandas matplotlib bertopic sentence-transformers umap-learn hdbscan scikit-learn
```

## Ejecución completa

Desde la carpeta `BERTopic`, el flujo completo se puede ejecutar así:

```bash
python scripts/dividir_textos_chunks.py
python scripts/script_bertopic_ajustado.py
python scripts/graficas_topicos_revista.py
```

## Notas metodológicas

Este flujo de trabajo utiliza BERTopic como alternativa al modelado de tópicos clásico con LDA. A diferencia de LDA, que se basa principalmente en patrones de coocurrencia léxica, BERTopic utiliza modelos de lenguaje para representar los fragmentos como vectores semánticos y después agruparlos mediante técnicas de clustering.

En este proyecto, los documentos originales se dividen en fragmentos de 200-300 palabras para evitar que los textos completos sean demasiado largos y para mejorar la calidad de la agrupación semántica.

El uso de BERTopic no elimina la necesidad de interpretación humana. Los tópicos generados deben revisarse críticamente, especialmente en corpus históricos con OCR, ruido textual, grafías antiguas, presencia de varias lenguas o heterogeneidad de géneros periodísticos.

## Limitaciones

Algunas limitaciones del procedimiento son:

* Los resultados dependen del tamaño de los fragmentos.
* Los tópicos pueden variar si se cambian los parámetros de BERTopic.
* El tópico `-1`, si aparece, representa fragmentos que el modelo no ha agrupado claramente.
* Las palabras asociadas a los tópicos pueden incluir ruido procedente del OCR.
* La interpretación final de los tópicos requiere validación humanística.

## Objetivo del experimento

Este experimento forma parte de una comparación entre métodos de investigación cuantitativa en Humanidades Digitales y métodos asistidos por IA. En este caso, BERTopic se utiliza para mostrar cómo los modelos de lenguaje pueden ayudar a detectar agrupaciones temáticas en un corpus histórico, sin sustituir la lectura crítica ni la interpretación experta.
