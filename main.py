"""
Script Principal Orquestador del Proyecto Integrador.

Ejecuta el flujo de generación, ensuciado y exportación de datos crudos
para las entidades 'usuario', 'empresa' y 'categoria'.
"""

from pathlib import Path
import sys

# Asegurar que la raíz del proyecto esté en el path de Python
CARPETA_PROYECTO = Path(__file__).resolve().parent
if str(CARPETA_PROYECTO) not in sys.path:
    sys.path.insert(0, str(CARPETA_PROYECTO))

import pandas as pd

# Módulos de simulación
from notebook.simulaciones.simulacion_usuario import (
    FILAS as FILAS_USUARIOS,
    generar_datos as generar_datos_usuarios,
    ensuciar as ensuciar_usuarios,
)
from notebook.simulaciones.simulacion_empresa import (
    FILAS as FILAS_EMPRESAS,
    generar_datos as generar_datos_empresas,
    ensuciar as ensuciar_empresas,
)
from notebook.simulaciones.simulacion_categorias import (
    FILAS as FILAS_CATEGORIAS,
    generar_datos as generar_datos_categorias,
    ensuciar as ensuciar_categorias,
)

# Módulo de exportación
from notebook.exportacion.exportacion import (
    exportar_usuarios_crudos,
    exportar_empresas_crudos,
    exportar_categorias_crudos,
)


def ejecutar_pipeline():
    print("=" * 70)
    print("    PROYECTO INTEGRADOR - PIPELINE DE DATOS CRUDOS")
    print("=" * 70)

    # -------------------------------------------------------------
    # 1. ENTIDAD: USUARIO
    # -------------------------------------------------------------
    print("\n[PASO 1] Procesando entidad: USUARIO")
    print(f" -> Generando {FILAS_USUARIOS} registros limpios...")
    df_usuarios_limpio = pd.DataFrame(generar_datos_usuarios(FILAS_USUARIOS))
    
    print(" -> Ensuciando datos de usuarios a propósito...")
    df_usuarios_crudo = ensuciar_usuarios(df_usuarios_limpio)
    
    print("\n--- Vista previa 'usuario_crudo' (primeros 3 registros) ---")
    print(df_usuarios_crudo.head(3))
    print(f"Total registros: {len(df_usuarios_crudo)} | Columnas: {list(df_usuarios_crudo.columns)}")
    
    print("\n -> Exportando usuarios a 'datos/crudos/' (CSV, JSON, XLSX)...")
    rutas_usuarios = exportar_usuarios_crudos(df_usuarios_crudo)
    for ruta in rutas_usuarios:
        if ruta:
            print(f"    * {ruta.name}")

    # -------------------------------------------------------------
    # 2. ENTIDAD: EMPRESA
    # -------------------------------------------------------------
    print("\n" + "-" * 70)
    print("[PASO 2] Procesando entidad: EMPRESA")
    print(f" -> Generando {FILAS_EMPRESAS} registros limpios...")
    df_empresas_limpio = pd.DataFrame(generar_datos_empresas(FILAS_EMPRESAS))
    
    print(" -> Ensuciando datos de empresas a propósito...")
    df_empresas_crudo = ensuciar_empresas(df_empresas_limpio)
    
    print("\n--- Vista previa 'empresa_crudo' (primeros 3 registros) ---")
    print(df_empresas_crudo.head(3))
    print(f"Total registros: {len(df_empresas_crudo)} | Columnas: {list(df_empresas_crudo.columns)}")
    
    print("\n -> Exportando empresas a 'datos/crudos/' (CSV, JSON, XLSX)...")
    rutas_empresas = exportar_empresas_crudos(df_empresas_crudo)
    for ruta in rutas_empresas:
        if ruta:
            print(f"    * {ruta.name}")

    # -------------------------------------------------------------
    # 3. ENTIDAD: CATEGORIA
    # -------------------------------------------------------------
    print("\n" + "-" * 70)
    print("[PASO 3] Procesando entidad: CATEGORIA")
    print(f" -> Generando {FILAS_CATEGORIAS} registros limpios...")
    df_cat_limpio = pd.DataFrame(generar_datos_categorias(FILAS_CATEGORIAS))

    print(" -> Ensuciando datos de categorías a propósito...")
    df_cat_crudo = ensuciar_categorias(df_cat_limpio)

    print("\n--- Vista previa 'categoria_crudo' (primeros 3 registros) ---")
    print(df_cat_crudo.head(3))
    print(f"Total registros: {len(df_cat_crudo)} | Columnas: {list(df_cat_crudo.columns)}")

    print("\n -> Exportando categorías a 'datos/crudos/' (CSV, JSON, XLSX)...")
    rutas_cat = exportar_categorias_crudos(df_cat_crudo)
    for ruta in rutas_cat:
        if ruta:
            print(f"    * {ruta.name}")

    print("\n" + "=" * 70)
    print("PIPELINE COMPLETADO CON ÉXITO")
    print("=" * 70)


if __name__ == "__main__":
    ejecutar_pipeline()
