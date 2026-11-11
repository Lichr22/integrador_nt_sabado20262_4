"""
Módulo de Consultas Analíticas sobre la entidad 'registros' (participaciones en retos).

Script: src/consultas_registros.py
Lee el archivo limpio 'data/limpio/registros_limpio.csv' y responde 5 preguntas
analíticas sobre los datos, utilizando filtrado booleano, detección de duplicados
por subconjunto de columnas, conteo de frecuencias y agregaciones con groupby.
Cada consulta se encuentra en su propia función, imprime la respuesta en consola
y persiste el resultado en 'data/limpio/registros_consulta_N.csv'.
"""

from pathlib import Path
import sys
import pandas as pd

# Detección dinámica de rutas usando Pathlib
CARPETA_PROYECTO = Path(__file__).resolve().parent.parent
CARPETA_DATA_LIMPIO = CARPETA_PROYECTO / "data" / "limpio"
CARPETA_DATOS_LIMPIOS = CARPETA_PROYECTO / "datos" / "limpios"


def obtener_ruta_archivo_limpio() -> Path:
    """Localiza el archivo limpio de registros dando prioridad a 'data/limpio/'."""
    rutas_candidatas = [
        CARPETA_DATA_LIMPIO / "registros_limpio.csv",
        CARPETA_DATOS_LIMPIOS / "registros_limpio.csv",
        CARPETA_DATA_LIMPIO / "registro_limpio.csv",
        CARPETA_DATOS_LIMPIOS / "registro_limpio.csv",
    ]

    for ruta in rutas_candidatas:
        if ruta.exists():
            return ruta

    raise FileNotFoundError(
        f"No se encontró el archivo limpio de registros en:\n"
        f"- {CARPETA_DATA_LIMPIO / 'registros_limpio.csv'}\n"
        f"- {CARPETA_DATOS_LIMPIOS / 'registros_limpio.csv'}\n"
        "Asegúrate de ejecutar primero la fase de limpieza."
    )


def cargar_datos() -> pd.DataFrame:
    """Carga el DataFrame limpio detectando delimitador y asegurando la columna 'mes' y estados."""
    ruta = obtener_ruta_archivo_limpio()
    try:
        df = pd.read_csv(ruta, sep=None, engine="python", encoding="utf-8-sig")
    except Exception:
        df = pd.read_csv(ruta, sep=";", encoding="utf-8-sig")

    # Asegurar que el estado esté normalizado
    if "estado" in df.columns:
        df["estado"] = (
            df["estado"]
            .astype(str)
            .str.strip()
            .str.upper()
            .str.replace(" ", "_")
        )

    # Asegurar columna 'mes' para agregaciones temporales
    if "mes" not in df.columns and "fecha_registro" in df.columns:
        fechas_dt = pd.to_datetime(df["fecha_registro"], errors="coerce")
        df["mes"] = fechas_dt.dt.strftime("%Y-%m")

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
# CONSULTA 1: Participaciones ya finalizadas
# =============================================================================
def consulta_1_participaciones_finalizadas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pregunta 1: ¿Cuáles son las participaciones o registros que ya se encuentran finalizados?
    Filtro booleano: df["estado"] == "FINALIZADO".
    """
    print("\n" + "=" * 70)
    print("CONSULTA 1: Participaciones ya finalizadas")
    print("Pregunta: Filtrar participaciones con estado 'FINALIZADO'.")
    print("=" * 70)

    finalizados = df[df["estado"] == "FINALIZADO"]

    print(finalizados[["id", "id_usuario", "id_reto", "estado", "fecha_registro"]].head(10))
    print(f"\n-> Total de participaciones finalizadas: {len(finalizados)} de {len(df)}")

    guardar_resultado(finalizados, "registros_consulta_1.csv", index=False)
    print("-> Guardado en: data/limpio/registros_consulta_1.csv")
    return finalizados


# =============================================================================
# CONSULTA 2: Participaciones repetidas (mismo usuario en el mismo reto)
# =============================================================================
def consulta_2_participaciones_repetidas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pregunta 2: ¿Cuáles son las participaciones repetidas donde un mismo usuario
    se encuentra inscrito múltiples veces en el mismo reto?
    Filtro de duplicados por subconjunto: subset=["id_usuario", "id_reto"], keep=False.
    """
    print("\n" + "=" * 70)
    print("CONSULTA 2: Participaciones repetidas (mismo usuario en el mismo reto)")
    print("Pregunta: Detectar registros duplicados por usuario y reto (keep=False).")
    print("=" * 70)

    repetidos = df[df.duplicated(subset=["id_usuario", "id_reto"], keep=False)]

    print(repetidos[["id", "id_usuario", "id_reto", "estado", "fecha_registro"]].head(10))
    print(f"\n-> Total de registros con usuario y reto repetido: {len(repetidos)} de {len(df)}")

    guardar_resultado(repetidos, "registros_consulta_2.csv", index=False)
    print("-> Guardado en: data/limpio/registros_consulta_2.csv")
    return repetidos


