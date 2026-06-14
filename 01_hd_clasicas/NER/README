# Extracción, normalización y visualización de entidades nombradas en revistas históricas

Este repositorio contiene datos, scripts y grafos derivados de un flujo de trabajo para la extracción, limpieza, reconciliación y visualización de entidades nombradas en tres revistas/periódicos históricos. El objetivo principal es estudiar la presencia de entidades de persona en cada publicación y observar coincidencias entre revistas: autoras, autores, personajes literarios, figuras históricas u otras personas mencionadas en más de una cabecera que permitan estudiar la circulación de referentes y de autoras.

## Contenido del repositorio

El repositorio incluye:

```text
.
├── scripts/
│   ├── limpiar_entidades.py
│   └── crear_gephi_personas_revistas.py
│
├── data/
│   ├── entidades-femina-wikidata.tsv
│   ├── entities-heraldo-wikidata.tsv
│   └── entidades-filipinas-wikidata.tsv
│
├── gephi/
│   ├── gephi_edges_personas_revistas_es.csv
│   ├── gephi_nodes_personas_revistas_es.csv
│   ├── personas_revistas_combinado_es.tsv
│   └── grafos/
│       ├── entidades_revistas_completo.gephi
│       ├── grafo_revistas_completo.png
│       ├── grafo_revistas_completo.svg
│       ├── grafo_revistas_filtrado.png
│       └── grafo_revistas_filtrado.svg
│
└── README.md
```

## Objetivos

Este trabajo tiene tres objetivos principales:

1. Extraer entidades nombradas de textos históricos mediante reconocimiento automático de entidades.
2. Limpiar y normalizar variantes de nombres procedentes de OCR, diferencias ortográficas, abreviaturas y reconciliaciones parciales.
3. Construir un grafo bipartito revista–persona para visualizar qué entidades aparecen en cada revista y cuáles conectan varias publicaciones.

## Flujo de trabajo

El proceso seguido consta de cuatro fases:

1. Extracción automática de entidades nombradas con NameTag.
2. Limpieza, normalización y reconciliación de entidades con OpenRefine.
3. Enriquecimiento parcial mediante Wikidata.
4. Creación de tablas de nodos y aristas para Gephi y visualización de redes.

## 1. Extracción de entidades nombradas con NameTag

La extracción inicial de entidades se realizó con NameTag, servicio alojado en LINDAT/CLARIAH-CZ:

https://lindat.mff.cuni.cz/services/nametag/

En concreto, se utilizó el modelo para español disponible a través de la interfaz de NameTag:

https://lindat.mff.cuni.cz/services/nametag/?data=https%3A%2F%2Fswitchboard.clarin.eu%2Fapi%2Fstorage%2F8f12c841-c1da-40a1-891c-03320b1daf25%3Fmediatype%3Dtext%252Fplain&model=spa

NameTag es una herramienta de reconocimiento de entidades nombradas, o Named Entity Recognition, que identifica nombres propios en un texto y los clasifica en categorías predefinidas. En este proyecto, la extracción se usó como punto de partida para localizar entidades de tipo persona, lugar, organización y otras categorías detectadas automáticamente.

Las entidades resultantes fueron revisadas posteriormente, ya que los textos históricos y los resultados procedentes de OCR presentan problemas frecuentes:

* variantes ortográficas;
* errores de reconocimiento óptico de caracteres;
* abreviaturas;
* nombres incompletos;
* mezcla de idiomas;
* entidades mal clasificadas;
* formas de tratamiento incorporadas al nombre;
* repeticiones de una misma entidad bajo formas distintas.

## 2. Limpieza y reconciliación con OpenRefine

Tras la extracción automática, las tablas de entidades se trabajaron en OpenRefine:

https://openrefine.org/

OpenRefine se utilizó para:

* limpiar datos tabulares;
* crear columnas normalizadas;
* agrupar variantes mediante clustering;
* revisar manualmente entidades dudosas;
* eliminar filas no pertinentes;
* reconciliar entidades con Wikidata cuando fue posible;
* añadir identificadores externos de Wikidata, especialmente QID.

El trabajo en OpenRefine permitió crear o revisar una columna normalizada, por ejemplo:

```text
entity_normalized_clean
```

Esta columna conserva una forma limpia de la entidad y sirve como base para el análisis posterior.

En los casos en los que una entidad pudo vincularse con Wikidata, se añadió una columna con el identificador correspondiente:

```text
wikidata_qid
```

Por ejemplo:

```text
Q535
Q859
Q1398
```

El QID permite reconocer como una misma entidad variantes que pueden aparecer con nombres distintos en varias revistas.

## 3. Reconciliación con Wikidata

La reconciliación con Wikidata se realizó desde OpenRefine mediante el servicio de reconciliación:

https://wikidata-reconciliation.wmcloud.org/

