"""
Módulo de Visualización y Generación de Reportes: Registros (Participaciones).

Script: src/reporte_registros.py
Lee el archivo limpio 'datos/limpios/registros_limpio.csv', genera 3 gráficas analíticas
utilizando matplotlib a partir de las consultas previas y las guarda en formato PNG
dentro de 'reportes/'. Finaliza imprimiendo por consola las conclusiones sobre demanda,
estacionalidad y la necesidad de control de duplicados con HTTP 409 en el backend.
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
CARPETA_DATOS = CARPETA_PROYECTO / "datos" / "limpios"
CARPETA_REPORTES = CARPETA_PROYECTO / "reportes"

# Asegurar la creación automática de la carpeta reportes
os.makedirs("reportes", exist_ok=True)
CARPETA_REPORTES.mkdir(parents=True, exist_ok=True)


def obtener_ruta_limpia() -> Path:
    """Retorna la ruta del archivo limpio generado por la fase de limpieza."""
    ruta = CARPETA_DATOS / "registros_limpio.csv"
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró {ruta}. Ejecuta primero: python main.py --limpiar")
    return ruta


def cargar_datos() -> pd.DataFrame:
    """Carga y prepara el DataFrame limpio de registros."""
    ruta = obtener_ruta_limpia()
    try:
        df = pd.read_csv(ruta, sep=None, engine="python", encoding="utf-8-sig")
    except Exception:
        df = pd.read_csv(ruta, sep=";", encoding="utf-8-sig")

    if "estado" in df.columns:
        df["estado"] = (
            df["estado"]
            .astype(str)
            .str.strip()
            .str.upper()
            .str.replace(" ", "_")
        )

    if "mes" not in df.columns and "fecha_registro" in df.columns:
        fechas_dt = pd.to_datetime(df["fecha_registro"], errors="coerce")
        df["mes"] = fechas_dt.dt.strftime("%Y-%m")

    return df


# =============================================================================
# GRÁFICA 1: Barras - Participaciones por Estado
# =============================================================================
def generar_grafica_1_barras_estado(conteo: pd.Series) -> str:
    """Genera gráfica de barras mostrando la distribución de participaciones por estado."""
    ruta_guardado = CARPETA_REPORTES / "registros_grafica_1.png"

    plt.figure(figsize=(9, 5))
    conteo.plot(kind="bar", color="#2980b9", edgecolor="black")

    plt.title("Cantidad de Participaciones por Estado", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Estado de la Participación", fontsize=11, fontweight="bold")
    plt.ylabel("Cantidad de Participaciones", fontsize=11, fontweight="bold")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.savefig(ruta_guardado, dpi=120)
    plt.close()

    print(f"[OK] Gráfica 1 guardada en: {ruta_guardado}")
    return str(ruta_guardado)


# =============================================================================
# GRÁFICA 2: Línea - Participaciones por Mes
# =============================================================================
def generar_grafica_2_linea_por_mes(por_mes: pd.Series) -> str:
    """Genera gráfica de línea con marcadores circulares mostrando inscripciones por mes."""
    ruta_guardado = CARPETA_REPORTES / "registros_grafica_2.png"

    plt.figure(figsize=(10, 5))
    por_mes.plot(kind="line", marker="o", color="#27ae60", linewidth=2, markersize=6)

    plt.title("Evolución Mensual de Inscripciones", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Mes de Registro (Año-Mes)", fontsize=11, fontweight="bold")
    plt.ylabel("Cantidad de Participaciones", fontsize=11, fontweight="bold")
    plt.xticks(rotation=45, ha="right")
    plt.grid(True, linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.savefig(ruta_guardado, dpi=120)
    plt.close()

    print(f"[OK] Gráfica 2 guardada en: {ruta_guardado}")
    return str(ruta_guardado)


# =============================================================================
# GRÁFICA 3: Barras Horizontales - Los 10 Retos con Más Participantes
# =============================================================================
def generar_grafica_3_barras_horizontales_top_retos(top_retos: pd.Series) -> str:
    """Genera gráfica de barras horizontales mostrando los 10 retos más demandados."""
    ruta_guardado = CARPETA_REPORTES / "registros_grafica_3.png"

    plt.figure(figsize=(9, 6))
    top_retos.plot(kind="barh", color="#e67e22", edgecolor="black")

    plt.title("Los 10 Retos con Más Participantes", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Cantidad de Participantes Inscritos", fontsize=11, fontweight="bold")
    plt.ylabel("ID del Reto", fontsize=11, fontweight="bold")
    plt.grid(axis="x", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.savefig(ruta_guardado, dpi=120)
    plt.close()

    print(f"[OK] Gráfica 3 guardada en: {ruta_guardado}")
    return str(ruta_guardado)


# =============================================================================
# CONCLUSIONES DEL NEGOCIO Y CALIDAD DE DATOS
# =============================================================================
def imprimir_conclusiones(df: pd.DataFrame, top_retos: pd.Series, por_mes: pd.Series) -> None:
    """Imprime por consola las conclusiones analíticas y recomendaciones para el backend."""
    reto_lider = top_retos.index[0]
    cant_reto_lider = top_retos.iloc[0]

    mes_lider = str(por_mes.idxmax())
    cant_mes_lider = por_mes.max()

    # Detección de duplicados por combinación (id_usuario, id_reto)
    filas_repetidas_total = df.duplicated(subset=["id_usuario", "id_reto"], keep=False).sum()
    duplicados_redundantes = df.duplicated(subset=["id_usuario", "id_reto"], keep="first").sum()

    print("\n" + "=" * 75)
    print("                      CONCLUSIONES DEL ANÁLISIS")
    print("=" * 75)

    print(f"""
