"""
Módulo de Consultas Analíticas sobre la entidad 'categorias'.

Script: src/consultas_categorias.py
Lee el archivo limpio 'data/limpio/categorias_limpio.csv' y responde 5 preguntas
analíticas sobre los datos, utilizando conteo de frecuencias, filtrado de cadenas
y agregaciones con groupby (longitud de texto, distribución por área y tabla cruzada).
Cada consulta se encuentra en su propia función, imprime la respuesta en consola
y persiste el resultado en 'data/limpio/categorias_consulta_N.csv'.
"""

from pathlib import Path
import sys
import pandas as pd

# Detección dinámica de rutas usando Pathlib
CARPETA_PROYECTO = Path(__file__).resolve().parent.parent
CARPETA_DATA_LIMPIO = CARPETA_PROYECTO / "data" / "limpio"
CARPETA_DATOS_LIMPIOS = CARPETA_PROYECTO / "datos" / "limpios"


def obtener_ruta_archivo_limpio() -> Path:
    """Localiza el archivo limpio de categorias dando prioridad a 'data/limpio/'."""
    rutas_candidatas = [
        CARPETA_DATA_LIMPIO / "categorias_limpio.csv",
        CARPETA_DATOS_LIMPIOS / "categorias_limpio.csv",
        CARPETA_DATA_LIMPIO / "categoria_limpio.csv",
        CARPETA_DATOS_LIMPIOS / "categoria_limpio.csv",
    ]

    for ruta in rutas_candidatas:
        if ruta.exists():
            return ruta

    raise FileNotFoundError(
        f"No se encontró el archivo limpio de categorias en:\n"
        f"- {CARPETA_DATA_LIMPIO / 'categorias_limpio.csv'}\n"
        f"- {CARPETA_DATOS_LIMPIOS / 'categorias_limpio.csv'}\n"
        "Asegúrate de ejecutar primero la fase de limpieza."
    )


def cargar_datos() -> pd.DataFrame:
    """Carga el DataFrame limpio detectando delimitador y asegurando la columna largo_desc."""
    ruta = obtener_ruta_archivo_limpio()
    try:
        df = pd.read_csv(ruta, sep=None, engine="python", encoding="utf-8-sig")
    except Exception:
        df = pd.read_csv(ruta, sep=";", encoding="utf-8-sig")

    # Asegurar que descripcion sea texto y rellenar nulos residuales
    if "descripcion" in df.columns:
        df["descripcion"] = df["descripcion"].fillna("Sin descripcion").astype(str).str.strip()

    # Asegurar columna largo_desc
    if "largo_desc" in df.columns:
        df["largo_desc"] = pd.to_numeric(df["largo_desc"], errors="coerce")
    elif "descripcion" in df.columns:
        df["largo_desc"] = df["descripcion"].str.len()

    return df


def guardar_resultado(df_o_serie, nombre_archivo: str, index: bool = True) -> None:
    """Guarda el resultado en 'data/limpio/' y sincroniza con 'datos/limpios/'."""
    CARPETA_DATA_LIMPIO.mkdir(parents=True, exist_ok=True)
    ruta_data = CARPETA_DATA_LIMPIO / nombre_archivo
    df_o_serie.to_csv(ruta_data, sep=";", encoding="utf-8-sig", index=index)

    # Mantener sincronizado si existe datos/limpios/
    if CARPETA_DATOS_LIMPIOS.exists():
        ruta_datos = CARPETA_DATOS_LIMPIOS / nombre_archivo
        df_o_serie.to_csv(ruta_datos, sep=";", encoding="utf-8-sig", index=index)


# =============================================================================
# CONSULTA 1: Cuántas veces aparece cada categoría (detecta las variantes)
# =============================================================================
def consulta_1_frecuencia_categorias(df: pd.DataFrame) -> pd.Series:
    """
    Pregunta 1: ¿Cuántas veces aparece cada categoría registrada en la plataforma?
    Conteo de frecuencias para validar la normalización de variantes.
    """
    print("\n" + "=" * 70)
    print("CONSULTA 1: Cuántas veces aparece cada categoría")
    print("Pregunta: Conteo de frecuencias por categoría para verificar variantes.")
    print("=" * 70)

    conteo = df["nombre"].value_counts()

    print(conteo)
    print(f"\n-> Total de categorías únicas consolidadas: {len(conteo)}")

    guardar_resultado(conteo, "categorias_consulta_1.csv", index=True)
    print("-> Guardado en: data/limpio/categorias_consulta_1.csv")
    return conteo


