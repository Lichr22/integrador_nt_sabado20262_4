"""
Módulo de Consultas Analíticas sobre la entidad 'retos'.

Script: src/consultas_retos.py
Lee el archivo limpio 'datos/limpios/retos_limpio.csv' y responde 5 preguntas
analíticas sobre los datos, utilizando filtrado booleano, nlargest, conteo de frecuencias
y agregaciones avanzadas con groupby (duración y evolución mensual).
Cada consulta se encuentra en su propia función, imprime la respuesta en consola
y persiste el resultado en 'datos/limpios/retos_consulta_N.csv'.
"""

from pathlib import Path
import sys
import pandas as pd

# Detección dinámica de rutas usando Pathlib
CARPETA_PROYECTO = Path(__file__).resolve().parent.parent
CARPETA_DATOS_LIMPIOS = CARPETA_PROYECTO / "datos" / "limpios"


def obtener_ruta_archivo_limpio() -> Path:
    """Retorna la ruta del archivo limpio generado por la fase de limpieza."""
    ruta = CARPETA_DATOS_LIMPIOS / "retos_limpio.csv"
    if not ruta.exists():
        raise FileNotFoundError(
            f"No se encontró {ruta}.\n"
            "Ejecuta primero la fase de limpieza: python main.py --limpiar"
        )
    return ruta


def cargar_datos() -> pd.DataFrame:
    """Carga el DataFrame limpio detectando delimitador y asegurando tipos datetime y numéricos."""
    ruta = obtener_ruta_archivo_limpio()
    try:
        df = pd.read_csv(ruta, sep=None, engine="python", encoding="utf-8-sig")
    except Exception:
        df = pd.read_csv(ruta, sep=";", encoding="utf-8-sig")

    # Asegurar tipo datetime en fechas para habilitar el accesor .dt
    if "fecha_inicio" in df.columns:
        df["fecha_inicio"] = pd.to_datetime(df["fecha_inicio"], errors="coerce")
    if "fecha_fin" in df.columns:
        df["fecha_fin"] = pd.to_datetime(df["fecha_fin"], errors="coerce")

    # Asegurar duración en días (numérico)
    if "duracion_dias" in df.columns:
        df["duracion_dias"] = pd.to_numeric(df["duracion_dias"], errors="coerce")
    elif "fecha_inicio" in df.columns and "fecha_fin" in df.columns:
        df["duracion_dias"] = (df["fecha_fin"] - df["fecha_inicio"]).dt.days

    # Estandarizar valores de estado a mayúsculas con guion bajo (ej. EN_CURSO)
    if "estado" in df.columns:
        df["estado"] = (
            df["estado"]
            .astype(str)
            .str.strip()
            .str.upper()
            .str.replace(" ", "_")
        )

    return df


def guardar_resultado(df_o_serie, nombre_archivo: str, index: bool = True) -> None:
    """Guarda el resultado de la consulta en 'datos/limpios/'."""
    CARPETA_DATOS_LIMPIOS.mkdir(parents=True, exist_ok=True)
    df_o_serie.to_csv(CARPETA_DATOS_LIMPIOS / nombre_archivo, sep=";", encoding="utf-8-sig", index=index)