# =============================================================================
# CONSULTA 3: Cuántas participaciones hay por estado
# =============================================================================
def consulta_3_participaciones_por_estado(df: pd.DataFrame) -> pd.Series:
    """
    Pregunta 3: ¿Cuántas participaciones existen según su estado operativo?
    Conteo rápido mediante value_counts().
    """
    print("\n" + "=" * 70)
    print("CONSULTA 3: Cuántas participaciones hay por estado")
    print("Pregunta: Distribución y conteo de participaciones por estado.")
    print("=" * 70)

    conteo = df["estado"].value_counts()

    print(conteo)
    print(f"\n-> Total de estados registrados: {len(conteo)}")

    guardar_resultado(conteo, "registros_consulta_3.csv", index=True)
    print("-> Guardado en: data/limpio/registros_consulta_3.csv")
    return conteo


# =============================================================================
# CONSULTA 4: GROUPBY - Los 10 retos con más participantes
# =============================================================================
def consulta_4_groupby_top_retos_participantes(df: pd.DataFrame) -> pd.Series:
    """
    Pregunta 4: Utilizando agregación GROUPBY, ¿cuáles son los 10 retos con mayor
    número de participantes inscritos?
    """
    print("\n" + "=" * 70)
    print("CONSULTA 4 (GROUPBY): Los 10 retos con más participantes")
    print("Pregunta: Conteo agrupado de participantes por reto, obteniendo los 10 mayores.")
    print("=" * 70)

    top_retos = df.groupby("id_reto")["id"].count().nlargest(10)

    print(top_retos)
    print(f"\n-> Top 10 retos con mayor cantidad de participantes obtenido exitosamente.")

    guardar_resultado(top_retos, "registros_consulta_4.csv", index=True)
    print("-> Guardado en: data/limpio/registros_consulta_4.csv")
    return top_retos


# =============================================================================
# CONSULTA 5: GROUPBY por mes - Cuántas participaciones hubo cada mes
# =============================================================================
def consulta_5_groupby_participaciones_por_mes(df: pd.DataFrame) -> pd.Series:
    """
    Pregunta 5: Utilizando GROUPBY por período mensual, ¿cuántas participaciones
    se registraron cada mes a lo largo del tiempo?
    """
    print("\n" + "=" * 70)
    print("CONSULTA 5 (GROUPBY): Cuántas participaciones hubo cada mes")
    print("Pregunta: Conteo temporal de participaciones agrupadas por mes de registro.")
    print("=" * 70)

    por_mes = df.groupby("mes")["id"].count()

    print(por_mes)
    print(f"\n-> Total de meses analizados: {len(por_mes)}")

    guardar_resultado(por_mes, "registros_consulta_5.csv", index=True)
    print("-> Guardado en: data/limpio/registros_consulta_5.csv")
    return por_mes


# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================
def main():
    print("#" * 70)
    print("  EJECUCIÓN DE CONSULTAS ANALÍTICAS: REGISTROS (src/consultas_registros.py)")
    print("#" * 70)

    df_limpio = cargar_datos()
    print(f"[INFO] Archivo limpio cargado exitosamente. Total registros: {len(df_limpio)}")

    # Ejecución ordenada de las cinco consultas requeridas
    consulta_1_participaciones_finalizadas(df_limpio)
    consulta_2_participaciones_repetidas(df_limpio)
    consulta_3_participaciones_por_estado(df_limpio)
    consulta_4_groupby_top_retos_participantes(df_limpio)
    consulta_5_groupby_participaciones_por_mes(df_limpio)

    print("\n" + "#" * 70)
    print("  LAS 5 CONSULTAS DE REGISTROS FUERON EJECUTADAS Y EXPORTADAS CON ÉXITO")
    print("#" * 70)


if __name__ == "__main__":
    main()

