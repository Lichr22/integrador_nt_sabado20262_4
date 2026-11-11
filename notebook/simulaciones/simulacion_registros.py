'''
Simulación de la tabla 'registros' (participaciones/asignaciones en retos).
Genera datos sintéticos y aplica ensuciado de datos para análisis de calidad.
'''

import random
import uuid
import pandas as pd
from datetime import datetime
from faker import Faker

# 1. Sembrar semillas para los datos a simular
random.seed(42)
Faker.seed(42)

# 2. Identificar los datos a simular con su tipo de dato
# id (texto (UUID)), 
# fecha_registro (fecha), 
# observacion (texto), 
# estado (texto),
# id_usuario (texto (UUID)), 
# id_reto (texto (UUID))

# 3. Establecer una constante para el número de simulaciones
FILAS = 800
ESTADOS = ["Activo", "No Activo", "Bloqueado", "En revisión", "en_curso", "EN CURSO", "Cerrado"]
IDS_USUARIO = [str(uuid.uuid4()) for _ in range(5)]
IDS_RETO = [str(uuid.uuid4()) for _ in range(5)]
FALSITO = Faker("es_CO")


# 4. Funcion generadora
def generar_datos(numero_filas=FILAS):
    registros = []
    for _ in range(numero_filas):
        registros.append({
            "id": str(uuid.uuid4()),
            "fecha_registro": FALSITO.date_time_between(start_date="-1y", end_date="now"),
            "observacion": FALSITO.sentence(nb_words=10),
            "estado": random.choice(ESTADOS),
            "id_usuario": random.choice(IDS_USUARIO),
            "id_reto": random.choice(IDS_RETO),
        })
    return registros


# 7. Preparar la simulación para ensuciar los datos

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

    # 1. Observacion: 20% nulo
    filas_elegidas = obtener_muestra(datos_df, 0.20)
    datos_df.loc[filas_elegidas, "observacion"] = None

    # 2. Estado: 10% con errores de escritura
    filas_elegidas = obtener_muestra(datos_df, 0.10)
    datos_df.loc[filas_elegidas, "estado"] = datos_df.loc[filas_elegidas, "estado"].map(escribir_mal)

    # 3. Mezclar el formato de la fecha
    iso = datos_df["fecha_registro"].dt.strftime("%Y-%m-%d %H:%M:%S")
    latino = datos_df["fecha_registro"].dt.strftime("%d/%m/%Y %H:%M")
    datos_df["fecha_registro"] = iso
    filas_elegidas = obtener_muestra(datos_df, 0.25)
    datos_df.loc[filas_elegidas, "fecha_registro"] = latino.loc[filas_elegidas]

    # 4. Duplicación de combinaciones id_usuario e id_reto (10%)
    filas_elegidas = obtener_muestra(datos_df, 0.10)
    filas_origen = obtener_muestra(datos_df, 0.10)
    datos_df.loc[filas_elegidas, ["id_usuario", "id_reto"]] = datos_df.loc[filas_origen, ["id_usuario", "id_reto"]].values

    # 5. 5% de las filas repetidas tal cual (duplicados exactos)
    filas_elegidas = obtener_muestra(datos_df, 0.05)
    duplicados_exactos = datos_df.loc[filas_elegidas].copy()
    datos_df = pd.concat([datos_df, duplicados_exactos], ignore_index=True)

    return datos_df


def generar_registros(numero_filas=FILAS):
    """Genera DataFrame sucio de registros listo para exportar a crudos."""
    df_limpio = pd.DataFrame(generar_datos(numero_filas))
    df_sucio = ensuciar(df_limpio)
    return df_sucio


if __name__ == "__main__":
    df_limpio = pd.DataFrame(generar_datos(FILAS))
    print("--- REGISTROS LIMPIOS ---")
    print(df_limpio.head())

    df_sucio = ensuciar(df_limpio)
    print("\n--- REGISTROS SUCIOS ---")
    print(df_sucio.head())
    print("\nValores nulos:")
    print(df_sucio.isna().sum())
    print(f"\nForma del DataFrame: {df_sucio.shape}")

