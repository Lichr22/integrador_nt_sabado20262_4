import random
import uuid
import pandas as pd
from faker import Faker

#1. Sembrar Semillas para los datos a simular
random.seed(42)
Faker.seed(42)

#2. identificar los datos a similiar con su tipo de dato
# id (texto(UUID)),
# nombre (texto)****,
# correo (texto),
# contrasena_hash(texto),
# rol (texto)*****,
# activo(boolean),
# fecha(texto)***,

#3. Establecer una constante para el NUMERO DE SIMULACIONES
FILAS = 250
ROLES = ["administrador", "empresario", "estudiante", "profesor"]
FALSITO = Faker("es_CO")

#4. Funcion generadora
def generar_datos(numero_filas=FILAS):
    usuarios = []
    for _ in range(numero_filas):
        usuarios.append({
            "id": str(uuid.uuid4()),
            "nombre": FALSITO.name(),
            "correo": FALSITO.email(),
            "contrasena_hash": FALSITO.sha256(),
            "rol": random.choice(ROLES),
            "activo": random.choice([True, False]),
            "fecha_registro": FALSITO.date_time_between(start_date="-2y", end_date="now"),
        })
    return usuarios

#7 Preparar simulacion para ensuciar datos

#7.1 funcion para obtener una muestra de los datos 
def obtener_muestra(datos, porcentaje):
    return datos.sample(frac=porcentaje, random_state=random.randint(0, 9999)).index

#7.2 funcion auxiliar para cambiar valores de un texto
def escribir_mal(texto):
    variantes = [texto.lower(), texto.title(), texto.capitalize(), f" {texto} ", "Andres"]
    return random.choice(variantes)

#7.3 funcion auxiliar para cambiar los booleanos
def convertir_booleano(valor):
    if valor:
        return random.choice(["SI", "1"])
    else:
        return random.choice(["NO", "0"])

#7.4 funcion principal para ensuciar los datos simulados
def ensuciar(datos_df):
    datos_df = datos_df.copy()

    # Nombre el 10% tenga espacios y el 8% este en mayuscula 
    filas_elegidas = obtener_muestra(datos_df, 0.1)
    datos_df.loc[filas_elegidas, "nombre"] = " " + datos_df.loc[filas_elegidas, "nombre"] + " "

    filas_elegidas = obtener_muestra(datos_df, 0.08)
    datos_df.loc[filas_elegidas, "nombre"] = datos_df.loc[filas_elegidas, "nombre"].str.upper()

    # correo el 5% de los datos esté sin arroba
    filas_elegidas = obtener_muestra(datos_df, 0.05)
    datos_df.loc[filas_elegidas, "correo"] = datos_df.loc[filas_elegidas, "correo"].str.replace("@", "")

    # correo el 4% de los correos no deberia tener ningun valor (None)
    filas_elegidas = obtener_muestra(datos_df, 0.04)
    datos_df.loc[filas_elegidas, "correo"] = None

    # Rol: Aplicar errores de escrituras (variantes)
    filas_elegidas = obtener_muestra(datos_df, 0.1)
    datos_df.loc[filas_elegidas, "rol"] = datos_df.loc[filas_elegidas, "rol"].map(escribir_mal)

    # Activo: en ocasiones llega SI, NO, 1, 0
    datos_df["activo"] = datos_df["activo"].astype(object)
    filas_elegidas = obtener_muestra(datos_df, 0.15)
    datos_df.loc[filas_elegidas, "activo"] = datos_df.loc[filas_elegidas, "activo"].map(convertir_booleano)

    # mezclar el formato de la fecha
    # ISO => 2026-10-03 YYYY-mm-dd HH:MM:SS
    # LATINO => d/m/y h:m
    iso = datos_df["fecha_registro"].dt.strftime("%Y-%m-%d %H:%M:%S")
    latino = datos_df["fecha_registro"].dt.strftime("%d/%m/%y %H:%M")
    datos_df["fecha_registro"] = iso
    filas_elegidas = obtener_muestra(datos_df, 0.25)
    datos_df.loc[filas_elegidas, "fecha_registro"] = latino.loc[filas_elegidas]

    return datos_df

def generar_usuarios(numero_filas=FILAS):
    """Genera directamente el DataFrame con datos sucios para el pipeline."""
    df_limpio = pd.DataFrame(generar_datos(numero_filas))
    df_sucio = ensuciar(df_limpio)
    return df_sucio

#6. probar la funcion
if __name__ == "__main__":
    df_limpio = pd.DataFrame(generar_datos(FILAS))
    print("--- 5 PRIMEROS REGISTROS LIMPIOS ---")
    print(df_limpio.head())

    df_sucio = ensuciar(df_limpio)
    print("\n--- 5 PRIMEROS REGISTROS SUCIOS ---")
    print(df_sucio.head())

    print("\n--- VALORES NULOS ---")
    print(df_sucio.isna().sum())

