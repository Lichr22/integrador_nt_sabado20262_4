"""
Módulo de Limpieza de Datos para la entidad 'usuario'.

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
    exportar_usuarios_limpios,
)

ROLES_VALIDOS = ["administrador", "empresario", "estudiante", "profesor"]


def limpiar_usuario(df_crudo: pd.DataFrame) -> pd.DataFrame:
    """Aplica las reglas de limpieza y calidad de datos sobre usuarios crudos."""
    df = df_crudo.copy()

    # 1. Eliminar duplicados exactos
    df = df.drop_duplicates(subset=["id"]).reset_index(drop=True)

    # 2. Limpieza de 'nombre': quitar espacios sobrantes y capitalizar en título
    df["nombre"] = df["nombre"].astype(str).str.strip().str.title()

    # 3. Limpieza de 'correo':
    # Rellenar nulos con valor por defecto o sintético y validar arroba
    df["correo"] = df["correo"].fillna("sin_correo@ejemplo.com")
    def reparar_correo(correo):
        correo = str(correo).strip().lower()
        if "@" not in correo:
            correo = correo + "@ejemplo.com"
        return correo
    df["correo"] = df["correo"].apply(reparar_correo)

    # 4. Limpieza de 'rol': normalizar casing y espacios
    def normalizar_rol(rol):
        if pd.isna(rol):
            return "estudiante"
        rol_limpio = str(rol).strip().lower()
        for r in ROLES_VALIDOS:
            if r in rol_limpio or rol_limpio in r:
                return r
        return "estudiante"
    df["rol"] = df["rol"].apply(normalizar_rol)

    # 5. Limpieza de 'activo': convertir a booleano estricto (True/False)
    def normalizar_booleano(valor):
        val_str = str(valor).strip().upper()
        if val_str in ["SI", "1", "TRUE"]:
            return True
        elif val_str in ["NO", "0", "FALSE"]:
            return False
        return bool(valor)
    df["activo"] = df["activo"].apply(normalizar_booleano).astype(bool)

    # 6. Limpieza de 'fecha_registro': unificar formatos ISO y Latino a datetime estandarizado
    df["fecha_registro"] = pd.to_datetime(
        df["fecha_registro"],
        format="mixed",
        dayfirst=True,
        errors="coerce",
    ).dt.strftime("%Y-%m-%d %H:%M:%S")

    return df


def ejecutar_limpieza():
    ruta_crudo = CARPETA_CRUDOS / "usuario_crudo.csv"
    if not ruta_crudo.exists():
        print(f"[ERROR] No se encontró el archivo {ruta_crudo}. Ejecuta primero main.py.")
        return None

    print(f"Cargando datos crudos desde: {ruta_crudo}")
    df_crudo = pd.read_csv(ruta_crudo, sep=";", encoding="utf-8-sig")

    print(f"Filas antes de limpieza: {len(df_crudo)}")
    df_limpio = limpiar_usuario(df_crudo)
    print(f"Filas después de limpieza: {len(df_limpio)}")

    rutas = exportar_usuarios_limpios(df_limpio)
    print("Datos limpios exportados exitosamente a 'datos/limpios/':")
    for r in rutas:
        if r:
            print(f"  * {r}")
    return df_limpio


if __name__ == "__main__":
    ejecutar_limpieza()

