"""
Módulo de Visualización y Generación de Reportes: Retos.

Script: src/reporte_retos.py
Lee el archivo limpio 'datos/limpios/retos_limpio.csv', genera 3 gráficas analíticas
utilizando matplotlib a partir de las consultas previas y las guarda en formato PNG
dentro de 'reportes/'. Finaliza imprimiendo en consola las conclusiones analíticas
sobre la estacionalidad, duración y reglas de validación temporal en el backend.
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
    ruta = CARPETA_DATOS / "retos_limpio.csv"
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró {ruta}. Ejecuta primero: python main.py --limpiar")
    return ruta


def cargar_datos() -> pd.DataFrame:
    """Carga y prepara el DataFrame limpio de retos."""
    ruta = obtener_ruta_limpia()
    try:
        df = pd.read_csv(ruta, sep=None, engine="python", encoding="utf-8-sig")
    except Exception:
        df = pd.read_csv(ruta, sep=";", encoding="utf-8-sig")

    if "fecha_inicio" in df.columns:
        df["fecha_inicio"] = pd.to_datetime(df["fecha_inicio"], errors="coerce")
    if "fecha_fin" in df.columns:
        df["fecha_fin"] = pd.to_datetime(df["fecha_fin"], errors="coerce")

    if "duracion_dias" in df.columns:
        df["duracion_dias"] = pd.to_numeric(df["duracion_dias"], errors="coerce")
    elif "fecha_inicio" in df.columns and "fecha_fin" in df.columns:
        df["duracion_dias"] = (df["fecha_fin"] - df["fecha_inicio"]).dt.days

    if "estado" in df.columns:
        df["estado"] = (
            df["estado"]
            .astype(str)
            .str.strip()
            .str.upper()
            .str.replace(" ", "_")
        )

    return df


# =============================================================================
# GRÁFICA 1: Barras - Cantidad de Retos por Estado
# =============================================================================
def generar_grafica_1_barras_estado(conteo: pd.Series) -> str:
    """Genera gráfica de barras mostrando la cantidad de retos por cada estado."""
    ruta_guardado = CARPETA_REPORTES / "retos_grafica_1.png"

    plt.figure(figsize=(9, 5))
    conteo.plot(kind="bar", color="#2980b9", edgecolor="black")

    plt.title("Cantidad de Retos por Estado Operativo", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Estado del Reto", fontsize=11, fontweight="bold")
    plt.ylabel("Cantidad de Retos", fontsize=11, fontweight="bold")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.savefig(ruta_guardado, dpi=120)
    plt.close()

    print(f"[OK] Gráfica 1 guardada en: {ruta_guardado}")
    return str(ruta_guardado)


# =============================================================================
# GRÁFICA 2: Línea - Retos que Empiezan Cada Mes
# =============================================================================
def generar_grafica_2_linea_por_mes(por_mes: pd.Series) -> str:
    """Genera gráfica de línea con marcadores circulares mostrando retos por mes."""
    ruta_guardado = CARPETA_REPORTES / "retos_grafica_2.png"

    plt.figure(figsize=(10, 5))
    por_mes.plot(kind="line", marker="o", color="#27ae60", linewidth=2, markersize=6)

    plt.title("Tendencia Mensual: Retos Iniciados por Mes", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Período Mensual (Año-Mes)", fontsize=11, fontweight="bold")
    plt.ylabel("Cantidad de Retos Iniciados", fontsize=11, fontweight="bold")
    plt.xticks(rotation=45, ha="right")
    plt.grid(True, linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.savefig(ruta_guardado, dpi=120)
    plt.close()

    print(f"[OK] Gráfica 2 guardada en: {ruta_guardado}")
    return str(ruta_guardado)


# =============================================================================
# GRÁFICA 3: Histograma - Cómo se Reparte la Duración de los Retos
# =============================================================================
def generar_grafica_3_histograma_duracion(df: pd.DataFrame) -> str:
    """Genera histograma con 20 bins mostrando la distribución de duración en días."""
    ruta_guardado = CARPETA_REPORTES / "retos_grafica_3.png"

    plt.figure(figsize=(9, 5))
    df["duracion_dias"].plot(kind="hist", bins=20, color="#e67e22", edgecolor="black")

    plt.title("Distribución de la Duración de los Retos en Días", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Duración del Reto (Días)", fontsize=11, fontweight="bold")
    plt.ylabel("Frecuencia (Cantidad de Retos)", fontsize=11, fontweight="bold")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.savefig(ruta_guardado, dpi=120)
    plt.close()

    print(f"[OK] Gráfica 3 guardada en: {ruta_guardado}")
    return str(ruta_guardado)


# =============================================================================
# CONCLUSIONES DEL NEGOCIO Y CALIDAD DE DATOS
# =============================================================================
def imprimir_conclusiones(df: pd.DataFrame, conteo: pd.Series, por_mes: pd.Series) -> None:
    """Imprime por consola las conclusiones derivadas de las consultas y visualizaciones."""
    top_meses = por_mes.sort_values(ascending=False)
    mes_lider = str(top_meses.index[0])
    max_retos_mes = top_meses.iloc[0]
    siguientes_meses = " y ".join(f"'{m}' ({c})" for m, c in top_meses.iloc[1:3].items())

    # Duración promedio por estado
    resumen_duracion = df.groupby("estado")["duracion_dias"].mean().round(1)
    mas_largos = resumen_duracion.sort_values(ascending=False).head(2)
    texto_mas_largos = " y ".join(f"'{e}' ({d:.1f} días)" for e, d in mas_largos.items())
    if "CERRADO" in resumen_duracion.index:
        dias_cerrado = resumen_duracion["CERRADO"]
        texto_cerrado = (
            f"Los retos con estado 'CERRADO' promedian {dias_cerrado:.1f} días "
            f"(~{dias_cerrado / 30:.1f} meses) de ciclo de resolución."
        )
    else:
        texto_cerrado = "No hay retos con estado 'CERRADO' en los datos limpios."

    # Fechas invertidas y nulas medidas directamente en el dataset crudo
    ruta_crudo = CARPETA_CRUDOS / "retos_crudo.csv"
    if ruta_crudo.exists():
        crudo = pd.read_csv(ruta_crudo, sep=";", encoding="utf-8-sig").drop_duplicates(subset=["id"])
        ini = pd.to_datetime(crudo["fecha_inicio"], format="mixed", dayfirst=True, errors="coerce")
        fin = pd.to_datetime(crudo["fecha_fin"], format="mixed", dayfirst=True, errors="coerce")
        invertidas = int((fin <= ini).sum())
        fin_nulas = int(fin.isna().sum())
        texto_invertidas = (
            f"En el dataset crudo se detectaron {invertidas} retos (de {len(crudo)}) donde la fecha de\n"
            f"     finalización era anterior o igual a la fecha de inicio (más {fin_nulas} retos con fecha de fin nula)."
        )
    else:
        texto_invertidas = f"No se encontró {ruta_crudo.name}; no fue posible medir las fechas invertidas."

    print("\n" + "=" * 75)
    print("                      CONCLUSIONES DEL ANÁLISIS")
    print("=" * 75)

    print(f"""
