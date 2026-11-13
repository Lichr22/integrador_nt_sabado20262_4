"""
Módulo de Consultas Analíticas sobre la entidad 'empresas'.

Script: src/consultas_empresas.py
Lee el archivo limpio 'datos/limpios/empresa_limpio.csv' y responde 5 preguntas
analíticas sobre los datos, utilizando filtros, ordenamientos y agregaciones con groupby.
Cada consulta se encuentra en su propia función, imprime la respuesta en consola
y persiste el resultado en 'datos/limpios/empresas_consulta_N.csv'.
"""

from pathlib import Path
import sys
import pandas as pd

# Detección dinámica de rutas usando Pathlib
CARPETA_PROYECTO = Path(__file__).resolve().parent.parent
CARPETA_DATOS_LIMPIOS = CARPETA_PROYECTO / "datos" / "limpios"


def obtener_ruta_archivo_limpio() -> Path:
    """Retorna la ruta del archivo limpio generado por la fase de limpieza."""
    ruta = CARPETA_DATOS_LIMPIOS / "empresa_limpio.csv"
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

    # Asegurar que la columna 'activa' sea de tipo booleano estricto
    if "activa" in df.columns:
        if df["activa"].dtype != bool:
            df["activa"] = df["activa"].astype(str).str.upper().isin(["TRUE", "1", "SI"])

    return df


def guardar_resultado(df_o_serie, nombre_archivo: str, index: bool = True) -> None:
    """Guarda el resultado de la consulta en 'datos/limpios/'."""
    CARPETA_DATOS_LIMPIOS.mkdir(parents=True, exist_ok=True)
    df_o_serie.to_csv(CARPETA_DATOS_LIMPIOS / nombre_archivo, sep=";", encoding="utf-8-sig", index=index)


# =============================================================================
# CONSULTA 1: Empresas Activas
# =============================================================================
def consulta_1_empresas_activas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pregunta 1: ¿Cuáles son las empresas que se encuentran actualmente activas?
    Filtro booleano: activa == True.
    """
    print("\n" + "=" * 70)
    print("CONSULTA 1: Empresas Activas")
    print("Pregunta: ¿Cuáles y cuántas empresas se encuentran activas en el sistema?")
    print("=" * 70)

    activas = df[df["activa"] == True]

    print(activas[["id", "nombre", "nit", "sector", "contacto", "activa"]].head(10))
    print(f"\n-> Total de empresas activas encontradas: {len(activas)} de {len(df)}")

    guardar_resultado(activas, "empresas_consulta_1.csv", index=False)
    print("-> Guardado en: datos/limpios/empresas_consulta_1.csv")
    return activas


# =============================================================================
# CONSULTA 2: Empresas de un Sector Ordenadas por Nombre
# =============================================================================
def consulta_2_empresas_por_sector_ordenadas(df: pd.DataFrame, sector: str = "Logistica") -> pd.DataFrame:
    """
    Pregunta 2: ¿Cuáles son las empresas pertenecientes al sector Logística,
    ordenadas alfabéticamente por su nombre?
    """
    print("\n" + "=" * 70)
    print(f"CONSULTA 2: Empresas del Sector '{sector}' Ordenadas Alfabéticamente")
    print(f"Pregunta: Listar empresas pertenecientes a '{sector}' ordenadas por nombre.")
    print("=" * 70)

    logistica = df[df["sector"] == sector].sort_values("nombre")

    print(logistica[["nombre", "sector", "nit", "contacto", "telefono"]].head(10))
    print(f"\n-> Total empresas en el sector '{sector}': {len(logistica)}")

    guardar_resultado(logistica, "empresas_consulta_2.csv", index=False)
    print("-> Guardado en: datos/limpios/empresas_consulta_2.csv")
    return logistica


# =============================================================================
# CONSULTA 3: Conteo Rápido de Empresas por Sector
# =============================================================================
def consulta_3_conteo_rapido_sector(df: pd.DataFrame) -> pd.Series:
    """
    Pregunta 3: ¿Cuántas empresas hay registradas en cada sector económico?
    Uso de value_counts() para conteo rápido.
    """
    print("\n" + "=" * 70)
    print("CONSULTA 3: Conteo Rápido de Empresas por Sector")
    print("Pregunta: ¿Cómo se distribuye la cantidad de empresas en cada sector?")
    print("=" * 70)

    conteo = df["sector"].value_counts()

    print(conteo)
    print(f"\n-> Total de sectores analizados: {len(conteo)}")

    guardar_resultado(conteo, "empresas_consulta_3.csv", index=True)
    print("-> Guardado en: datos/limpios/empresas_consulta_3.csv")
    return conteo


# =============================================================================
# CONSULTA 4: GROUPBY de Empresas por Sector (De Mayor a Menor)
# =============================================================================
def consulta_4_groupby_sector_descendente(df: pd.DataFrame) -> pd.Series:
    """
    Pregunta 4: Utilizando agregación GROUPBY, ¿cuántas empresas pertenecen a cada
    sector, ordenadas de mayor a menor cantidad?
    """
    print("\n" + "=" * 70)
    print("CONSULTA 4 (GROUPBY): Empresas por Sector (Mayor a Menor)")
    print("Pregunta: Conteo agrupado por sector ordenado descendentemente.")
    print("=" * 70)

    por_sector = df.groupby("sector")["id"].count().sort_values(ascending=False)

    print(por_sector)
    print(f"\n-> Sector líder con mayor número de empresas: {por_sector.index[0]} ({por_sector.iloc[0]})")

    guardar_resultado(por_sector, "empresas_consulta_4.csv", index=True)
    print("-> Guardado en: datos/limpios/empresas_consulta_4.csv")
    return por_sector


# =============================================================================
# CONSULTA 5: GROUPBY Doble de Activas e Inactivas por Sector
# =============================================================================
def consulta_5_groupby_doble_activa_sector(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pregunta 5: Utilizando GROUPBY multidimensional con unstack(), ¿cuántas empresas
    activas (True) e inactivas (False) existen en cada sector?
    """
    print("\n" + "=" * 70)
    print("CONSULTA 5 (GROUPBY DOBLE): Activas e Inactivas por Sector")
    print("Pregunta: Tabla cruzada de estado de actividad (True/False) agrupada por sector.")
    print("=" * 70)

    tabla = df.groupby(["sector", "activa"])["id"].count().unstack(fill_value=0)

    print(tabla)
    print("\n-> Resumen tabular generado con dimensiones:", tabla.shape)

    guardar_resultado(tabla, "empresas_consulta_5.csv", index=True)
    print("-> Guardado en: datos/limpios/empresas_consulta_5.csv")
    return tabla


# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================
def main():
    print("#" * 70)
    print("  EJECUCIÓN DE CONSULTAS ANALÍTICAS: EMPRESAS (SCRIPT src/consultas_empresas.py)")
    print("#" * 70)

    df_limpio = cargar_datos()
    print(f"[INFO] Archivo cargado exitosamente. Total registros limpios: {len(df_limpio)}")

    # Ejecución ordenada de las 5 consultas solicitadas
    consulta_1_empresas_activas(df_limpio)
    consulta_2_empresas_por_sector_ordenadas(df_limpio, sector="Logistica")
    consulta_3_conteo_rapido_sector(df_limpio)
    consulta_4_groupby_sector_descendente(df_limpio)
    consulta_5_groupby_doble_activa_sector(df_limpio)

    print("\n" + "#" * 70)
    print("  LAS 5 CONSULTAS FUERON EJECUTADAS Y EXPORTADAS EXITOSAMENTE")
    print("#" * 70)


if __name__ == "__main__":
    main()