# =============================================================================
# CONSULTA 1: Retos que están en curso
# =============================================================================
def consulta_1_retos_en_curso(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pregunta 1: ¿Cuáles son todos los retos que actualmente se encuentran en curso?
    Filtro booleano: df["estado"] == "EN_CURSO".
    """
    print("\n" + "=" * 70)
    print("CONSULTA 1: Retos que están en curso")
    print("Pregunta: Filtrar todos los retos con estado 'EN_CURSO'.")
    print("=" * 70)

    en_curso = df[df["estado"] == "EN_CURSO"]

    print(en_curso[["id", "nombre", "estado", "fecha_inicio", "fecha_fin", "duracion_dias"]].head(10))
    print(f"\n-> Total de retos en curso: {len(en_curso)} de {len(df)}")

    guardar_resultado(en_curso, "retos_consulta_1.csv", index=False)
    print("-> Guardado en: datos/limpios/retos_consulta_1.csv")
    return en_curso


# =============================================================================
# CONSULTA 2: Los 10 retos más largos
# =============================================================================
def consulta_2_retos_mas_largos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pregunta 2: ¿Cuáles son los 10 retos con mayor duración en días?
    Uso de nlargest() seleccionando columnas clave: nombre, duracion_dias y estado.
    """
    print("\n" + "=" * 70)
    print("CONSULTA 2: Los 10 retos más largos")
    print("Pregunta: Obtener los 10 retos con mayor duración en días y su estado.")
    print("=" * 70)

    largos = df.nlargest(10, "duracion_dias")[["nombre", "duracion_dias", "estado"]]

    print(largos)
    print(f"\n-> Top 10 retos más largos obtenido exitosamente.")

    guardar_resultado(largos, "retos_consulta_2.csv", index=False)
    print("-> Guardado en: datos/limpios/retos_consulta_2.csv")
    return largos


# =============================================================================
# CONSULTA 3: Cuántos retos hay por estado
# =============================================================================
def consulta_3_retos_por_estado(df: pd.DataFrame) -> pd.Series:
    """
    Pregunta 3: ¿Cuántos retos existen por cada estado operativo?
    Conteo rápido mediante value_counts().
    """
    print("\n" + "=" * 70)
    print("CONSULTA 3: Cuántos retos hay por estado")
    print("Pregunta: Distribución y conteo de retos según su estado operativo.")
    print("=" * 70)

    conteo = df["estado"].value_counts()

    print(conteo)
    print(f"\n-> Total de estados distintos registrados: {len(conteo)}")

    guardar_resultado(conteo, "retos_consulta_3.csv", index=True)
    print("-> Guardado en: datos/limpios/retos_consulta_3.csv")
    return conteo


# =============================================================================
# CONSULTA 4: GROUPBY - Duración promedio, mínima y máxima por estado
# =============================================================================
def consulta_4_groupby_duracion_por_estado(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pregunta 4: Utilizando agregación GROUPBY, ¿cuál es el conteo, duración
    promedio y duración máxima de los retos según su estado?
    """
    print("\n" + "=" * 70)
    print("CONSULTA 4 (GROUPBY): Duración por Estado")
    print("Pregunta: Estadísticas (count, mean, max) de la duración en días por estado.")
    print("=" * 70)

    resumen = df.groupby("estado")["duracion_dias"].agg(["count", "mean", "max"]).round(1)

    print(resumen)
    print(f"\n-> Resumen de duración por estado generado exitosamente.")

    guardar_resultado(resumen, "retos_consulta_4.csv", index=True)
    print("-> Guardado en: datos/limpios/retos_consulta_4.csv")
    return resumen


# =============================================================================
# CONSULTA 5: GROUPBY por mes - Cuántos retos empiezan cada mes
# =============================================================================
def consulta_5_groupby_retos_por_mes(df: pd.DataFrame) -> pd.Series:
    """
    Pregunta 5: Utilizando GROUPBY por período mensual, ¿cuántos retos inician cada mes?
    Agrupación temporal: df["fecha_inicio"].dt.to_period("M").
    """
    print("\n" + "=" * 70)
    print("CONSULTA 5 (GROUPBY): Cuántos retos empiezan cada mes")
    print("Pregunta: Conteo temporal de retos agrupados por mes de inicio.")
    print("=" * 70)

    por_mes = df.groupby(df["fecha_inicio"].dt.to_period("M"))["id"].count()

    print(por_mes)
    print(f"\n-> Total de períodos mensuales registrados: {len(por_mes)}")

    guardar_resultado(por_mes, "retos_consulta_5.csv", index=True)
    print("-> Guardado en: datos/limpios/retos_consulta_5.csv")
    return por_mes


# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================
def main():
    print("#" * 70)
    print("  EJECUCIÓN DE CONSULTAS ANALÍTICAS: RETOS (src/consultas_retos.py)")
    print("#" * 70)

    df_limpio = cargar_datos()
    print(f"[INFO] Archivo limpio cargado exitosamente. Total registros: {len(df_limpio)}")

    # Ejecución ordenada de las cinco consultas requeridas
    consulta_1_retos_en_curso(df_limpio)
    consulta_2_retos_mas_largos(df_limpio)
    consulta_3_retos_por_estado(df_limpio)
    consulta_4_groupby_duracion_por_estado(df_limpio)
    consulta_5_groupby_retos_por_mes(df_limpio)

    print("\n" + "#" * 70)
    print("  LAS 5 CONSULTAS DE RETOS FUERON EJECUTADAS Y EXPORTADAS CON ÉXITO")
    print("#" * 70)


if __name__ == "__main__":
    main()

