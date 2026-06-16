# Topic modeling

Este directorio reúne el proceso y los resultados de **modelado de temas** aplicado a los tres corpus hemerográficos del repositorio:

- `femina`
- `filipinas`
- `heraldo`

El análisis se ha realizado con dos herramientas:

1. **MALLET**, usado para preparar un corpus por frases, generar modelos de tópicos y calcular la composición temática de los documentos.
2. **Voyant Tools**, usado como herramienta de exploración visual e interactiva y para exportar listas de tópicos y pesos.

La comparación entre ambos resultados permite valorar qué temas aparecen de forma consistente en los dos métodos y qué diferencias dependen del algoritmo, del preprocesamiento o del ruido textual del corpus.

---

## Estructura de la carpeta

```text
topic_modeling/
├── mallet/
│   ├── claves_topicos/
│   │   ├── claves_topicos_femina.txt
│   │   ├── claves_topicos_filipinas.txt
│   │   └── claves_topicos_heraldo.txt
│   ├── composicion_documentos/
│   │   ├── composicion_documentos_femina.txt
│   │   ├── composicion_documentos_filipinas.txt
│   │   └── composicion_documentos_heraldo.txt
│   ├── corpus_por_frases/
│   ├── graficos/
│   ├── scripts/
│   │   ├── gráficos-topics.py
│   │   ├── preparar_texto.py
│   │   ├── run_mallet.txt
│   │   └── script_mallet.txt
│   ├── topicos/
│   └── stop-words.txt
└── voyant/
    ├── gráficos/
    ├── pesos/
    │   ├── weight_voyant_femina.csv
    │   ├── weight_voyant_filipinas.csv
    │   └── weight_voyant_heraldo.csv
    └── topicos/
        ├── topic-voyant-femina.csv
        ├── topic-voyant-filipinas.csv
        └── topic-voyant-heraldo.csv
```

---

## Flujo de trabajo con MALLET

## Reproducibilidad

Para reproducir el análisis es necesario tener instalado MALLET localmente y ajustar la variable `$MALLET_HOME` en los scripts correspondientes. Las rutas personales han sido sustituidas por rutas relativas al repositorio o por rutas genéricas para evitar dependencias del entorno local de trabajo.

El flujo completo de reproducción es el siguiente:

1. Preparar los textos con `mallet/scripts/preparar_texto.py`.
2. Importar los textos procesados a formato MALLET con `mallet/scripts/script_mallet.txt`.
3. Entrenar los modelos de tópicos con `mallet/scripts/run_mallet.txt`.
4. Generar los gráficos de prevalencia con `mallet/scripts/gráficos-topics.py`.
5. Comparar los resultados con las exportaciones de Voyant Tools conservadas en `voyant/topicos/` y `voyant/pesos/`.

Los resultados publicados en este directorio corresponden a tres corpus:

- `femina`
- `filipinas`
- `heraldo`

### 1. Preparación del corpus por frases

El script `mallet/scripts/preparar_texto.py` transforma un texto continuo en un archivo segmentado por frases. El proceso documentado en el script consiste en:

1. leer un archivo de entrada;
2. reemplazar saltos de línea internos por espacios;
3. normalizar espacios múltiples;
4. insertar saltos de línea después de puntos seguidos de mayúscula;
5. guardar un archivo en el que cada frase ocupa una línea.

En el script conservado, el ejemplo está configurado para `heraldo`:

```python
ruta_entrada = "C:/Users/.../heraldo_merged.txt"
ruta_salida = "C:/Users/.../heraldo_por_frases.txt"
```

La unidad de análisis usada para MALLET es, por tanto, la **frase**. Esta decisión es importante porque los resultados de composición documental y los gráficos posteriores calculan la presencia media de cada tópico por frase.

### 2. Importación del corpus en MALLET

El archivo `mallet/scripts/script_mallet.txt` documenta la importación del corpus a formato MALLET:

```powershell
C:\Users\...\mallet\bin\mallet.bat import-file ^
  --input nuevo_corpus\por_frases\heraldo_por_frases.txt ^
  --output nuevo_corpus\topics_heraldo.mallet ^
  --keep-sequence ^
  --remove-stopwords ^
  --stoplist-file "C:\Users\Rocio\nuevo_corpus\stop-words.txt" ^
  --token-regex "\p{L}+"
```

Parámetros relevantes:

- `import-file`: importa un único archivo de entrada.
- `--keep-sequence`: conserva el orden secuencial de los tokens.
- `--remove-stopwords`: elimina palabras vacías.
- `--stoplist-file`: usa la lista personalizada `stop-words.txt`.
- `--token-regex "\p{L}+"`: conserva secuencias formadas por letras, lo que permite trabajar con palabras acentuadas y otros caracteres alfabéticos.

### 3. Entrenamiento de tópicos

El archivo `mallet/scripts/run_mallet.txt` documenta el entrenamiento:

