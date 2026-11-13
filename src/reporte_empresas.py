"""
Módulo de Visualización y Generación de Reportes: Empresas.

Script: src/reporte_empresas.py
Lee el archivo limpio 'datos/limpios/empresa_limpio.csv', genera 3 gráficas analíticas
utilizando matplotlib y las guarda en formato PNG dentro del directorio 'reportes/'.
Finaliza imprimiendo por consola las conclusiones sobre la calidad y el comportamiento
de los datos de empresas.
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

# Asegurar la creación automática de la carpeta de reportes
os.makedirs("reportes", exist_ok=True)
CARPETA_REPORTES.mkdir(parents=True, exist_ok=True)


def obtener_ruta_limpia() -> Path:
    """Retorna la ruta del archivo limpio generado por la fase de limpieza."""
    ruta = CARPETA_DATOS / "empresa_limpio.csv"
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró {ruta}. Ejecuta primero: python main.py --limpiar")
    return ruta


def cargar_datos() -> pd.DataFrame:
    """Carga y prepara el DataFrame limpio de empresas."""
    ruta = obtener_ruta_limpia()
    try:
        df = pd.read_csv(ruta, sep=None, engine="python", encoding="utf-8-sig")
    except Exception:
        df = pd.read_csv(ruta, sep=";", encoding="utf-8-sig")

    if "activa" in df.columns and df["activa"].dtype != bool:
        df["activa"] = df["activa"].astype(str).str.upper().isin(["TRUE", "1", "SI"])

    return df


# =============================================================================
# GRÁFICA 1: Barras - Cantidad de Empresas por Sector
# =============================================================================
def generar_grafica_1_barras_sector(df: pd.DataFrame, por_sector: pd.Series) -> str:
    """Genera gráfica de barras con la distribución de empresas por sector."""
    ruta_guardado = CARPETA_REPORTES / "empresas_grafica_1.png"

    plt.figure(figsize=(8, 5))
    por_sector.plot(kind="bar", color="#2b5c8f", edgecolor="black")

    plt.title("Cantidad de Empresas por Sector Económico", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Sector Económico", fontsize=11, fontweight="bold")
    plt.ylabel("Cantidad de Empresas", fontsize=11, fontweight="bold")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.savefig(ruta_guardado, dpi=120)
    plt.close()

    print(f"[OK] Gráfica 1 guardada en: {ruta_guardado}")
    return str(ruta_guardado)


# =============================================================================
# GRÁFICA 2: Torta - Empresas Activas vs Inactivas
# =============================================================================
def generar_grafica_2_torta_activa(df: pd.DataFrame) -> str:
    """Genera gráfica de torta comparando el porcentaje de activas vs inactivas."""
    ruta_guardado = CARPETA_REPORTES / "empresas_grafica_2.png"

    plt.figure(figsize=(7, 6))
    conteo_activa = df["activa"].value_counts()
    
    # Etiquetas semánticas para la visualización
    etiquetas = [
        f"Inactivas (False)" if not val else f"Activas (True)"
        for val in conteo_activa.index
    ]

    conteo_activa.plot(
        kind="pie",
        labels=etiquetas,
        autopct="%1.1f%%",
        startangle=140,
        colors=["#e74c3c", "#2ecc71"],
        explode=(0.04, 0.04),
        shadow=True,
    )

    plt.title("Proporción de Empresas Activas vs Inactivas", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Distribución Global", fontsize=10)
    plt.ylabel("Porcentaje", fontsize=10)

    plt.tight_layout()
    plt.savefig(ruta_guardado, dpi=120)
    plt.close()

    print(f"[OK] Gráfica 2 guardada en: {ruta_guardado}")
    return str(ruta_guardado)


# =============================================================================
# GRÁFICA 3: Barras Apiladas - Activas e Inactivas por Sector
# =============================================================================
def generar_grafica_3_barras_apiladas(tabla: pd.DataFrame) -> str:
    """Genera gráfico de barras apiladas cruzando sector y estado de actividad."""
    ruta_guardado = CARPETA_REPORTES / "empresas_grafica_3.png"

    fig, ax = plt.subplots(figsize=(9, 6))
    tabla.plot(kind="bar", stacked=True, ax=ax, color=["#e74c3c", "#2ecc71"], edgecolor="black")

    plt.title("Empresas Activas e Inactivas por Sector Económico", fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Sector Económico", fontsize=11, fontweight="bold")
    plt.ylabel("Cantidad de Empresas", fontsize=11, fontweight="bold")
    plt.legend(["Inactivas (False)", "Activas (True)"], title="Estado", loc="upper right")
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
def imprimir_conclusiones(df: pd.DataFrame, por_sector: pd.Series) -> None:
    """Imprime por consola las conclusiones derivadas de los datos."""
    total_empresas = len(df)
    inactivas = (df["activa"] == False).sum()
    pct_inactivas = (inactivas / total_empresas) * 100

    sector_lider = por_sector.index[0]
    cant_sector_lider = por_sector.iloc[0]
    siguientes = " y ".join(f"{s} ({c})" for s, c in por_sector.iloc[1:3].items())
    resumen_inactivas = (
        "Más de la mitad de las organizaciones" if pct_inactivas > 50 else "Una proporción relevante de las organizaciones"
    )

    # Correos inválidos (nulos o sin '@') medidos directamente en el dataset crudo
    ruta_crudo = CARPETA_CRUDOS / "empresa_crudo.csv"
    if ruta_crudo.exists():
        df_crudo = pd.read_csv(ruta_crudo, sep=";", encoding="utf-8-sig").drop_duplicates(subset=["id"])
        correo = df_crudo["correo"]
        correos_invalidos = int((correo.isna() | ~correo.astype(str).str.contains("@")).sum())
        pct_correos = correos_invalidos / len(df_crudo) * 100
        texto_correos = (
            f"En los datos crudos se detectaron {correos_invalidos} correos inválidos (sin arroba '@' o nulos),\n"
            f"     el {pct_correos:.1f}% de las {len(df_crudo)} empresas."
        )
    else:
        texto_correos = f"No se encontró {ruta_crudo.name}; no fue posible medir los correos inválidos."

    print("\n" + "=" * 75)
    print("                      CONCLUSIONES DEL ANÁLISIS")
    print("=" * 75)

    print(f"""
