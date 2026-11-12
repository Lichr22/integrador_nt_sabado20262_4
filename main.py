"""
Script Principal Orquestador del Proyecto Integrador.

Ejecuta el flujo de generación, ensuciado y exportación de datos crudos
para todas las entidades del modelo de datos:
- usuario
- empresa
- categoria
- prioridades
- retos
- registros

Opcionalmente, con el argumento --limpiar, ejecuta también la fase de limpieza
hacia 'datos/limpios/'.
"""

import argparse
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
from notebook.simulaciones.simulacion_prioridades import (
    FILAS as FILAS_PRIORIDADES,
    generar_datos as generar_datos_prioridades,
    ensuciar as ensuciar_prioridades,
)
from notebook.simulaciones.simulacion_retos import (
    FILAS as FILAS_RETOS,
    generar_datos as generar_datos_retos,
    ensuciar as ensuciar_retos,
)
from notebook.simulaciones.simulacion_registros import (
    FILAS as FILAS_REGISTROS,
    generar_datos as generar_datos_registros,
    ensuciar as ensuciar_registros,
)

# Módulo de exportación
from notebook.exportacion.exportacion import (
    exportar_usuarios_crudos,
    exportar_empresas_crudos,
    exportar_categorias_crudos,
    exportar_prioridades_crudos,
    exportar_retos_crudos,
    exportar_registros_crudos,
)

# Módulos de limpieza
from notebook.limpieza.simulacion_usuario import ejecutar_limpieza as limpiar_usuarios
from notebook.limpieza.simulacion_empresa import ejecutar_limpieza as limpiar_empresas
from notebook.limpieza.simulacion_categorias import ejecutar_limpieza as limpiar_categorias
from notebook.limpieza.simulacion_prioridades import ejecutar_limpieza as limpiar_prioridades
from notebook.limpieza.simulacion_retos import ejecutar_limpieza as limpiar_retos
from notebook.limpieza.simulacion_registros import ejecutar_limpieza as limpiar_registros


def ejecutar_pipeline():
    print("=" * 70)
    print("    PROYECTO INTEGRADOR - PIPELINE DE DATOS CRUDOS")
    print("=" * 70)

    entidades = [
        ("USUARIO", FILAS_USUARIOS, generar_datos_usuarios, ensuciar_usuarios, exportar_usuarios_crudos),
        ("EMPRESA", FILAS_EMPRESAS, generar_datos_empresas, ensuciar_empresas, exportar_empresas_crudos),
        ("CATEGORIA", FILAS_CATEGORIAS, generar_datos_categorias, ensuciar_categorias, exportar_categorias_crudos),
        ("PRIORIDADES", FILAS_PRIORIDADES, generar_datos_prioridades, ensuciar_prioridades, exportar_prioridades_crudos),
        ("RETOS", FILAS_RETOS, generar_datos_retos, ensuciar_retos, exportar_retos_crudos),
        ("REGISTROS", FILAS_REGISTROS, generar_datos_registros, ensuciar_registros, exportar_registros_crudos),
    ]

    for i, (nombre, cant_filas, func_generar, func_ensuciar, func_exportar) in enumerate(entidades, start=1):
        print(f"\n[PASO {i}/{len(entidades)}] Procesando entidad: {nombre}")
        print(f" -> Generando {cant_filas} registros limpios...")
        df_limpio = pd.DataFrame(func_generar(cant_filas))

        print(f" -> Ensuciando datos de {nombre.lower()} a propósito...")
        df_crudo = func_ensuciar(df_limpio)

        print(f"\n--- Vista previa '{nombre.lower()}_crudo' (primeros 3 registros) ---")
        print(df_crudo.head(3))
        print(f"Total registros: {len(df_crudo)} | Columnas: {list(df_crudo.columns)}")

        print(f"\n -> Exportando a 'datos/crudos/' (CSV, JSON, XLSX)...")
        rutas = func_exportar(df_crudo)
        for r in rutas:
            if r:
                print(f"    * {r.name}")
        print("-" * 70)

    print("\n" + "=" * 70)
    print("PIPELINE DE DATOS CRUDOS FINALIZADO CON ÉXITO")
    print("=" * 70)


def ejecutar_limpieza_completa():
    print("\n" + "=" * 70)
    print("    PROYECTO INTEGRADOR - PIPELINE DE LIMPIEZA (DATOS LIMPIOS)")
    print("=" * 70)

    limpiezas = [
        ("USUARIO", limpiar_usuarios),
        ("EMPRESA", limpiar_empresas),
        ("CATEGORIA", limpiar_categorias),
        ("PRIORIDADES", limpiar_prioridades),
        ("RETOS", limpiar_retos),
        ("REGISTROS", limpiar_registros),
    ]

    for nombre, func_limpiar in limpiezas:
        print(f"\n>>> Limpiando entidad: {nombre}...")
        func_limpiar()

    print("\n" + "=" * 70)
    print("PIPELINE DE LIMPIEZA COMPLETO FINALIZADO CON ÉXITO")
    print("=" * 70)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline ETL de Simulación y Limpieza.")
    parser.add_argument(
        "--limpiar",
        action="store_true",
        help="Ejecuta también la fase de limpieza sobre los datos generados.",
    )
    args = parser.parse_args()

    ejecutar_pipeline()

    if args.limpiar:
        ejecutar_limpieza_completa()
