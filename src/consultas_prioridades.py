"""
Módulo de Consultas Analíticas sobre la entidad 'prioridades'.

Script: src/consultas_prioridades.py
Lee el archivo limpio 'datos/limpios/prioridades_limpio.csv' y responde 5 preguntas
analíticas sobre los datos, utilizando ordenamiento, filtros booleanos y agregaciones con groupby.
Cada consulta se encuentra en su propia función, imprime la respuesta en consola
y persiste el resultado en 'datos/limpios/prioridades_consulta_N.csv'.
"""

from pathlib import Path
import sys
import pandas as pd

# Detección dinámica de rutas usando Pathlib
CARPETA_PROYECTO = Path(__file__).resolve().parent.parent
CARPETA_DATOS_LIMPIOS = CARPETA_PROYECTO / "datos" / "limpios"


def obtener_ruta_archivo_limpio() -> Path:
    """Retorna la ruta del archivo limpio generado por la fase de limpieza."""
    ruta = CARPETA_DATOS_LIMPIOS / "prioridades_limpio.csv"
    if not ruta.exists():
        raise FileNotFoundError(
            f"No se encontró {ruta}.\n"
            "Ejecuta primero la fase de limpieza: python main.py --limpiar"
        )
    return ruta


def cargar_datos() -> pd.DataFrame:
    """Carga el DataFrame limpio detectando automáticamente delimitador y codificación."""
    ruta = obtener_ruta_archivo_limpio()
    try:
        df = pd.read_csv(ruta, sep=None, engine="python", encoding="utf-8-sig")
    except Exception:
        df = pd.read_csv(ruta, sep=";", encoding="utf-8-sig")

    # Asegurar tipos numéricos en nivel y dias_max_respuesta
    if "nivel" in df.columns:
        df["nivel"] = pd.to_numeric(df["nivel"], errors="coerce")
    if "dias_max_respuesta" in df.columns:
        df["dias_max_respuesta"] = pd.to_numeric(df["dias_max_respuesta"], errors="coerce")

    return df


def guardar_resultado(df_o_serie, nombre_archivo: str, index: bool = True) -> None:
    """Guarda el resultado de la consulta en 'datos/limpios/'."""
    CARPETA_DATOS_LIMPIOS.mkdir(parents=True, exist_ok=True)
    df_o_serie.to_csv(CARPETA_DATOS_LIMPIOS / nombre_archivo, sep=";", encoding="utf-8-sig", index=index)


# =============================================================================
# CONSULTA 1: Prioridades Ordenadas de Más Urgente a Menos Urgente
# =============================================================================
def consulta_1_prioridades_ordenadas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pregunta 1: ¿Cómo quedan ordenadas las prioridades de la más urgente (nivel 1)
    a la menos urgente (nivel 5)?
    """
    print("\n" + "=" * 70)
    print("CONSULTA 1: Prioridades Ordenadas de Más Urgente a Menos Urgente")
    print("Pregunta: Listar prioridades ordenadas por nivel ascendente (1 a 5).")
    print("=" * 70)

    ordenadas = df.sort_values("nivel")

    print(ordenadas.head(10))
    print(f"\n-> Total registros ordenados: {len(ordenadas)}")

    guardar_resultado(ordenadas, "prioridades_consulta_1.csv", index=False)
    print("-> Guardado en: datos/limpios/prioridades_consulta_1.csv")
    return ordenadas


# =============================================================================
# CONSULTA 2: Solo las Prioridades Urgentes (Nivel 1 y 2)
# =============================================================================
def consulta_2_prioridades_urgentes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pregunta 2: ¿Cuáles son las prioridades críticas y urgentes (niveles 1 y 2)?
    Filtro numérico: nivel <= 2.
    """
    print("\n" + "=" * 70)
    print("CONSULTA 2: Solo las Prioridades Urgentes (Niveles 1 y 2)")
    print("Pregunta: Filtrar registros con nivel de urgencia crítico o alto (nivel <= 2).")
    print("=" * 70)

    urgentes = df[df["nivel"] <= 2]

    print(urgentes.head(10))
    print(f"\n-> Total de prioridades urgentes (nivel <= 2): {len(urgentes)} de {len(df)}")

    guardar_resultado(urgentes, "prioridades_consulta_2.csv", index=False)
    print("-> Guardado en: datos/limpios/prioridades_consulta_2.csv")
    return urgentes


