"""
Módulo de Limpieza de Datos para la entidad 'categoria'.

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
    exportar_categorias_limpios,
)

AREAS_VALIDAS = ["Marketing", "Ventas", "Desarrollo", "Soporte", "Innovacion", "Operaciones"]


def limpiar_categoria(df_crudo: pd.DataFrame) -> pd.DataFrame:
    """Aplica las reglas de limpieza y calidad sobre categorias crudas."""
    df = df_crudo.copy()

    # 1. Eliminar duplicados exactos por id
    df = df.drop_duplicates(subset=["id"]).reset_index(drop=True)

    # 2. Limpieza de 'nombre': quitar espacios sobrantes y capitalizar en título
    df["nombre"] = df["nombre"].astype(str).str.strip().str.title()

    # 3. Limpieza de 'descripcion': rellenar nulos
    df["descripcion"] = df["descripcion"].fillna("Sin descripción asignada").str.strip()

    # 4. Limpieza de 'area_responsable': rellenar nulos y normalizar
    def normalizar_area(area):
        if pd.isna(area):
            return "General"
        a = str(area).strip().title()
        for valid in AREAS_VALIDAS:
            if valid.lower() == a.lower():
                return valid
        return "General"
    df["area_responsable"] = df["area_responsable"].apply(normalizar_area)

    return df


def ejecutar_limpieza():
    ruta_crudo = CARPETA_CRUDOS / "categoria_crudo.csv"
    if not ruta_crudo.exists():
        print(f"[ERROR] No se encontró el archivo {ruta_crudo}. Ejecuta primero main.py.")
        return None

    print(f"Cargando datos crudos desde: {ruta_crudo}")
    df_crudo = pd.read_csv(ruta_crudo, sep=";", encoding="utf-8-sig")

    print(f"Filas antes de limpieza: {len(df_crudo)}")
    df_limpio = limpiar_categoria(df_crudo)
    print(f"Filas después de limpieza: {len(df_limpio)}")

    rutas = exportar_categorias_limpios(df_limpio)
    print("Datos limpios exportados exitosamente a 'datos/limpios/':")
    for r in rutas:
        if r:
            print(f"  * {r}")
    return df_limpio


if __name__ == "__main__":
    ejecutar_limpieza()

