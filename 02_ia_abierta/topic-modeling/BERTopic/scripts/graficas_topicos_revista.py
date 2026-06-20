import pandas as pd
import matplotlib.pyplot as plt
import ast
import re
from pathlib import Path


# =========================
# CONFIGURACIÓN
# =========================

ARCHIVO_TOPICOS_REVISTA = "topicos_por_revista.csv"
ARCHIVO_TOPICOS = "topicos_bertopic.csv"

CARPETA_SALIDA = "graficas_topicos"

TOP_N = 10


# =========================
# FUNCIONES
# =========================

def limpiar_nombre_archivo(nombre):
    """
    Convierte el nombre de la revista en un nombre seguro para archivo.
    """
    nombre = nombre.lower()
    nombre = nombre.replace("á", "a").replace("é", "e").replace("í", "i")
    nombre = nombre.replace("ó", "o").replace("ú", "u").replace("ñ", "n")
    nombre = re.sub(r"[^a-z0-9]+", "_", nombre)
    nombre = nombre.strip("_")
    return nombre


def extraer_palabras_representacion(valor, max_palabras=8):
    """
    Extrae palabras asociadas a un tópico desde la columna Representation
    de BERTopic.

    BERTopic suele guardar Representation como algo parecido a:
    "['mujer', 'educación', 'hogar', ...]"
    """
    if pd.isna(valor):
        return ""

    valor = str(valor)

    try:
        lista = ast.literal_eval(valor)
        if isinstance(lista, list):
            return ", ".join([str(x) for x in lista[:max_palabras]])
    except Exception:
        pass

    # Si no se puede leer como lista, se limpia de forma básica
    valor = valor.replace("[", "").replace("]", "")
    valor = valor.replace("'", "").replace('"', "")
    palabras = [p.strip() for p in valor.split(",") if p.strip()]

    return ", ".join(palabras[:max_palabras])


def preparar_tabla_topicos(df_topicos):
    """
    Prepara una tabla con topic y palabras asociadas.
    """
    df_topicos = df_topicos.copy()

    # Normalizar nombre de columna del identificador de tópico
    if "Topic" in df_topicos.columns:
        df_topicos = df_topicos.rename(columns={"Topic": "topic"})
    elif "topic" not in df_topicos.columns:
        raise ValueError("No encuentro una columna llamada 'Topic' o 'topic' en topicos_bertopic.csv")

    # Buscar columna de palabras asociadas
    if "Representation" in df_topicos.columns:
        df_topicos["palabras"] = df_topicos["Representation"].apply(extraer_palabras_representacion)
    elif "Name" in df_topicos.columns:
        # BERTopic suele crear nombres como: 0_mujer_educacion_hogar
        df_topicos["palabras"] = (
            df_topicos["Name"]
            .astype(str)
            .str.replace(r"^\-?\d+_", "", regex=True)
            .str.replace("_", ", ")
        )
    else:
        raise ValueError(
            "No encuentro una columna 'Representation' ni 'Name' en topicos_bertopic.csv"
        )

    df_topicos["topic"] = df_topicos["topic"].astype(int)

    return df_topicos[["topic", "palabras"]]


# =========================
# CARGA DE DATOS
# =========================

df_revistas = pd.read_csv(ARCHIVO_TOPICOS_REVISTA)
df_topicos = pd.read_csv(ARCHIVO_TOPICOS)

# Normalizar nombres de columnas esperados
if "topic" not in df_revistas.columns:
    if "Topic" in df_revistas.columns:
        df_revistas = df_revistas.rename(columns={"Topic": "topic"})
    else:
        raise ValueError("No encuentro una columna llamada 'topic' en topicos_por_revista.csv")

if "revista" not in df_revistas.columns:
    raise ValueError("No encuentro una columna llamada 'revista' en topicos_por_revista.csv")

# Detectar columna de peso
if "porcentaje_en_revista" in df_revistas.columns:
    columna_peso = "porcentaje_en_revista"
    etiqueta_x = "Porcentaje dentro de la revista"
elif "porcentaje" in df_revistas.columns:
    columna_peso = "porcentaje"
    etiqueta_x = "Porcentaje dentro de la revista"
elif "n_chunks" in df_revistas.columns:
    columna_peso = "n_chunks"
    etiqueta_x = "Número de chunks"
elif "n_documentos" in df_revistas.columns:
    columna_peso = "n_documentos"
    etiqueta_x = "Número de documentos"
else:
    raise ValueError(
        "No encuentro una columna de peso: 'porcentaje_en_revista', 'porcentaje', 'n_chunks' o 'n_documentos'"
    )

df_revistas["topic"] = df_revistas["topic"].astype(int)

df_palabras = preparar_tabla_topicos(df_topicos)

# Unir distribución por revista con palabras del tópico
df = df_revistas.merge(df_palabras, on="topic", how="left")

df["palabras"] = df["palabras"].fillna("sin palabras asociadas")

# Eliminar tópico -1 si aparece: suele ser ruido
df = df[df["topic"] != -1].copy()


# =========================
# CREAR CARPETA DE SALIDA
# =========================

Path(CARPETA_SALIDA).mkdir(exist_ok=True)


# =========================
# GENERAR UNA GRÁFICA POR REVISTA
# =========================

revistas = sorted(df["revista"].dropna().unique())

for revista in revistas:
    df_r = df[df["revista"] == revista].copy()

    df_r = (
        df_r
        .sort_values(columna_peso, ascending=False)
        .head(TOP_N)
        .sort_values(columna_peso, ascending=True)
    )

    if df_r.empty:
        print(f"No hay datos para {revista}")
        continue

    # Etiqueta: tópico + palabras
    df_r["etiqueta"] = df_r.apply(
        lambda row: f"Tópico {row['topic']}: {row['palabras']}",
        axis=1
    )

    # Altura dinámica según número de tópicos
    altura = max(6, 0.75 * len(df_r))

    plt.figure(figsize=(13, altura))

    plt.barh(df_r["etiqueta"], df_r[columna_peso])

    plt.title(f"Diez tópicos más relevantes en {revista}", fontsize=16)
    plt.xlabel(etiqueta_x)
    plt.ylabel("Tópicos y palabras asociadas")

    # Añadir valores al final de cada barra
    max_valor = df_r[columna_peso].max()

    for i, valor in enumerate(df_r[columna_peso]):
        if "porcentaje" in columna_peso:
            texto_valor = f"{valor:.1f}%"
        else:
            texto_valor = f"{int(valor)}"

        plt.text(
            valor + max_valor * 0.01,
            i,
            texto_valor,
            va="center",
            fontsize=10
        )

    plt.tight_layout()

    nombre_archivo = limpiar_nombre_archivo(revista)
    salida_png = Path(CARPETA_SALIDA) / f"top_10_topicos_{nombre_archivo}.png"

    plt.savefig(salida_png, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Gráfica creada: {salida_png}")


print()
print("Proceso terminado.")
print(f"Las gráficas están en la carpeta: {CARPETA_SALIDA}")