# =============================================================================
# CONSULTA 3: Cuántas Veces Aparece Cada Nombre (Frecuencia de Nombres)
# =============================================================================
def consulta_3_conteo_nombres(df: pd.DataFrame) -> pd.Series:
    """
    Pregunta 3: ¿Cuántas veces aparece registrado cada nombre de prioridad?
    Uso de value_counts() para detectar frecuencias de nombres estandarizados.
    """
    print("\n" + "=" * 70)
    print("CONSULTA 3: Frecuencia de Cada Nombre de Prioridad")
    print("Pregunta: ¿Cuántas veces aparece cada nombre estandarizado en la tabla?")
    print("=" * 70)

    conteo = df["nombre"].value_counts()

    print(conteo)
    print(f"\n-> Total de categorías de prioridad distintas: {len(conteo)}")

    guardar_resultado(conteo, "prioridades_consulta_3.csv", index=True)
    print("-> Guardado en: datos/limpios/prioridades_consulta_3.csv")
    return conteo


# =============================================================================
# CONSULTA 4: GROUPBY - Cuántas Filas Hay por Nivel
# =============================================================================
def consulta_4_groupby_filas_por_nivel(df: pd.DataFrame) -> pd.Series:
    """
    Pregunta 4: Utilizando agregación GROUPBY, ¿cuántos registros existen por cada
    nivel numérico de prioridad?
    """
    print("\n" + "=" * 70)
    print("CONSULTA 4 (GROUPBY): Cantidad de Filas por Nivel")
    print("Pregunta: Conteo agrupado de registros por cada nivel numérico (1 al 5).")
    print("=" * 70)

    por_nivel = df.groupby("nivel")["id"].count()

    print(por_nivel)
    print(f"\n-> Total de niveles analizados: {len(por_nivel)}")

    guardar_resultado(por_nivel, "prioridades_consulta_4.csv", index=True)
    print("-> Guardado en: datos/limpios/prioridades_consulta_4.csv")
    return por_nivel


# =============================================================================
# CONSULTA 5: GROUPBY - Días de Respuesta Mínimo, Promedio y Máximo por Prioridad
# =============================================================================
def consulta_5_groupby_dias_respuesta_resumen(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pregunta 5: Utilizando GROUPBY y agregaciones múltiples (min, mean, max), ¿cuáles
    son los días de respuesta mínimo, promedio y máximo para cada nombre de prioridad?
    """
    print("\n" + "=" * 70)
    print("CONSULTA 5 (GROUPBY): Días de Respuesta Mínimo, Promedio y Máximo")
    print("Pregunta: Estadísticas (min, promedio, max) de días de respuesta por nombre de prioridad.")
    print("=" * 70)

    resumen = df.groupby("nombre")["dias_max_respuesta"].agg(["min", "mean", "max"]).round(1)

    print(resumen)
    print(f"\n-> Resumen estadístico agrupado generado exitosamente.")

    guardar_resultado(resumen, "prioridades_consulta_5.csv", index=True)
    print("-> Guardado en: datos/limpios/prioridades_consulta_5.csv")
    return resumen


# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================
def main():
    print("#" * 70)
    print("  EJECUCIÓN DE CONSULTAS ANALÍTICAS: PRIORIDADES (src/consultas_prioridades.py)")
    print("#" * 70)

    df_limpio = cargar_datos()
    print(f"[INFO] Archivo limpio cargado exitosamente. Total registros: {len(df_limpio)}")

    # Ejecución ordenada de las cinco consultas requeridas
    consulta_1_prioridades_ordenadas(df_limpio)
    consulta_2_prioridades_urgentes(df_limpio)
    consulta_3_conteo_nombres(df_limpio)
    consulta_4_groupby_filas_por_nivel(df_limpio)
    consulta_5_groupby_dias_respuesta_resumen(df_limpio)

    print("\n" + "#" * 70)
    print("  LAS 5 CONSULTAS DE PRIORIDADES FUERON EJECUTADAS Y EXPORTADAS")
    print("#" * 70)


if __name__ == "__main__":
    main()