# =============================================================================
# CONSULTA 2: Categorías sin descripción
# =============================================================================
def consulta_2_categorias_sin_descripcion(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pregunta 2: ¿Cuáles son las categorías que no poseen una descripción asignada?
    Filtro de registros con valor estándar 'Sin descripcion'.
    """
    print("\n" + "=" * 70)
    print("CONSULTA 2: Categorías sin descripción")
    print("Pregunta: Filtrar registros con descripción marcada como 'Sin descripcion'.")
    print("=" * 70)

    sin_desc = df[df["descripcion"] == "Sin descripcion"]

    print(sin_desc[["id", "nombre", "area_responsable", "descripcion"]].head(10))
    print(f"\n-> Total de categorías sin descripción: {len(sin_desc)} de {len(df)}")

    guardar_resultado(sin_desc, "categorias_consulta_2.csv", index=False)
    print("-> Guardado en: data/limpio/categorias_consulta_2.csv")
    return sin_desc


# =============================================================================
# CONSULTA 3: GROUPBY - Largo promedio de la descripción por categoría
# =============================================================================
def consulta_3_groupby_largo_promedio_descripcion(df: pd.DataFrame) -> pd.Series:
    """
    Pregunta 3: Utilizando GROUPBY, ¿cuál es el largo promedio (en caracteres)
    de la descripción de cada categoría, ordenado de mayor a menor?
    """
    print("\n" + "=" * 70)
    print("CONSULTA 3 (GROUPBY): Largo promedio de la descripción por categoría")
    print("Pregunta: Longitud promedio de caracteres en la descripción por categoría.")
    print("=" * 70)

    largos = df.groupby("nombre")["largo_desc"].mean().round(1).sort_values(ascending=False)

    print(largos)
    print(f"\n-> Largo promedio calculado exitosamente para {len(largos)} categorías.")

    guardar_resultado(largos, "categorias_consulta_3.csv", index=True)
    print("-> Guardado en: data/limpio/categorias_consulta_3.csv")
    return largos


# =============================================================================
# CONSULTA 4: GROUPBY - Cuántas categorías maneja cada área
# =============================================================================
def consulta_4_groupby_categorias_por_area(df: pd.DataFrame) -> pd.Series:
    """
    Pregunta 4: Utilizando GROUPBY, ¿cuántas categorías están a cargo de cada
    área responsable, ordenadas de mayor a menor?
    """
    print("\n" + "=" * 70)
    print("CONSULTA 4 (GROUPBY): Cuántas categorías maneja cada área")
    print("Pregunta: Conteo de categorías asignadas a cada área responsable.")
    print("=" * 70)

    por_area = df.groupby("area_responsable")["id"].count().sort_values(ascending=False)

    print(por_area)
    print(f"\n-> Total de áreas responsables analizadas: {len(por_area)}")

    guardar_resultado(por_area, "categorias_consulta_4.csv", index=True)
    print("-> Guardado en: data/limpio/categorias_consulta_4.csv")
    return por_area


# =============================================================================
# CONSULTA 5: GROUPBY doble - Categorías por área (tabla cruzada)
# =============================================================================
def consulta_5_groupby_doble_categorias_por_area(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pregunta 5: Utilizando GROUPBY doble y unstack, ¿cómo se distribuyen las
    categorías en cada área responsable en una tabla cruzada bidimensional?
    """
    print("\n" + "=" * 70)
    print("CONSULTA 5 (GROUPBY DOBLE): Categorías por área (tabla cruzada)")
    print("Pregunta: Matriz cruzada de categorías por área responsable (unstack con fill_value=0).")
    print("=" * 70)

    tabla = df.groupby(["area_responsable", "nombre"])["id"].count().unstack(fill_value=0)

    print(tabla)
    print(f"\n-> Tabla cruzada generada con dimensiones: {tabla.shape[0]} áreas x {tabla.shape[1]} categorías.")

    guardar_resultado(tabla, "categorias_consulta_5.csv", index=True)
    print("-> Guardado en: data/limpio/categorias_consulta_5.csv")
    return tabla


# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================
def main():
    print("#" * 70)
    print("  EJECUCIÓN DE CONSULTAS ANALÍTICAS: CATEGORÍAS (src/consultas_categorias.py)")
    print("#" * 70)

    df_limpio = cargar_datos()
    print(f"[INFO] Archivo limpio cargado exitosamente. Total registros: {len(df_limpio)}")

    # Ejecución ordenada de las cinco consultas requeridas
    consulta_1_frecuencia_categorias(df_limpio)
    consulta_2_categorias_sin_descripcion(df_limpio)
    consulta_3_groupby_largo_promedio_descripcion(df_limpio)
    consulta_4_groupby_categorias_por_area(df_limpio)
    consulta_5_groupby_doble_categorias_por_area(df_limpio)

    print("\n" + "#" * 70)
    print("  LAS 5 CONSULTAS DE CATEGORÍAS FUERON EJECUTADAS Y EXPORTADAS CON ÉXITO")
    print("#" * 70)


if __name__ == "__main__":
    main()