Cuando fue posible, las entidades de persona fueron alineadas con ítems de Wikidata. Para personas, se priorizó el tipo:

```text
human / ser humano / Q5
```

La reconciliación con Wikidata se usó de manera semiautomática. No todas las entidades tienen perfil en Wikidata, especialmente en el caso de autoras, colaboradoras o personajes de prensa histórica local. Por ello, el flujo de trabajo conserva siempre el valor de la columna local `entity_normalized_clean` cuando no hay QID o cuando no se puede recuperar una etiqueta adecuada.

La lógica utilizada en el script final es:

```text
si hay QID y hay etiqueta en español → usar etiqueta en español
si hay QID pero no hay etiqueta en español → usar entity_normalized_clean
si no hay QID → usar entity_normalized_clean
```

Además, se contemplan correcciones manuales para entidades problemáticas, por ejemplo cuando Wikidata devuelve etiquetas en otro idioma o cuando una reconciliación necesita revisión.

## 4. Limpieza automática con Python

El script `limpiar_entidades.py` automatiza parte de la limpieza de las tablas exportadas desde OpenRefine.

Entre otras tareas, permite:

* eliminar comillas;
* normalizar espacios;
* convertir entidades escritas completamente en mayúsculas a una forma capitalizada;
* conservar en minúscula partículas y stop-words dentro de nombres propios;
* eliminar formas de tratamiento y abreviaturas como `Sr.`, `Sra.`, `Señorita`, `Mrs.`, `Mme`, `Dr.`, `Dra.`, etc.;
* crear una nueva columna limpia sin sobrescribir la columna original.

Ejemplo de transformación:

```text
"PETRONILA ANGELICA GOMEZ"        → Petronila Angelica Gomez
"Sra. CONSUELO MONTALVO DE FRIAS" → Consuelo Montalvo de Frias
"MARIA L . ANGELIS DE CANINO"     → Maria L. Angelis de Canino
```

El script está pensado para trabajar con archivos TSV o CSV exportados desde OpenRefine. Se recomienda usar TSV para evitar problemas con comas internas en los datos.

## 5. Creación de tablas para Gephi

El script `crear_gephi_personas_revistas.py` toma como entrada las tablas finales de entidades de cada revista:

```text
C:\...\entidades-femina-wikidata.tsv
C:\...\entities-heraldo-wikidata.tsv
C:\...\entidades-filipinas-wikidata.tsv
```

El script extrae la columna:

```text
entity_normalized_clean
```

y la combina con el nombre de la revista, inferido a partir del nombre del archivo.

Por ejemplo:

```text
entidades-femina-wikidata.tsv      → Femina
entities-heraldo-wikidata.tsv      → Heraldo
entidades-filipinas-wikidata.tsv   → Filipinas
```

El resultado son tres archivos principales:

```text
personas_revistas_combinado_es.tsv
gephi_edges_personas_revistas_es.csv
gephi_nodes_personas_revistas_es.csv
```

### Tabla combinada

La tabla `personas_revistas_combinado_es.tsv` sirve para revisar los datos antes o después de generar el grafo. Contiene, entre otras, las columnas:

```text
revista
persona
wikidata_qid
entity_original_clean
```

### Tabla de aristas

El archivo `gephi_edges_personas_revistas_es.csv` se importa en Gephi como tabla de aristas. Cada fila representa una relación entre una revista y una persona.

Columnas principales:

```text
Source
Target
Type
Weight
Label
revista
```

* `Source`: nodo de la revista.
* `Target`: nodo de la persona.
* `Type`: tipo de grafo, en este caso no dirigido.
* `Weight`: número de veces que la persona aparece en esa revista.
* `Label`: etiqueta legible de la arista.
* `revista`: revista de procedencia, útil para colorear aristas.

### Tabla de nodos

El archivo `gephi_nodes_personas_revistas_es.csv` se importa en Gephi como tabla de nodos.

Columnas principales:

```text
Id
Label
node_type
wikidata_qid
```

* `Id`: identificador interno estable del nodo.
* `Label`: nombre visible en el grafo.
* `node_type`: distingue entre `revista` y `persona`.
* `wikidata_qid`: identificador de Wikidata cuando existe.

Cuando existe QID, el script lo utiliza como identificador estable para evitar que la misma persona aparezca duplicada bajo nombres diferentes.

## 6. Visualización en Gephi

Los archivos generados se importan en Gephi:

https://gephi.org/

Gephi se utilizó para crear un grafo bipartito en el que:

* los nodos de tipo `revista` representan publicaciones;
* los nodos de tipo `persona` representan entidades personales;
* las aristas conectan cada persona con las revistas en las que aparece;
* el peso de la arista representa la frecuencia de aparición en una revista.

### Importación en Gephi

