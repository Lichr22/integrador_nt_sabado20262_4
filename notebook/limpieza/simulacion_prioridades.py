"""
Módulo de Limpieza de Datos para la entidad 'prioridades'.

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
    exportar_prioridades_limpios,
)

NIVELES_VALIDOS = {
    "muy baja": 1,
    "baja": 2,
    "media": 3,
    "alta": 4,
    "critica": 5,
}

DIAS_VALIDOS = {
    1: 10,
    2: 7,
    3: 5,
    4: 2,
    5: 1,
}

PALABRAS_A_INT = {
    "uno": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5,
    "1": 1, "2": 2, "3": 3, "4": 4, "5": 5,
}


def limpiar_prioridades(df_crudo: pd.DataFrame) -> pd.DataFrame:
    """Aplica las reglas de limpieza sobre prioridades crudas."""
    df = df_crudo.copy()

    # 1. Eliminar duplicados exactos
    df = df.drop_duplicates(subset=["id"]).reset_index(drop=True)

    # 2. Normalizar 'nombre': limpiar espacios y minúsculas sin colisión entre 'baja' y 'muy baja'
    def normalizar_nombre(nombre):
        if pd.isna(nombre):
            return "media"
        n = str(nombre).strip().lower()
        if "muy" in n:
            return "muy baja"
        elif "baja" in n:
            return "baja"
        elif "crit" in n:
            return "critica"
        elif "alta" in n:
            return "alta"
        elif "med" in n:
            return "media"
        return "media"
    df["nombre"] = df["nombre"].apply(normalizar_nombre)

    # 3. Limpiar 'nivel': corregir textos y nulos a enteros usando el nombre
    def reparar_nivel(row):
        val = row["nivel"]
        if pd.isna(val) or str(val).strip() == "":
            return NIVELES_VALIDOS.get(row["nombre"], 3)
        val_str = str(val).strip().lower()
        if val_str in PALABRAS_A_INT:
            return PALABRAS_A_INT[val_str]
        try:
            return int(float(val_str))
        except (ValueError, TypeError):
            return NIVELES_VALIDOS.get(row["nombre"], 3)

    df["nivel"] = df.apply(reparar_nivel, axis=1).astype(int)

    # 4. Limpiar 'dias_max_respuesta': corregir 999 o nulos usando el nivel
    def reparar_dias(row):
        dias = row["dias_max_respuesta"]
        if pd.isna(dias) or dias == 999 or str(dias).strip() == "":
            return DIAS_VALIDOS.get(row["nivel"], 5)
        try:
            d_int = int(float(dias))
            return DIAS_VALIDOS.get(row["nivel"], d_int)
        except (ValueError, TypeError):
            return DIAS_VALIDOS.get(row["nivel"], 5)

    df["dias_max_respuesta"] = df.apply(reparar_dias, axis=1).astype(int)

    return df


def ejecutar_limpieza():
    ruta_crudo = CARPETA_CRUDOS / "prioridades_crudo.csv"
    if not ruta_crudo.exists():
        print(f"[ERROR] No se encontró el archivo {ruta_crudo}. Ejecuta primero main.py.")
        return None

    print(f"Cargando datos crudos desde: {ruta_crudo}")
    df_crudo = pd.read_csv(ruta_crudo, sep=";", encoding="utf-8-sig")

    print(f"Filas antes de limpieza: {len(df_crudo)}")
    df_limpio = limpiar_prioridades(df_crudo)
    print(f"Filas después de limpieza: {len(df_limpio)}")

    rutas = exportar_prioridades_limpios(df_limpio)
    print("Datos limpios exportados exitosamente a 'datos/limpios/':")
    for r in rutas:
        if r:
            print(f"  * {r}")
    return df_limpio


if __name__ == "__main__":
    ejecutar_limpieza()

