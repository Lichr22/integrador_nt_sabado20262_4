"""
Módulo de Visualización y Generación de Reportes: Categorías.

Script: src/reporte_categorias.py
Lee el archivo limpio 'datos/limpios/categoria_limpio.csv', genera 3 gráficas analíticas
con matplotlib a partir de las consultas previas y las guarda en formato PNG en 'reportes/'.
Finaliza imprimiendo en consola las conclusiones de calidad de datos, catálogo de entidades
y justificación técnica para unicidad de nombres en el backend.
"""

import os
import tempfile
from pathlib import Path

# Configurar directorio temporal de matplotlib para evitar advertencias de permisos
os.environ.setdefault("MPLCONFIGDIR", tempfile.gettempdir())

import matplotlib.pyplot as plt
import pandas as pd

# 1. Configuración de Rutas con Pathlib y os
CARPETA_PROYECTO = Path(__file__).resolve().parent.parent
CARPETA_DATOS = CARPETA_PROYECTO / "datos" / "limpios"
CARPETA_CRUDOS = CARPETA_PROYECTO / "datos" / "crudos"
CARPETA_REPORTES = CARPETA_PROYECTO / "reportes"

# Asegurar la creación automática de la carpeta reportes
os.makedirs("reportes", exist_ok=True)
CARPETA_REPORTES.mkdir(parents=True, exist_ok=True)


def obtener_ruta_limpia() -> Path:
    """Retorna la ruta del archivo limpio generado por la fase de limpieza."""
    ruta = CARPETA_DATOS / "categoria_limpio.csv"
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró {ruta}. Ejecuta primero: python main.py --limpiar")
    return ruta


def cargar_datos() -> pd.DataFrame:
    """Carga y prepara el DataFrame limpio de categorias."""
    ruta = obtener_ruta_limpia()
    try:
        df = pd.read_csv(ruta, sep=None, engine="python", encoding="utf-8-sig")
    except Exception:
        df = pd.read_csv(ruta, sep=";", encoding="utf-8-sig")

    if "descripcion" in df.columns:
        df["descripcion"] = df["descripcion"].fillna("Sin descripcion").astype(str).str.strip()

    if "largo_desc" in df.columns:
        df["largo_desc"] = pd.to_numeric(df["largo_desc"], errors="coerce")
    elif "descripcion" in df.columns:
        df["largo_desc"] = df["descripcion"].str.len()

    return df