1. Abrir Gephi.
2. Ir a `File → Import Spreadsheet`.
3. Importar primero:

```text
gephi_edges_personas_revistas_es.csv
```

como `Edges table`.

4. Importar después:

```text
gephi_nodes_personas_revistas_es.csv
```

como `Nodes table`.

5. En `Overview`, aplicar un layout, por ejemplo:

```text
ForceAtlas 2
```

6. Colorear nodos por:

```text
node_type
```

7. Colorear aristas por:

```text
revista
```

8. Ajustar el tamaño de los nodos por:

```text
Degree
```

o, si se desea ponderar por número de menciones:

```text
Weighted Degree
```

### Interpretación del grafo

El grafo permite observar:

* qué personas aparecen en cada revista;
* qué entidades se repiten en más de una revista;
* qué figuras funcionan como conexiones entre publicaciones;
* qué revista concentra más menciones de determinadas personas;
* diferencias entre presencia puntual y frecuencia de mención.

Las personas conectadas con más de una revista son especialmente relevantes para estudiar circulación cultural, redes de autoría, menciones compartidas o referencias literarias e históricas comunes.

## Limitaciones

Este flujo de trabajo combina procesamiento automático y revisión manual. Por tanto, los resultados deben interpretarse teniendo en cuenta varias limitaciones:

* Las entidades proceden de OCR y pueden contener errores.
* NameTag puede producir falsos positivos o falsos negativos.
* OpenRefine facilita la agrupación de variantes, pero no elimina la necesidad de revisión humana.
* Wikidata no contiene todas las personas relevantes para un corpus histórico.
* Algunas entidades pueden estar reconciliadas con ítems incorrectos.
* Algunas etiquetas de Wikidata pueden aparecer en idiomas distintos o no disponer de etiqueta española.
* Las entidades literarias, religiosas, mitológicas o alegóricas pueden ser ambiguas.
* La categoría `PER` puede incluir tanto personas reales como personajes, figuras religiosas o nombres simbólicos.

Por estas razones, el grafo debe entenderse como una visualización exploratoria y no como una representación definitiva de todas las relaciones históricas presentes en las revistas.

## Requisitos

Los scripts están escritos en Python y utilizan principalmente:

```text
pandas
re
pathlib
urllib
json
```

Para instalar `pandas`:

```bash
pip install pandas
```

o:

```bash
py -m pip install pandas
```

## Reproducibilidad

Para reproducir el flujo de trabajo:

1. Extraer entidades con NameTag usando el modelo español.
2. Exportar los resultados a CSV o TSV.
3. Abrir las tablas en OpenRefine.
4. Limpiar y agrupar variantes de entidades.
5. Reconciliar entidades de persona con Wikidata cuando sea posible.
6. Exportar las tablas con las columnas `entity_normalized_clean` y `wikidata_qid`.
7. Ejecutar `limpiar_entidades.py` si se desea una limpieza adicional.
8. Ejecutar `crear_gephi_personas_revistas.py`.
9. Importar en Gephi los archivos de nodos y aristas.
10. Aplicar layout, colores, filtros y exportar los grafos.

## Citas y referencias

### NameTag

NameTag. LINDAT/CLARIAH-CZ. Herramienta y servicio web para reconocimiento de entidades nombradas.
https://lindat.mff.cuni.cz/services/nametag/

Straková, J., Straka, M., & Hajič, J. NameTag: Open-source tool for named entity recognition.
Véase también la documentación y servicio de LINDAT/CLARIAH-CZ.

### OpenRefine

OpenRefine. Herramienta libre y de código abierto para trabajar con datos desordenados, limpiarlos, transformarlos y enriquecerlos con servicios externos.
https://openrefine.org/

Documentación sobre reconciliación en OpenRefine:
https://openrefine.org/docs/manual/reconciling

Documentación sobre reconciliación con Wikibase/Wikidata:
https://openrefine.org/docs/manual/wikibase/reconciling

### Wikidata reconciliation service

Wikidata reconciliation for OpenRefine. Servicio para alinear datasets con ítems de Wikidata desde OpenRefine.
https://wikidata-reconciliation.wmcloud.org/

### Wikidata

Wikidata. Base de conocimiento colaborativa y multilingüe.
https://www.wikidata.org/

### Gephi

Bastian, M., Heymann, S., & Jacomy, M. (2009). “Gephi: An Open Source Software for Exploring and Manipulating Networks.” International AAAI Conference on Weblogs and Social Media.

Gephi: The Open Graph Viz Platform.
https://gephi.org/

## Licencia

Indicar aquí la licencia del repositorio.

Por ejemplo:

```text
CC BY 4.0 para los datos derivados y la documentación.
MIT License para los scripts.
```

Antes de publicar los datos, conviene comprobar las condiciones de uso de los textos fuente, las imágenes o los OCR originales.