1. SECTOR CON MÁS EMPRESAS REGISTRADAS:
   - El sector líder es '{sector_lider}' con un total de {cant_sector_lider} empresas 
     registradas, seguido por {siguientes}. Este sector representa el motor de demanda
     principal en el ecosistema de la plataforma.

2. PORCENTAJE DE EMPRESAS INACTIVAS Y SU IMPACTO EN LA PLATAFORMA:
   - El {pct_inactivas:.1f}% de las empresas ({inactivas} de {total_empresas}) se encuentra actualmente 
     INACTIVO.
   - Impacto para la plataforma:
     {resumen_inactivas} en estado inactivo indica una fricción
     severa en el proceso de adopción (onboarding incompleto) o abandono temprano. Estas 
     empresas no pueden publicar retos ni interactuar comercialmente, lo que puede 
     distorsionar los KPIs de conversión y generar falsas expectativas a los proponentes. 
     Se requiere una estrategia de reactivación por correo y verificación de cuentas.

3. CORREOS ELECTRÓNICOS INVÁLIDOS Y LA IMPORTANCIA DE LA VALIDACIÓN EN EL BACKEND:
   - {texto_correos}
   - ¿Por qué es fundamental validarlos en el Backend?
     El Backend es la barrera definitiva de protección de la base de datos. Permitir correos 
     mal formados rompe canales críticos de comunicación (confirmación de retos, restablecimiento 
     de contraseñas, alertas de auditoría) y eleva la tasa de rebotes (bounces) afectando la 
     reputación de los servidores SMTP. Las validaciones mediante expresiones regulares (regex) 
     o esquemas de datos (como Pydantic) deben impedir que un registro corrupto toque el motor 
     de persistencia.
""")
    print("=" * 75)


# =============================================================================
# EJECUCIÓN PRINCIPAL
# =============================================================================
def main():
    print("#" * 75)
    print("   GENERANDO REPORTE GRÁFICO DE EMPRESAS (SCRIPT src/reporte_empresas.py)")
    print("#" * 75)

    df = cargar_datos()
    print(f"[INFO] Datos limpios cargados: {len(df)} registros.")

    # 1. Preparar consultas base
    por_sector = df.groupby("sector")["id"].count().sort_values(ascending=False)
    tabla_sector_activa = df.groupby(["sector", "activa"])["id"].count().unstack(fill_value=0)

    # 2. Generar las tres gráficas
    print("\nGenerando visualizaciones...")
    generar_grafica_1_barras_sector(df, por_sector)
    generar_grafica_2_torta_activa(df)
    generar_grafica_3_barras_apiladas(tabla_sector_activa)

    # 3. Imprimir conclusiones
    imprimir_conclusiones(df, por_sector)


if __name__ == "__main__":
    main()
