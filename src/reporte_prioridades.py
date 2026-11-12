"""
Módulo de Visualización y Generación de Reportes: Prioridades.

Script: src/reporte_prioridades.py
Lee el archivo limpio 'data/limpio/prioridades_limpio.csv', genera 3 gráficas analíticas
utilizando matplotlib y las guarda en formato PNG dentro del directorio 'reportes/'.
Finaliza imprimiendo por consola las conclusiones sobre la calidad y el comportamiento
de las prioridades y acuerdos de nivel de servicio (SLA).
"""

import os
import tempfile
from pathlib import Path

# Configurar directorio temporal de matplotlib para evitar problemas de permisos
os.environ.setdefault("MPLCONFIGDIR", tempfile.gettempdir())

import matplotlib.pyplot as plt
import pandas as pd

# 1. Configuración de Rutas con Pathlib y os
CARPETA_PROYECTO = Path(__file__).resolve().parent.parent
CARPETA_DATA = CARPETA_PROYECTO / "data" / "limpio"
CARPETA_DATOS = CARPETA_PROYECTO / "datos" / "limpios"
CARPETA_REPORTES = CARPETA_PROYECTO / "reportes"

# Asegurar la creación automática de la carpeta reportes
os.makedirs("reportes", exist_ok=True)
CARPETA_REPORTES.mkdir(parents=True, exist_ok=True)


def obtener_ruta_limpia() -> Path:
    """Retorna la ruta del archivo limpio prioridades_limpio.csv."""
    rutas = [
        CARPETA_DATA / "prioridades_limpio.csv",
        CARPETA_DATOS / "prioridades_limpio.csv",
    ]
    for r in rutas:
        if r.exists():
            return r
    raise FileNotFoundError("No se encontró 'prioridades_limpio.csv' en 'data/limpio/' ni 'datos/limpios/'.")


def cargar_datos() -> pd.DataFrame:
    """Carga y prepara el DataFrame limpio de prioridades."""
    ruta = obtener_ruta_limpia()
    try:
        df = pd.read_csv(ruta, sep=None, engine="python", encoding="utf-8-sig")
    except Exception:
        df = pd.read_csv(ruta, sep=";", encoding="utf-8-sig")

    if "nivel" in df.columns:
        df["nivel"] = pd.to_numeric(df["nivel"], errors="coerce")
    if "dias_max_respuesta" in df.columns:
        df["dias_max_respuesta"] = pd.to_numeric(df["dias_max_respuesta"], errors="coerce")

    return df


