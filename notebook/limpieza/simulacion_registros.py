"""
Módulo de Limpieza de Datos para la entidad 'registros'.

Lee los datos crudos desde 'datos/crudos/', corrige los defectos
inyectados durante la simulación y exporta los datos limpios a 'datos/limpios/'.
"""

from pathlib import Path
import sys
import pandas as pd

# Importar exportación
CARPETA_PROYECTO = Path(__file__).resolve().parents[2]
if str(CARPETA_PROYECTO) not in sys.path:
    sys.path.insert(0, str(CARPETA_PROYECTO))

from notebook.exportacion.exportacion import (
    CARPETA_CRUDOS,
    exportar_registros_limpios,
)

ESTADOS_VALIDOS = ["ACTIVO", "NO_ACTIVO", "BLOQUEADO", "EN_REVISION", "EN_CURSO", "FINALIZADO"]


def limpiar_registros(df_crudo: pd.DataFrame) -> pd.DataFrame:
    """Aplica las reglas de limpieza sobre registros crudos."""
    df = df_crudo.copy()

    # 1. Eliminar duplicados exactos por id
    df = df.drop_duplicates(subset=["id"]).reset_index(drop=True)

    # 2. Limpiar 'observacion': rellenar nulos
    df["observacion"] = df["observacion"].fillna("Sin observaciones registradas").str.strip()

    # 3. Limpiar 'estado': corregir variantes y casing (normalizar a FINALIZADO, EN_CURSO, etc.)
    def normalizar_estado(estado):
        if pd.isna(estado):
            return "ACTIVO"
        e = str(estado).strip().lower().replace("-", " ").replace("_", " ")
        if "cerrad" in e or "finaliz" in e:
            return "FINALIZADO"
        elif "curso" in e:
            return "EN_CURSO"
        elif "no activo" in e:
            return "NO_ACTIVO"
        elif "revis" in e:
            return "EN_REVISION"
        elif "bloq" in e:
            return "BLOQUEADO"
        return "ACTIVO"

    df["estado"] = df["estado"].apply(normalizar_estado)

    # 4. Limpiar 'fecha_registro': unificar formatos a YYYY-MM-DD HH:MM:SS
    fechas_dt = pd.to_datetime(
        df["fecha_registro"], format="mixed", dayfirst=True, errors="coerce"
    )
    df["fecha_registro"] = fechas_dt.dt.strftime("%Y-%m-%d %H:%M:%S")

    # 5. Generar columna 'mes' para análisis temporal (formato YYYY-MM)
    df["mes"] = fechas_dt.dt.strftime("%Y-%m")

    return df


def ejecutar_limpieza():
    ruta_crudo = CARPETA_CRUDOS / "registros_crudo.csv"
    if not ruta_crudo.exists():
        print(f"[ERROR] No se encontró el archivo {ruta_crudo}. Ejecuta primero main.py.")
        return None

    print(f"Cargando datos crudos desde: {ruta_crudo}")
    df_crudo = pd.read_csv(ruta_crudo, sep=";", encoding="utf-8-sig")

    print(f"Filas antes de limpieza: {len(df_crudo)}")
    df_limpio = limpiar_registros(df_crudo)
    print(f"Filas después de limpieza: {len(df_limpio)}")

    rutas = exportar_registros_limpios(df_limpio)

    print("Datos limpios exportados exitosamente a 'datos/limpios/':")
    for r in rutas:
        if r:
            print(f"  * {r}")
    return df_limpio


if __name__ == "__main__":
    ejecutar_limpieza()