1. CUÁL ES EL RETO MÁS POPULAR Y CUÁNTOS PARTICIPANTES TIENE:
   - El reto más popular de la plataforma es '{reto_lider}' con un total 
     de {cant_reto_lider} participantes registrados.
   - Los retos líderes concentran un volumen significativo de la demanda estudiantil y profesional, 
     lo que sugiere que temáticas atractivas o con mayores incentivos movilizan rápidamente 
     a la comunidad de proponentes.

2. EN QUÉ MES HUBO MÁS INSCRIPCIONES:
   - El período con mayor actividad de inscripción fue '{mes_lider}' registrando {cant_mes_lider} 
     participaciones.
   - Los picos de inscripción suelen coincidir con el inicio de los semestres académicos, cuando
     instituciones y estudiantes buscan proyectos integradores, prácticas y desafíos abiertos
     para complementar su formación curricular.

3. CUÁNTAS INSCRIPCIONES DUPLICADAS SE ENCONTRARON Y POR QUÉ EL BACKEND DEBE BLOQUEARLAS CON 409:
   - En el análisis se detectaron {filas_repetidas_total} registros involucrados en duplicidades de 
     usuario y reto (con {duplicados_redundantes} inscripciones redundantes sobre las combinaciones únicas).
   - ¿Por qué el Backend debe responder con código HTTP 409 (Conflict)?
     a) Regla de negocio inmutable: Un usuario sólo puede inscribirse UNA VEZ a un mismo reto.
     b) Si el backend permite postulaciones múltiples del mismo usuario:
        * Se distorsionan gravemente los cupos máximos y las métricas de participación real.
        * Provoca conflictos en la asignación de jurados y doble calificación de entregas.
        * Puede generar inconsistencias de estado (el usuario podría aparecer simultáneamente 
          'ACTIVO' y 'FINALIZADO' en el mismo reto).
     c) Arquitectura preventiva: La base de datos debe declarar un índice único compuesto:
        `CONSTRAINT uq_usuario_reto UNIQUE (id_usuario, id_reto)`
        y el endpoint de inscripción (POST `/api/registros`) debe atrapar la violación de unicidad 
        y retornar limpiamente un código `HTTP 409 Conflict` con un mensaje explicativo al cliente.
""")
    print("=" * 75)


# =============================================================================
# EJECUCIÓN PRINCIPAL
# =============================================================================
def main():
    print("#" * 75)
    print("   GENERANDO REPORTE GRÁFICO DE REGISTROS (src/reporte_registros.py)")
    print("#" * 75)

    df = cargar_datos()
    print(f"[INFO] Datos limpios cargados: {len(df)} registros.")

    # 1. Preparar consultas base
    conteo = df["estado"].value_counts()
    por_mes = df.groupby("mes")["id"].count()
    top_retos = df.groupby("id_reto")["id"].count().nlargest(10)

    # 2. Generar las tres gráficas
    print("\nGenerando visualizaciones...")
    generar_grafica_1_barras_estado(conteo)
    generar_grafica_2_linea_por_mes(por_mes)
    generar_grafica_3_barras_horizontales_top_retos(top_retos)

    # 3. Imprimir conclusiones
    imprimir_conclusiones(df, top_retos, por_mes)


if __name__ == "__main__":
    main()

