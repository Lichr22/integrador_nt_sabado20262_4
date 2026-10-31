"""
Módulo de Limpieza de Datos para la entidad 'empresa'.

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
    exportar_empresas_limpios,
)

SECTORES_VALIDOS = ["Comunicaciones", "Retail", "Logistica", "Agro", "Alimentos", "Tecnologia"]


def limpiar_empresa(df_crudo: pd.DataFrame) -> pd.DataFrame:
    """Aplica las reglas de limpieza y calidad de datos sobre empresas crudas."""
    df = df_crudo.copy()

    # 1. Eliminar duplicados exactos y duplicados por NIT
    df = df.drop_duplicates(subset=["id"]).reset_index(drop=True)
    df = df.drop_duplicates(subset=["nit"]).reset_index(drop=True)

    # 2. Limpieza de 'nombre': quitar espacios sobrantes y capitalizar en título
    df["nombre"] = df["nombre"].astype(str).str.strip().str.title()

    # 3. Limpieza de 'nit': estandarizar a solo dígitos (10 dígitos)
    df["nit"] = df["nit"].astype(str).str.replace(r"[^0-9]", "", regex=True)

    # 4. Limpieza de 'sector': normalizar casing y espacios
    def normalizar_sector(sector):
        if pd.isna(sector):
            return "Tecnologia"
        s = str(sector).strip().title()
        for valid in SECTORES_VALIDOS:
            if valid.lower() == s.lower():
                return valid
        return "Tecnologia"
    df["sector"] = df["sector"].apply(normalizar_sector)

    # 5. Limpieza de 'contacto': rellenar nulos
    df["contacto"] = df["contacto"].fillna("Contacto Principal").str.strip().str.title()

    # 6. Limpieza de 'correo': asegurar arroba
    def reparar_correo(correo):
        if pd.isna(correo):
            return "empresa@dominio.com"
        c = str(correo).strip().lower()
        if "@" not in c:
            c = c + "@empresa.com"
        return c
    df["correo"] = df["correo"].apply(reparar_correo)

    # 7. Limpieza de 'telefono': extraer solo dígitos (10 dígitos limpios)
    def normalizar_telefono(tel):
        if pd.isna(tel):
            return "3000000000"
        digitos = "".join([d for d in str(tel) if d.isdigit()])
        if len(digitos) > 10 and digitos.startswith("57"):
            digitos = digitos[2:]
        return digitos[:10]
    df["telefono"] = df["telefono"].apply(normalizar_telefono)

    # 8. Limpieza de 'activa': convertir a booleano estricto
    def normalizar_booleano(valor):
        val_str = str(valor).strip().upper()
        if val_str in ["SI", "1", "TRUE"]:
            return True
        elif val_str in ["NO", "0", "FALSE"]:
            return False
        return bool(valor)
    df["activa"] = df["activa"].apply(normalizar_booleano).astype(bool)

    return df


def ejecutar_limpieza():
    ruta_crudo = CARPETA_CRUDOS / "empresa_crudo.csv"
    if not ruta_crudo.exists():
        print(f"[ERROR] No se encontró el archivo {ruta_crudo}. Ejecuta primero main.py.")
        return None

    print(f"Cargando datos crudos desde: {ruta_crudo}")
    df_crudo = pd.read_csv(ruta_crudo, sep=";", encoding="utf-8-sig")

    print(f"Filas antes de limpieza: {len(df_crudo)}")
    df_limpio = limpiar_empresa(df_crudo)
    print(f"Filas después de limpieza: {len(df_limpio)}")

    rutas = exportar_empresas_limpios(df_limpio)
    print("Datos limpios exportados exitosamente a 'datos/limpios/':")
    for r in rutas:
        if r:
            print(f"  * {r}")
    return df_limpio


if __name__ == "__main__":
    ejecutar_limpieza()