# =============================================================================
# GRÁFICA 1: Barras Horizontales - Cuántas Veces Aparece Cada Categoría
# =============================================================================
def generar_grafica_1_barras_horizontales(conteo: pd.Series) -> str:
    """Genera gráfica de barras horizontales mostrando la frecuencia de cada categoría."""
    ruta_guardado = CARPETA_REPORTES / "categorias_grafica_1.png"

    plt.figure(figsize=(9, 6))
    conteo.sort_values(ascending=True).plot(kind="barh", color="#3498db", edgecolor="black")

    plt.title("Frecuencia de Registros por Categoría", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Cantidad de Registros", fontsize=11, fontweight="bold")
    plt.ylabel("Nombre de la Categoría", fontsize=11, fontweight="bold")
    plt.grid(axis="x", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.savefig(ruta_guardado, dpi=120)
    plt.close()

    print(f"[OK] Gráfica 1 guardada en: {ruta_guardado}")
    return str(ruta_guardado)


# =============================================================================
# GRÁFICA 2: Torta - Reparto de Categorías por Área Responsable
# =============================================================================
def generar_grafica_2_torta_area(por_area: pd.Series) -> str:
    """Genera gráfica de torta con la distribución porcentual por área responsable."""
    ruta_guardado = CARPETA_REPORTES / "categorias_grafica_2.png"

    plt.figure(figsize=(8, 7))
    colores = ["#e74c3c", "#2ecc71", "#3498db", "#9b59b6", "#f1c40f", "#1abc9c", "#e67e22"]
    por_area.plot(
        kind="pie",
        autopct="%1.1f%%",
        startangle=140,
        colors=colores,
        shadow=True,
    )

    plt.title("Reparto de Categorías por Área Responsable", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Distribución por Área Responsable", fontsize=10)
    plt.ylabel("Porcentaje", fontsize=10)

    plt.tight_layout()
    plt.savefig(ruta_guardado, dpi=120)
    plt.close()

    print(f"[OK] Gráfica 2 guardada en: {ruta_guardado}")
    return str(ruta_guardado)


# =============================================================================
# GRÁFICA 3: Barras - Largo Promedio de la Descripción por Categoría
# =============================================================================
def generar_grafica_3_barras_largo_promedio(largos: pd.Series) -> str:
    """Genera gráfica de barras verticales con el largo promedio de la descripción."""
    ruta_guardado = CARPETA_REPORTES / "categorias_grafica_3.png"

    plt.figure(figsize=(9, 5))
    largos.plot(kind="bar", color="#9b59b6", edgecolor="black")

    plt.title("Largo Promedio de la Descripción por Categoría", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Categoría", fontsize=11, fontweight="bold")
    plt.ylabel("Largo Promedio (Caracteres)", fontsize=11, fontweight="bold")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.savefig(ruta_guardado, dpi=120)
    plt.close()

    print(f"[OK] Gráfica 3 guardada en: {ruta_guardado}")
    return str(ruta_guardado)


# =============================================================================
# CONCLUSIONES DEL NEGOCIO Y CALIDAD DE DATOS
# =============================================================================
def imprimir_conclusiones(df_limpio: pd.DataFrame, conteo: pd.Series) -> None:
    """Imprime en consola las conclusiones analíticas y técnicas sobre categorías."""
    filas_limpias = len(df_limpio)
    total_categorias_reales = len(conteo)

    # Comparar con el dataset crudo para medir lo que corrigió la limpieza
    ruta_crudo = CARPETA_CRUDOS / "categoria_crudo.csv"
    if ruta_crudo.exists():
        df_crudo = pd.read_csv(ruta_crudo, sep=";", encoding="utf-8-sig")
        filas_crudo = len(df_crudo)
        filas_eliminadas = filas_crudo - filas_limpias
        crudo_unico = df_crudo.drop_duplicates(subset=["id"])
        comparacion = crudo_unico[["id", "nombre"]].merge(
            df_limpio[["id", "nombre"]], on="id", suffixes=("_crudo", "_limpio")
        )
        nombres_corregidos = int((comparacion["nombre_crudo"] != comparacion["nombre_limpio"]).sum())
        descripciones_nulas = int(crudo_unico["descripcion"].isna().sum())
        texto_filas = (
            f"Se eliminaron {filas_eliminadas} filas duplicadas (reducción de {filas_crudo}\n"
            f"     registros crudos a {filas_limpias} registros limpios y consistentes)."
        )
        texto_correcciones = (
            f"Adicionalmente, se corrigieron {nombres_corregidos} anomalías de escritura en 'nombre' (mezclas de\n"
            f"     mayúsculas, minúsculas y espacios sobrantes) y se estandarizaron {descripciones_nulas}\n"
            f"     descripciones nulas bajo el rótulo unificado 'Sin descripcion'."
        )
    else:
        texto_filas = f"No se encontró {ruta_crudo.name}; no fue posible medir las filas eliminadas."
        texto_correcciones = f"Quedaron {filas_limpias} registros limpios."

    print("\n" + "=" * 75)
    print("                      CONCLUSIONES DEL ANÁLISIS")
    print("=" * 75)

    print(f"""
1. CUÁNTAS FILAS SE ELIMINARON AL QUITAR DUPLICADOS Y VARIANTES DE ESCRITURA:
   - {texto_filas}
   - {texto_correcciones}

2. CUÁNTAS CATEGORÍAS REALES QUEDARON AL FINAL (CATÁLOGO OFICIAL):
   - Al finalizar la consolidación quedaron {total_categorias_reales} categorías REALES y canónicas:
     {list(conteo.index)}.
   - Todas las variantes tipográficas fueron unificadas hacia los términos rectores del negocio, 
     garantizando que ninguna entidad hija (retos) sufra dispersión ni falsas subdivisiones.

3. POR QUÉ EL BACKEND DEBE DECLARAR 'nombre' COMO ÚNICO PARA QUE ESTO NO VUELVA A PASAR:
   - Las categorías constituyen tablas maestras (lookup tables) que parametrizan la lógica 
     temática del sistema.
   - Si el backend no exige unicidad (`unique=True` / `CONSTRAINT uq_categoria_nombre UNIQUE`):
     a) Múltiples usuarios o administradores registrarán sinónimos o duplicados semánticos 
        (ej: 'Inteligencia Artificial', 'inteligencia artificial', 'IA'), fragmentando el catálogo.
     b) Se destruye la confiabilidad de las consultas agregadas por área y sector, arruinando 
        los filtros de búsqueda en el front y las recomendaciones algorítmicas de retos.
     c) Restringir el campo como ÚNICO en la base de datos junto a validaciones previas de 
        normalización de cadenas (trim y lowercase/titlecase) asegura la pureza e integridad 
        estructural del modelo relacional.
""")
    print("=" * 75)


# =============================================================================
# EJECUCIÓN PRINCIPAL
# =============================================================================
def main():
    print("#" * 75)
    print("   GENERANDO REPORTE GRÁFICO DE CATEGORÍAS (src/reporte_categorias.py)")
    print("#" * 75)

    df = cargar_datos()
    print(f"[INFO] Datos limpios cargados: {len(df)} registros.")

    # 1. Preparar consultas base
    conteo = df["nombre"].value_counts()
    por_area = df.groupby("area_responsable")["id"].count().sort_values(ascending=False)
    largos = df.groupby("nombre")["largo_desc"].mean().round(1).sort_values(ascending=False)

    # 2. Generar las tres gráficas
    print("\nGenerando visualizaciones...")
    generar_grafica_1_barras_horizontales(conteo)
    generar_grafica_2_torta_area(por_area)
    generar_grafica_3_barras_largo_promedio(largos)

    # 3. Imprimir conclusiones
    imprimir_conclusiones(df, conteo)


if __name__ == "__main__":
    main()

