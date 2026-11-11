'''
El elemento central: la necesidad que publica la empresa.
Genera datos sintéticos de la tabla 'retos' y aplica ensuciado intencional.
'''

import random
import uuid
import pandas as pd
from datetime import datetime, timedelta
from faker import Faker

# 1. Sembrar semillas para los datos a simular
random.seed(42)
Faker.seed(42)

# 2. Identificar los datos a simular con su tipo de dato
# id (texto (UUID)), 
# nombre (texto), 
# descripcion (texto), 
# fecha_inicio (fecha), 
# fecha_fin (fecha), 
# estado (texto),
# id_empresa (texto (UUID)), 
# id_categoria (texto (UUID)), 
# id_prioridad (texto (UUID)).

# 3. Establecer una constante para el número de simulaciones
FILAS = 500
ESTADOS = ["Activo", "No Activo", "Bloqueado", "En revisión", "en_curso", "EN CURSO", "Cerrado"]
IDS_EMPRESA = [str(uuid.uuid4()) for _ in range(5)]
IDS_CATEGORIA = [str(uuid.uuid4()) for _ in range(5)]
IDS_PRIORIDAD = [str(uuid.uuid4()) for _ in range(5)]
FALSITO = Faker("es_CO")


# 4. Funcion generadora
def generar_datos(numero_filas=FILAS):
    retos = []
    for _ in range(numero_filas):
        fecha_ini = FALSITO.date_time_between(start_date="-1y", end_date="+3m")
        retos.append({
            "id": str(uuid.uuid4()),
            "nombre": FALSITO.sentence(nb_words=6).rstrip("."),
            "descripcion": FALSITO.sentence(nb_words=12),
            "fecha_inicio": fecha_ini,
            "fecha_fin": fecha_ini + timedelta(days=random.randint(15, 180)),
            "estado": random.choice(ESTADOS),
            "id_empresa": random.choice(IDS_EMPRESA),
            "id_categoria": random.choice(IDS_CATEGORIA),
            "id_prioridad": random.choice(IDS_PRIORIDAD),
        })
    return retos


# 7. Preparar la simulacion para ensuciar datos

# 7.1 Funcion para obtener una muestra de los datos
def obtener_muestra(datos, porcentaje):
    return datos.sample(frac=porcentaje, random_state=random.randint(0, 9999)).index


# 7.2 Función auxiliar para cambiar valores de un texto
def escribir_mal(texto):
    if pd.isna(texto):
        return texto
    variantes = [texto.lower(), texto.title(), texto.capitalize(), f" {texto} ", "JuanJo"]
    return random.choice(variantes)


# 7.3 Funcion auxiliar para cambiar los booleanos
def convertir_booleano(valor):
    if valor:
        return random.choice(["SI", "1"])
    else:
        return random.choice(["NO", "0"])


# 7.4 Funcion principal para ensuciar los datos simulados
def ensuciar(datos_df):
    datos_df = datos_df.copy()

    # 5% de las filas repetidas tal cual (duplicados exactos)
    filas_elegidas = obtener_muestra(datos_df, 0.05)
    duplicados_exactos = datos_df.loc[filas_elegidas].copy()
    datos_df = pd.concat([datos_df, duplicados_exactos], ignore_index=True)

    # Nombre: 10% con espacios sobrantes
    filas_elegidas = obtener_muestra(datos_df, 0.10)
    datos_df.loc[filas_elegidas, "nombre"] = "  " + datos_df.loc[filas_elegidas, "nombre"] + "  "

    # Descripcion: 12% en None (nulos)
    filas_elegidas = obtener_muestra(datos_df, 0.12)
    datos_df.loc[filas_elegidas, "descripcion"] = None

    # Fecha_inicio: dos formatos mezclados ("2026-03-02" y "02/03/2026")
    iso_fi = datos_df["fecha_inicio"].dt.strftime("%Y-%m-%d")
    latino_fi = datos_df["fecha_inicio"].dt.strftime("%d/%m/%Y")
    datos_df["fecha_inicio"] = iso_fi
    filas_elegidas = obtener_muestra(datos_df, 0.50)  # 50% de cada formato para mezclar
    datos_df.loc[filas_elegidas, "fecha_inicio"] = latino_fi.loc[filas_elegidas]

    # Fecha_fin: 8% en None y 5% ANTERIOR a fecha_inicio (error lógico)
    filas_elegidas = obtener_muestra(datos_df, 0.08)
    datos_df.loc[filas_elegidas, "fecha_fin"] = None

    filas_elegidas = obtener_muestra(datos_df, 0.05)
    fechas_dt = pd.to_datetime(
        datos_df.loc[filas_elegidas, "fecha_inicio"],
        format="mixed",
        dayfirst=True,
        errors="coerce",
    )
    datos_df.loc[filas_elegidas, "fecha_fin"] = (fechas_dt - pd.Timedelta(days=5)).dt.strftime("%Y-%m-%d")

    # Estado: 10% con errores de escritura
    filas_elegidas = obtener_muestra(datos_df, 0.10)
    datos_df.loc[filas_elegidas, "estado"] = datos_df.loc[filas_elegidas, "estado"].map(escribir_mal)

    return datos_df


def generar_retos(numero_filas=FILAS):
    """Genera DataFrame sucio de retos listo para exportar a crudos."""
    df_limpio = pd.DataFrame(generar_datos(numero_filas))
    df_sucio = ensuciar(df_limpio)
    return df_sucio


if __name__ == "__main__":
    df_limpio = pd.DataFrame(generar_datos(FILAS))
    print("--- RETOS LIMPIOS ---")
    print(df_limpio.head())

    df_sucio = ensuciar(df_limpio)
    print("\n--- RETOS SUCIOS ---")
    print(df_sucio.head())
    print("\nValores nulos:")
    print(df_sucio.isna().sum())
    print(f"\nForma del DataFrame: {df_sucio.shape}")