```powershell
$env:MALLET_HOME = "C:\Users\...\mallet"

C:\Users\...\mallet\bin\mallet.bat train-topics ^
  --input nuevo_corpus/topics_filipinas.mallet ^
  --num-topics 10 ^
  --optimize-interval 10 ^
  --output-topic-keys nuevo_corpus/claves_topicos.txt ^
  --output-doc-topics nuevo_corpus/composicion_documentos.txt
```

Este comando genera dos tipos principales de salida:

- `claves_topicos_*.txt`: palabras clave de cada tópico.
- `composicion_documentos_*.txt`: distribución de tópicos por unidad documental.


### 4. Cálculo de prevalencia y generación de gráficos

El script `mallet/scripts/gráficos-topics.py` procesa los resultados de MALLET para cada uno de los tres periódicos:

```python
periodicos = ["femina", "filipinas", "heraldo"]
```

El script:

1. lee las claves de tópicos;
2. lee la composición documental;
3. suma la proporción de cada tópico en todas las frases;
4. calcula la prevalencia media de cada tópico;
5. ordena los tópicos por prevalencia;
6. genera un gráfico de barras horizontal para cada periódico.

La etiqueta del eje X queda definida como:

```python
"Proporción en el corpus (Media de presencia por frase)"
```

Por tanto, los gráficos de MALLET no representan únicamente una lista de palabras clave, sino una estimación de la presencia media de cada tópico en el corpus segmentado por frases.

---

## Resultados de MALLET

Los archivos `claves_topicos_*.txt` contienen 10 tópicos por corpus. Cada línea incluye:

1. identificador del tópico;
2. peso o valor asociado;
3. palabras clave del tópico.

### *Fémina*

En `claves_topicos_femina.txt` se observan varios conjuntos temáticos interpretables:

- **Mujer, hogar y sociedad:** `mujer`, `hombre`, `vida`, `hogar`, `patria`, `mujeres`, `sociedad`, `social`, `amor`, `moral`.
- **Lírica, amor y sensibilidad:** `amor`, `alma`, `vida`, `ojos`, `corazón`, `dulce`, `luz`, `sol`, `cielo`, `dios`, `flores`.
- **Identidad editorial de la revista:** `fémina`, `revista`, `macorís`, `san`, `pedro`, `página`, `edición`, `número`.
- **Cultura dominicana y americanismo:** `mujeres`, `república`, `liga`, `américa`, `internacional`, `colón`, `hispano`, `mundo`.
- **Figuras intelectuales femeninas:** `petronila`, `gomez`, `mujer`, `maestra`, `angelica`, `literatura`, `normal`, `ciencias`, `nación`.

También aparecen tópicos con mezcla de léxico narrativo, anuncios o ruido editorial, como `casa`, `centavos`, `vender`, `precio`, `artículos`.

### *Filipinas*

En `claves_topicos_filipinas.txt` aparecen temas muy marcados por la condición multilingüe y por el carácter hemerográfico del corpus:

- **Mujer, educación y hogar:** `mujer`, `hombre`, `casa`, `educación`, `vida`, `hogar`, `madre`, `hijos`, `familia`, `niños`.
- **Léxico en tagalo o filipino:** `sa`, `ng`, `ang`, `na`, `at`, `ay`, `babae`, `hindi`, `kung`, `lalaki`.
- **Anuncios, alimentación e higiene:** `harina`, `nestle`, `agua`, `lacteada`, `higiene`, `alimento`, `leche`, `medicinas`.
- **Manila, suscripciones y economía editorial:** `manila`, `mes`, `filipinas`, `provincias`, `años`, `pesos`, `subscripción`, `precios`.
- **Lírica amorosa:** `amor`, `vida`, `corazón`, `alma`, `noche`, `flores`, `alegría`, `madre`, `luz`.

La presencia de un tópico en tagalo/filipino es especialmente relevante: indica que el corpus no es monolingüe.

### *El Heraldo de la Mujer*

En `claves_topicos_heraldo.txt` destacan estos bloques:

- **Mujer, derechos y progreso:** `mujer`, `mujeres`, `vida`, `mundo`, `hombres`, `pueblo`, `progreso`, `derecho`, `patria`, `humanidad`.
- **Puerto Rico y figuras/personas del corpus:** `rico`, `puerto`, `mujer`, `mujeres`, `duprey`, `sra`, `san`, `ana`, `señora`, `puertorriqueña`.
- **Publicidad y productos:** `pomada`, `mercado`, `americano`, `pecas`, `cutánea`, `producto`, `manchas`.
- **Moda y comercio:** `casa`, `bellas`, `preciosos`, `correo`, `trajes`, `crepé`, `corte`, `surtido`.
- **Lírica y corporalidad amorosa:** `mar`, `labios`, `ojos`, `mañana`, `manos`, `amor`, `noche`, `joven`, `flores`.

