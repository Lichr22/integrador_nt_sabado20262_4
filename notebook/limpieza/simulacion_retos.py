"""
Módulo de Limpieza de Datos para la entidad 'retos'.

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
    exportar_retos_limpios,
)

ESTADOS_VALIDOS = ["ACTIVO", "NO_ACTIVO", "BLOQUEADO", "EN_REVISION", "EN_CURSO", "CERRADO"]


def limpiar_retos(df_crudo: pd.DataFrame) -> pd.DataFrame:
    """Aplica las reglas de limpieza sobre retos crudos."""
    df = df_crudo.copy()

    # 1. Eliminar duplicados exactos
    df = df.drop_duplicates(subset=["id"]).reset_index(drop=True)

    # 2. Limpiar 'nombre': quitar espacios sobrantes
    df["nombre"] = df["nombre"].astype(str).str.strip()

    # 3. Limpiar 'descripcion': rellenar nulos
    df["descripcion"] = df["descripcion"].fillna("Descripción no especificada").str.strip()

    # 4. Limpiar 'fecha_inicio': estandarizar a formato YYYY-MM-DD
    df["fecha_inicio"] = pd.to_datetime(
        df["fecha_inicio"], format="mixed", dayfirst=True, errors="coerce"
    )

    # 5. Limpiar 'fecha_fin': rellenar nulos y corregir error lógico (fin anterior a inicio)
    df["fecha_fin"] = pd.to_datetime(
        df["fecha_fin"], format="mixed", dayfirst=True, errors="coerce"
    )
    # Rellenar nulos con fecha_inicio + 30 días
    nulos_fin = df["fecha_fin"].isna()
    df.loc[nulos_fin, "fecha_fin"] = df.loc[nulos_fin, "fecha_inicio"] + pd.Timedelta(days=30)

    # Corregir error lógico: si fecha_fin <= fecha_inicio, ajustar a fecha_inicio + 30 días
    anteriores = df["fecha_fin"] <= df["fecha_inicio"]
    df.loc[anteriores, "fecha_fin"] = df.loc[anteriores, "fecha_inicio"] + pd.Timedelta(days=30)

    # Calcular duración en días
    df["duracion_dias"] = (df["fecha_fin"] - df["fecha_inicio"]).dt.days

    # Convertir ambas fechas a formato string estándar
    df["fecha_inicio"] = df["fecha_inicio"].dt.strftime("%Y-%m-%d")
    df["fecha_fin"] = df["fecha_fin"].dt.strftime("%Y-%m-%d")

    # 6. Limpiar 'estado': corregir casing y variantes
    def normalizar_estado(estado):
        if pd.isna(estado):
            return "ACTIVO"
        e = str(estado).strip().lower().replace("-", " ").replace("_", " ")
        if "revis" in e:
            return "EN_REVISION"
        elif "curso" in e:
            return "EN_CURSO"
        elif "no activo" in e:
            return "NO_ACTIVO"
        elif "bloq" in e:
            return "BLOQUEADO"
        elif "cerrad" in e:
            return "CERRADO"
        return "ACTIVO"

    df["estado"] = df["estado"].apply(normalizar_estado)

    return df


def ejecutar_limpieza():
    ruta_crudo = CARPETA_CRUDOS / "retos_crudo.csv"
    if not ruta_crudo.exists():
        print(f"[ERROR] No se encontró el archivo {ruta_crudo}. Ejecuta primero main.py.")
        return None

    print(f"Cargando datos crudos desde: {ruta_crudo}")
    df_crudo = pd.read_csv(ruta_crudo, sep=";", encoding="utf-8-sig")

    print(f"Filas antes de limpieza: {len(df_crudo)}")
    df_limpio = limpiar_retos(df_crudo)
    print(f"Filas después de limpieza: {len(df_limpio)}")

    rutas = exportar_retos_limpios(df_limpio)
    print("Datos limpios exportados exitosamente a 'datos/limpios/':")
    for r in rutas:
        if r:
            print(f"  * {r}")
    return df_limpio


if __name__ == "__main__":
    ejecutar_limpieza()