1. EN QUÉ MES SE CONCENTRAN LOS RETOS Y POR QUÉ PUEDE SER:
   - El pico más alto de aperturas de retos se concentra en el mes '{mes_lider}' con un 
     total de {max_retos_mes} retos iniciados, seguido por {siguientes_meses}.
   - Posible explicación de negocio:
     Los picos de apertura suelen coincidir con cierres de trimestre fiscal en las empresas
     aliadas y con las convocatorias semestrales de universidades y centros de formación,
     lo que genera olas sincronizadas de publicación de necesidades en la plataforma.

2. CUÁNTO DURA EN PROMEDIO UN RETO SEGÚN SU ESTADO:
   - La duración promedio general en días según cada estado operativo es:
{chr(10).join([f"     * {est:<15}: {dias:>5.1f} días" for est, dias in resumen_duracion.items()])}
   - Observación:
     {texto_cerrado}
     Los promedios más altos los registran {texto_mas_largos}, lo que puede
     indicar cuellos de botella administrativos o dependencias no resueltas.

3. CUÁNTOS RETOS TENÍAN LA FECHA DE FIN ANTES QUE LA DE INICIO (DATO PARA EL BACKEND):
   - {texto_invertidas}
   - Importancia técnica para el Backend:
     Permitir fechas invertidas representa un fallo grave de lógica temporal:
     a) Provoca duraciones negativas o inconsistencias matemáticas en reportes y métricas SLA.
     b) Bloquea algoritmos de calendarización y disparadores automáticos de cierre de convocatorias.
     c) El Backend debe implementar validadores de esquema estrictos (por ejemplo, con 
        Pydantic validators `@model_validator` o restricciones CHECK en la base de datos tipo
        `CHECK (fecha_fin > fecha_inicio)`), rechazando inmediatamente cualquier carga con 
        fechas incoherentes antes de la persistencia.
""")
    print("=" * 75)


# =============================================================================
# EJECUCIÓN PRINCIPAL
# =============================================================================
def main():
    print("#" * 75)
    print("   GENERANDO REPORTE GRÁFICO DE RETOS (src/reporte_retos.py)")
    print("#" * 75)

    df = cargar_datos()
    print(f"[INFO] Datos limpios cargados: {len(df)} registros.")

    # 1. Preparar consultas base
    conteo = df["estado"].value_counts()
    por_mes = df.groupby(df["fecha_inicio"].dt.to_period("M"))["id"].count()

    # 2. Generar las tres gráficas
    print("\nGenerando visualizaciones...")
    generar_grafica_1_barras_estado(conteo)
    generar_grafica_2_linea_por_mes(por_mes)
    generar_grafica_3_histograma_duracion(df)

    # 3. Imprimir conclusiones
    imprimir_conclusiones(df, conteo, por_mes)


if __name__ == "__main__":
    main()