También aparecen tópicos con mezcla lingüística, por ejemplo `or`, `to`, `in`, `the`, `american`, `be`, `her`, `men`, `is`, `on`.

---

## Resultados de Voyant Tools

Los archivos de Voyant se conservan en dos subcarpetas:

- `voyant/topicos/`: palabras de cada tópico.
- `voyant/pesos/`: pesos exportados por Voyant.

Los archivos de tópicos están separados por punto y coma, aunque tienen extensión `.csv`.

### *Fémina*

En `topic-voyant-femina.csv` aparecen tópicos con palabras asociadas a:

- mujer e interioridad: `mujer`, `alma`, `espiritual`, `historia`, `conciencia`;
- patria, revista y sociedad: `patria`, `revista`, `pueblo`, `petronila`, `sociedad`;
- intelectualidad y república: `fémina`, `hombres`, `intelectual`, `palabra`, `república`;
- cultura, hogar y evolución: `hogar`, `cultura`, `noble`, `evolución`, `santo`;
- nación dominicana: `dominicana`, `libertad`, `tierra`, `mundo`, `nacional`.

Los resultados coinciden parcialmente con MALLET en la centralidad de `mujer`, `patria`, `sociedad`, `hogar`, `república`, `dominicana` y `fémina`.

### *Filipinas*

En `topic-voyant-filipinas.csv` los tópicos son más dispersos. Aparecen algunos ejes interpretables:

- mujer, ciencia y vida: `mujer`, `ciencia`, `vida`, `palabra`;
- hombre, educación y mujeres: `hombre`, `educación`, `mujeres`, `vida`;
- Manila y objetos de circulación: `ferrocarril`, `manila`, `abanicos`, `hijos`;
- naturaleza y México: `página`, `naturaleza`, `fuerza`, `antigua`, `méxico`;
- ciudad y publicidad: `ciudad`, `sociales`, `espíritu`, `publicidad`, `diario`.

Sin embargo, también aparecen términos difíciles de interpretar o probablemente procedentes del OCR, la segmentación o el contexto publicitario: `mulas`, `cascabel`, `tinding`, `marfil`, `sombreros`, `bizcochos`, `fabricados`.

### *El Heraldo de la Mujer*

En `topic-voyant-heraldo.csv` la salida muestra un nivel alto de ruido textual. Hay algunos términos relevantes:

- mujer y mundo: `mujer`, `amor`, `mar`, `mundo`;
- derechos y correspondencia: `derechos`, `señoras`, `cartas`, `recibiendo`;
- cultura y revista: `cultura`, `revista`, `mundial`, `número`;
- Heraldo, Puerto Rico y literatas: `heraldo`, `puerto`, `puertorriqueñas`, `literatas`, `retratos`.

Pero predominan términos fragmentarios o ruidosos: `empre`, `abonaremos`, `roqué`, `quesen`, `agan`, `vor`, `sas`, `vue`, `estra`, `aquena`, `anas`, `baring`, `rrera`. En este corpus, Voyant parece más sensible que MALLET al ruido de OCR, fragmentos tipográficos y residuos editoriales.

---

## Comparación entre MALLET y Voyant Tools

### Diferencias generales

| Aspecto | MALLET | Voyant Tools |
|---|---|---|
| Tipo de uso | Modelado reproducible mediante comandos y scripts | Exploración visual e interactiva |
| Unidad documentada | Frases, según `preparar_texto.py` y `gráficos-topics.py` | No queda documentada explícitamente en los archivos exportados pero con la herramienta spyral y la exportación de enlaces es reproducible|
| Preprocesamiento visible | Sí: stopwords, token regex, segmentación por frases | Parcial |
| Resultados principales | Claves de tópicos, composición documental y prevalencia | Tópicos y pesos exportados |
| Interpretabilidad | Mayor en los tres corpus, especialmente en `femina` y `heraldo` | Variable; más útil como exploración inicial |
| Sensibilidad al ruido | Menor, aunque no lo elimina por completo | Mayor, sobre todo en `filipinas` y `heraldo` |

### Coincidencias temáticas

Los dos métodos detectan la centralidad de campos semánticos vinculados con:

- mujer, mujeres, hogar, sociedad y educación;
- patria, nación, república, pueblo y mundo;
- amor, alma, corazón, flores, noche y sensibilidad lírica;
- nombres de lugares, periódicos y referencias editoriales;
- anuncios, productos y léxico comercial.

Estas coincidencias sugieren que los temas principales del corpus están relacionados con la escritura de mujeres, la formación intelectual y moral, la identidad nacional o transnacional, la sociabilidad cultural y la convivencia entre textos literarios, ensayísticos y publicitarios.

### 5. Referencias

McCallum, Andrew Kachites. 2002. “MALLET: A Machine Learning for Language Toolkit.” http://mallet.cs.umass.edu.

Sinclair, Stéfan, and Geoffrey Rockwell. 2016. *Voyant Tools*. http://voyant-tools.org.