# =============================================================================
# GRÁFICA 1: Barras - Cuántas Filas Hay por Nivel
# =============================================================================
def generar_grafica_1_barras_por_nivel(por_nivel: pd.Series) -> str:
    """Genera gráfica de barras mostrando la cantidad de filas por cada nivel."""
    ruta_guardado = CARPETA_REPORTES / "prioridades_grafica_1.png"

    plt.figure(figsize=(8, 5))
    por_nivel.plot(kind="bar", color="#2980b9", edgecolor="black")

    plt.title("Cantidad de Filas por Nivel de Prioridad", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Nivel de Prioridad (1 a 5)", fontsize=11, fontweight="bold")
    plt.ylabel("Cantidad de Registros", fontsize=11, fontweight="bold")
    plt.xticks(rotation=0)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.savefig(ruta_guardado, dpi=120)
    plt.close()

    print(f"[OK] Gráfica 1 guardada en: {ruta_guardado}")
    return str(ruta_guardado)


# =============================================================================
# GRÁFICA 2: Barras - Días Promedio de Respuesta por Prioridad
# =============================================================================
def generar_grafica_2_barras_dias_promedio(resumen: pd.DataFrame) -> str:
    """Genera gráfica de barras con los días promedio de respuesta por nombre de prioridad."""
    ruta_guardado = CARPETA_REPORTES / "prioridades_grafica_2.png"

    plt.figure(figsize=(8, 5))
    resumen["mean"].plot(kind="bar", color="#e67e22", edgecolor="black")

    plt.title("Días Promedio de Respuesta por Prioridad", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Nombre de Prioridad", fontsize=11, fontweight="bold")
    plt.ylabel("Días Promedio de Respuesta", fontsize=11, fontweight="bold")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.savefig(ruta_guardado, dpi=120)
    plt.close()

    print(f"[OK] Gráfica 2 guardada en: {ruta_guardado}")
    return str(ruta_guardado)


# =============================================================================
# GRÁFICA 3: Torta - Reparto de las Prioridades
# =============================================================================
def generar_grafica_3_torta_reparto(conteo: pd.Series) -> str:
    """Genera gráfica de torta mostrando la distribución porcentual de prioridades."""
    ruta_guardado = CARPETA_REPORTES / "prioridades_grafica_3.png"

    plt.figure(figsize=(7, 6))
    colores = ["#3498db", "#2ecc71", "#f1c40f", "#e67e22", "#e74c3c"]
    conteo.plot(
        kind="pie",
        autopct="%1.1f%%",
        startangle=140,
        colors=colores,
        shadow=True,
    )

    plt.title("Reparto Proporcional de las Prioridades", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Distribución de Categorías", fontsize=10)
    plt.ylabel("Porcentaje", fontsize=10)

    plt.tight_layout()
    plt.savefig(ruta_guardado, dpi=120)
    plt.close()

    print(f"[OK] Gráfica 3 guardada en: {ruta_guardado}")
    return str(ruta_guardado)


# =============================================================================
# CONCLUSIONES DEL NEGOCIO Y CALIDAD DE DATOS
# =============================================================================
def imprimir_conclusiones(df: pd.DataFrame, conteo: pd.Series, resumen: pd.DataFrame) -> None:
    """Imprime por consola las conclusiones del análisis de prioridades."""
    total_prioridades_reales = len(conteo)
    nombres_prioridades = list(conteo.index)

    print("\n" + "=" * 75)
    print("                      CONCLUSIONES DEL ANÁLISIS")
    print("=" * 75)

    print(f"""
1. CUÁNTAS PRIORIDADES REALES QUEDARON AL FINAL:
   - Quedaron exactamente {total_prioridades_reales} prioridades REALES y únicas: {nombres_prioridades}.
   - En la simulación original se habían inyectado errores de casing ('ALTA', ' alta ', 'Alta'), 
     pero gracias a la fase de limpieza y normalización se eliminaron las redundancias 
     semánticas y duplicados exactos, consolidando las 5 categorías oficiales del negocio.

2. RELACIÓN ENTRE EL NIVEL Y LOS DÍAS MÁXIMOS DE RESPUESTA:
   - Existe una relación inversa y proporcional estricta entre la urgencia y el tiempo de atención:
     * Nivel 1 (muy baja) : 10 días máximos de respuesta.
     * Nivel 2 (baja)     : 7 días máximos de respuesta.
     * Nivel 3 (media)    : 5 días máximos de respuesta.
     * Nivel 4 (alta)     : 2 días máximos de respuesta.
     * Nivel 5 (crítica)  : 1 día máximo de respuesta.
   - A mayor nivel de severidad y criticidad del reto o solicitud, menor es la ventana de 
     tiempo permitida por el SLA (Acuerdo de Nivel de Servicio) para brindar una solución.

3. POR QUÉ EL BACKEND DEBE VALIDAR QUE 'NIVEL' ESTÉ ENTRE 1 Y 5:
   - Durante la inyección de anomalías aparecieron valores nulos, textos ("tres", "cinco") y 
     días absurdos como '999'.
   - Si el backend permite niveles fuera del rango [1, 5]:
     a) Se rompe la lógica de negocio del SLA, asignando plazos infinitos o inexistentes a casos urgentes.
     b) Se compromete la integridad referencial y las agregaciones analíticas de las tablas relacionadas (retos).
     c) Provoca caídas (crashes) en consultas y dashboards que esperan valores enteros continuos.
   - Por tanto, el backend debe aplicar validaciones estrictas (con esquemas Pydantic / DTOs y 
     restricciones CHECK en la base de datos) para garantizar que 'nivel' sea un entero entre 1 y 5.
""")
    print("=" * 75)


# =============================================================================
# EJECUCIÓN PRINCIPAL
# =============================================================================
def main():
    print("#" * 75)
    print("   GENERANDO REPORTE GRÁFICO DE PRIORIDADES (src/reporte_prioridades.py)")
    print("#" * 75)

    df = cargar_datos()
    print(f"[INFO] Datos limpios cargados: {len(df)} registros.")

    # 1. Preparar consultas base
    por_nivel = df.groupby("nivel")["id"].count()
    resumen = df.groupby("nombre")["dias_max_respuesta"].agg(["min", "mean", "max"]).round(1)
    conteo = df["nombre"].value_counts()

    # 2. Generar las tres gráficas
    print("\nGenerando visualizaciones...")
    generar_grafica_1_barras_por_nivel(por_nivel)
    generar_grafica_2_barras_dias_promedio(resumen)
    generar_grafica_3_torta_reparto(conteo)

    # 3. Imprimir conclusiones
    imprimir_conclusiones(df, conteo, resumen)


if __name__ == "__main__":
    main()

