# NER con Gemini 3 Flash Preview

Este directorio contiene los resultados del reconocimiento de entidades nombradas (NER) aplicado a un corpus de revistas históricas femeninas en español: *Fémina*, *Filipinas* y *El Heraldo de la Mujer*. El objetivo es extraer y cuantificar las menciones de personas a lo largo de las publicaciones.

El modelo utilizado es **Gemini 2.5 Flash Preview**, accedido a través de **Google AI Studio** con ajustes predeterminados.

---

## Estructura de carpetas

```text
03_ia_comercial/
└── NER/
    └── gemini-3-flash-preview/
        └── results/
            ├── personas-fémina.csv
            ├── personas-filipinas.csv
            ├── personas-general.csv
            └── personas-heraldo.csv
```
---

## Corpus de entrada

Los textos analizados son los archivos `.txt` resultantes de las transcripciones de **Transkribus**, unidos y reconstruidos en un único fichero por revista. Estos archivos consolidados son los mismos que se usan en el resto del pipeline de análisis del proyecto.

---

## Flujo de trabajo

### 1. Iteraciones por revista

Se realizaron **5 iteraciones independientes** para cada revista (*Fémina*, *Filipinas*, *El Heraldo de la Mujer*), más **5 iteraciones adicionales** sobre el corpus conjunto de las tres publicaciones (carpeta `general`).

Cada iteración se ejecutó en un **chat independiente** en Google AI Studio, de modo que el modelo no arrastrase contexto entre ejecuciones.

### 2. Prompt

Se utilizó el mismo prompt en todas las iteraciones y para todas las revistas. El texto del prompt se encuentra en `03_ia_comercial/prompts/prompt-NER.txt`

El prompt solicitaba al modelo que identificase todas las menciones de personas en el texto y devolviera los resultados en formato CSV con las columnas: `revista,persona,frecuencia`

### 3. Control de calidad de la respuesta

Cuando la respuesta del modelo estaba incompleta o no respetaba el formato CSV solicitado, se **regeneró la respuesta** dentro del mismo chat hasta obtener un resultado válido.

### 4. Selección de la lista más larga

El criterio para seleccionar el resultado representativo de cada revista fue quedarse con la **iteración que producía la lista más larga de nombres**, asumiendo que recoge el mayor número de entidades identificadas en el texto.

### 5. Unificación de nombres

La lista seleccionada se pasó de nuevo por el mismo modelo (Gemini 2.5 Flash Preview, Google AI Studio) para **unificar variantes y duplicados** de un mismo nombre (por ejemplo, formas abreviadas, apellidos solos, grafías alternativas), obteniendo así los archivos CSV finales.

---