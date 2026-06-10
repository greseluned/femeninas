# femeninas
# Humanidades Digitales clásicas e Inteligencia Artificial en prensa femenina hispánica

Este repositorio contiene los datos, scripts, prompts, configuraciones y resultados de un estudio comparativo sobre el análisis digital de tres revistas femeninas hispánicas de principios del siglo XX:

* **Fémina** — República Dominicana, 1922-1923.
* **Filipinas** — Filipinas, 1909-1910.
* **El Heraldo de la Mujer** — Puerto Rico, 1919-1920.

El proyecto compara tres aproximaciones metodológicas:

1. **Humanidades Digitales clásicas**: frecuencia de palabras, modelado de temas, extracción de entidades nombradas y análisis de sentimientos.
2. **IA abierta/local con Gemma en AnythingLLM**: análisis del corpus mediante un sistema RAG reproducible, instalado en local y basado en un modelo abierto.
3. **IA comercial**: análisis del corpus mediante herramientas comerciales.

El objetivo del repositorio es garantizar la trazabilidad y la reproducibilidad de los análisis, conservar los datos derivados y documentar los prompts utilizados para preparar un artículo académico comparativo.

## 1. Preguntas de investigación

El estudio parte de las siguientes preguntas:

1. ¿Hay redes de mujeres visibles en la prensa de los tres países estudiados?
2. ¿Comparten las revistas temas, preocupaciones, vocabularios o referentes?
3. ¿Qué discursos aparecen en torno a la mujer, la patria, la raza, la religión, el feminismo, el sufragio y el colonialismo?
4. ¿Qué diferencias hay entre los resultados obtenidos mediante Humanidades Digitales clásicas y mediante sistemas de IA?
5. ¿Qué herramientas ofrecen mayor trazabilidad, exhaustividad y reproducibilidad?
6. ¿Qué tipos de errores produce cada metodología?

## 2. Corpus

El corpus está formado por tres revistas femeninas publicadas en contextos marcados por el colonialismo o el dominio estadounidense en el Caribe y Asia hispánica.

| Revista                | País / territorio    | Fechas    | Extensión aproximada   | Fuente                                                                |
| ---------------------- | -------------------- | --------- | ---------------------- | --------------------------------------------------------------------- |
| Fémina                 | República Dominicana | 1922-1923 | 200 páginas            | Archivo General de la Nación / Biblioteca del Caribe                  |
| Filipinas              | Filipinas            | 1909-1910 | 92 páginas en español  | National Library of the Philippines                                   |
| El Heraldo de la Mujer | Puerto Rico          | 1919-1920 | 192 páginas en español | Biblioteca Digital Memoria de Madrid / Archivo Digital de Puerto Rico |

El corpus puede conservarse en tres formatos:

* imágenes originales en **JPG**;
* resultados de OCR en **ALTO-XML**;
* texto plano en **TXT**.

La carpeta `corpus/` contiene los materiales de partida y sus metadatos.

## 3. Estructura del repositorio

El repositorio está organizado por metodología, de modo que los scripts, prompts y resultados de cada aproximación estén claramente separados.

```text
revistas-femeninas-hd-ia/
│
├── corpus/
├── 01_hd_clasicas/
├── 02_ia_abierta_gemma/
├── 03_ia_comercial/
├── 04_comparacion_metodologica/
├── docs/
├── article/
└── tests/
```

## 4. `corpus/`

Esta carpeta contiene el corpus de trabajo y los metadatos.

```text
corpus/
├── README.md
├── metadata/
│   ├── corpus_metadata.csv
│
├── femina_rd/
│   ├── jpg/
│   ├── alto_xml/
│   └── txt/
│
├── filipinas_ph/
│   ├── jpg/
│   ├── alto_xml/
│   └── txt/
│
└── heraldo_mujer_pr/
    ├── jpg/
    ├── alto_xml/
    └── txt/
```

## 5. `01_hd_clasicas/`

Esta carpeta reúne los análisis realizados con métodos tradicionales de Humanidades Digitales.

```text
01_hd_clasicas/
├── README.md
├── scripts/
└── results/
```

Incluye los siguientes tipos de análisis:

* segmentación del OCR;
* modelado de temas;
* extracción de entidades nombradas;
* normalización de entidades;
* análisis de sentimientos;
* visualización de resultados;
* exportación de grafos para Gephi.

## 6. `02_ia_abierta_gemma/`

Esta carpeta contiene los experimentos realizados con IA abierta/local. Hemos experimentado con **Gemma en AnythingLLM**.

```text
02_ia_abierta_gemma/
├── README.md
├── config/
├── scripts/
├── prompts/
├── inputs/
└── results/
```

El objetivo de esta sección es documentar una aproximación con IA que sea más reproducible que las herramientas comerciales, en la medida en que se puede registrar:

* modelo utilizado;
* versión del modelo;
* configuración del espacio de trabajo;
* documentos incluidos;
* documentos excluidos;
* parámetros del sistema RAG;
* prompts;
* respuestas;
* evidencias textuales;

Los prompts se guardan en:

```text
02_ia_abierta_gemma/prompts/
```

Los resultados se guardan en:

```text
02_ia_abierta_gemma/results/
├── respuestas_raw/
├── respuestas_tablas/
└── figures/
```

## 7. `03_ia_comercial/`

