import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Carpeta de trabajo
carpeta_topics = r"C:\Users\Rocio\nuevo_corpus\topics"
periodicos = ["femina", "filipinas", "heraldo"]

def obtener_top_10(texto_palabras):
    if pd.isna(texto_palabras): return ""
    lista = str(texto_palabras).split()
    return ", ".join(lista[:10])

# Procesamiento de datos reales
for p in periodicos:
    plt.close('all')
    
    ruta_claves = os.path.join(carpeta_topics, f"claves_topicos_{p}.txt")
    ruta_docs = os.path.join(carpeta_topics, f"composicion_documentos_{p}.txt")
    
    print(f"Calculando el impacto real del periódico: {p.upper()}")
    
    # 1. Leer las palabras clave de los tópicos
    df_claves = pd.read_csv(ruta_claves, sep="\t", names=["ID_Topico", "Falso_Peso", "Palabras_Clave"])
    df_claves["Top_10_Palabras"] = df_claves["Palabras_Clave"].apply(obtener_top_10)
    
    # 2. PARSEO DEL ARCHIVO (Adaptado a tu formato secuencial de decimales)
    totales_topicos = {}
    total_frases = 0
    
    with open(ruta_docs, 'r', encoding='utf-8') as f:
        for linea in f:
            # Saltamos comentarios o líneas vacías
            if linea.startswith('#') or not linea.strip():
                continue
            partes = linea.strip().split('\t')
            if len(partes) < 3:
                continue
            
            total_frases += 1
            
            # En tu formato: partes[0]=ID_Doc, partes[1]=Ruta, partes[2:]=Solo decimales
            proporciones_decimales = partes[2:]
            
            # Recorremos los decimales. La posición 't_id' es automáticamente el número de tópico
            for t_id, prop_str in enumerate(proporciones_decimales):
                try:
                    prop = float(prop_str)
                    totales_topicos[t_id] = totales_topicos.get(t_id, 0.0) + prop
                except ValueError:
                    # Por si acaso MALLET mete algún texto extraño al final de la línea
                    continue

    # Calculamos la proporción media real
    prevalencia_real = {t_id: suma_prop / total_frases for t_id, suma_prop in totales_topicos.items()}
    
    # Convertimos a DataFrame y unimos con las palabras clave
    df_real = pd.DataFrame(list(prevalencia_real.items()), columns=["ID_Topico", "Prevalencia_Real"])
    df_final = pd.merge(df_claves, df_real, on="ID_Topico")
    
    # Ordenamos por el impacto real en el texto
    df_ordenado = df_final.sort_values(by="Prevalencia_Real", ascending=False)
    
    # Generamos la etiqueta del eje Y
    df_ordenado["Etiqueta_Eje"] = df_ordenado.apply(
        lambda row: f"Tópico {row['ID_Topico']}: {row['Top_10_Palabras']}", axis=1
    )

    # 3. Graficar la verdadera realidad del periódico
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.set_theme(style="whitegrid")
    
    # Graficamos usando un degradado de azul (Oscuro para barras largas, claro para cortas)
    sns.barplot(
        x="Prevalencia_Real", 
        y="Etiqueta_Eje", 
        data=df_ordenado,
        orient="h",
        palette="Blues_r",
        ax=ax
    )

    ax.set_title(f"PREVALENCIA DE LOS TÓPICOS: {p.upper()}", fontsize=18, fontweight="bold", pad=20)
    ax.set_xlabel("Proporción en el corpus (Media de presencia por frase)", fontsize=13, fontweight="bold")
    ax.set_ylabel("Estructura del tópico (ID + Palabras Clave)", fontsize=13, fontweight="bold")
    ax.tick_params(axis='y', labelsize=11) 
    
    plt.tight_layout()
    
    # Guardamos el gráfico corregido
    plt.savefig(os.path.join(carpeta_topics, f"grafico_real_{p}.png"), dpi=300, bbox_inches='tight')
    plt.show()

print("\n¡Proceso completado! Ya deberías ver los tres gráficos independientes en tu panel.")