Esta carpeta contiene los experimentos realizados con sistemas comerciales de IA.

```text
03_ia_comercial/
├── README.md
├── notebooklm/
└── otros_modelos_comerciales/
```

La subcarpeta `notebooklm/` permite guardar:

* prompts;
* documentos subidos;
* configuración del notebook;
* respuestas originales;
* respuestas tabuladas;
* citas y evidencias;

```text
03_ia_comercial/notebooklm/
├── README.md
├── prompts/
├── inputs/
└── results/
```

## 8. `04_comparacion_metodologica/`

Esta carpeta reúne los scripts, notebooks y resultados de la comparación entre las tres aproximaciones:

1. HD clásicas.
2. IA abierta/local con Gemma.
3. IA comercial.

```text
04_comparacion_metodologica/
├── README.md
├── scripts/
└── results/
```

Los aspectos comparados incluyen:

* temas identificados;
* entidades nombradas;
* redes de personas;
* presencia o ausencia de mujeres reales;
* referencias a escritoras;
* referencias al feminismo internacional;
* discursos sobre patria, raza, religión, colonialismo y sufragio;
* precisión;
* exhaustividad;
* reproducibilidad;
* trazabilidad;
* dependencia del prompt;
* capacidad de aportar citas textuales verificables.

Los resultados comparativos se guardan en:

```text
04_comparacion_metodologica/results/
├── tablas_comparativas/
├── matrices_evaluacion/
├── figuras_articulo/
└── informe_comparativo.md
```

## 9. Prompts

Los prompts se conservan dentro de la carpeta correspondiente a cada sistema de IA:

```text
02_ia_abierta_gemma/prompts/
03_ia_comercial/notebooklm/prompts/
03_ia_comercial/otros_modelos_comerciales/prompts/
```

Cada prompt debe guardarse como archivo `.md` independiente.

Además, cada sección de IA debe incluir un archivo `prompt_log.csv` con los siguientes campos:

```text
id_prompt,
fecha,
herramienta,
modelo,
version_modelo,
corpus_utilizado,
documentos_incluidos,
documentos_excluidos,
prompt_file,
output_file,
observaciones
```

## 10. Ejemplo de prompt

```text
Responde únicamente basándote en los documentos del corpus.
Si un tema no aparece explícitamente en los textos, no lo incluyas.
No uses conocimiento externo.
Si no encuentras suficiente evidencia textual para un tópico, indícalo explícitamente.

Analiza cada una de las tres publicaciones del corpus —Fémina, Filipinas y El Heraldo de la Mujer— por separado.

Para cada una, identifica los 8 temas principales siguiendo este procedimiento:

1. Lista los 8 temas en orden de mayor a menor presencia en la revista.
2. Para cada tema, proporciona exactamente 8 palabras clave representativas extraídas literalmente del texto.
3. Indica para cada tema un porcentaje estimado de presencia respecto al total del contenido de esa publicación.
4. Cita al menos 2 fragmentos textuales concretos que justifiquen cada tema, con indicación de la parte del documento en que aparecen.
5. Devuelve los resultados en formato de tabla con estas columnas:

Revista | Nº tópico | Nombre del tópico | Palabras clave | % presencia | Fragmentos de ejemplo
```

## 11. Criterios de evaluación

Los resultados de cada metodología se evaluarán con criterios comunes:

| Criterio          | Descripción                                                                     |
| ----------------- | ------------------------------------------------------------------------------- |
| Precisión         | Si los resultados son correctos respecto al corpus.                             |
| Exhaustividad     | Si el método recupera todos o la mayoría de los casos relevantes.               |
| Trazabilidad      | Si permite comprobar de dónde sale cada resultado.                              |
| Reproducibilidad  | Si otro investigador puede repetir el procedimiento.                            |
| Interpretabilidad | Si los resultados pueden analizarse de forma crítica.                           |
| Sesgos            | Si el método privilegia ciertos documentos, páginas, entidades o temas.         |
| Errores           | Si produce falsos positivos, omisiones, alucinaciones o asociaciones engañosas. |

## 12. Reproducibilidad

Para reproducir los análisis de Humanidades Digitales clásicas:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Después, ejecutar los notebooks de la carpeta:

```text
01_hd_clasicas/notebooks/
```

Para reproducir los experimentos con Gemma en AnythingLLM, consultar:

```text
02_ia_abierta_gemma/config/
02_ia_abierta_gemma/prompts/
02_ia_abierta_gemma/inputs/
```

Para revisar los experimentos con IA comercial, consultar:

```text
03_ia_comercial/
```

En el caso de herramientas comerciales, la reproducibilidad puede ser parcial, por lo que se documentarán las condiciones de uso, los documentos subidos, la fecha del experimento y las respuestas obtenidas.

## 13. Licencia

https://creativecommons.org/licenses/by-nc/4.0/ 

## 14. Cómo citar este repositorio

Referencia provisional:

```text
Ortuño Casanova, Rocío, Vera-Rojas, María Teresa y Pirvu, Nuria.
Humanidades Digitales clásicas e Inteligencia Artificial en prensa femenina hispánica.
Repositorio de datos, scripts, prompts y resultados para el estudio comparativo de Fémina, Filipinas y El Heraldo de la Mujer.
```

## 15. Autoría

* Rocío Ortuño Casanova
* Nuria Pirvu
* María Teresa Vera-Rojas
