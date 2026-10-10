'''Organizacion que registra o propone retos. Crea el script `src/simular_empresas.py`. Con la libreria **Faker** genera 300 filas falsas de la tabla `empresas`, con las MISMAS columnas que usa Backend II. Despues **ensucia los datos a proposito**: nulos, duplicados, espacios sobrantes, mayusculas mezcladas y formatos distintos. Esos errores son los que vas a arreglar en la etapa de limpieza, asi que tienen que quedar bien puestos.

Usa `Faker("es_CO")` y fija la semilla con `Faker.seed(42)` y `random.seed(42)` para que el resultado sea SIEMPRE el mismo y tu compañero pueda reproducirlo.'''

import random
import uuid
import pandas as pd
from faker import Faker

# 1. Sembrar Semillas para los datos a simular
random.seed(42)
Faker.seed(42)

# 2. identificar los datos a similiar con su tipo de dato
# id (texto (UUID)),
# nombre (texto),
# nit (texto),
# sector (texto)***********,
# contacto (texto),
# correo (texto),
# telefono (texto),
# activa (booleano).

# 3. Establecer una constante para el NUMERO DE SIMULACIONES
FILAS = 300
SECTORES = ["Comunicaciones", "Retail", "Logistica", "Agro", "Alimentos", "Tecnologia"]
FAKE = Faker("es_CO")

# 7 Preparar simulacion para ensuciar datos

# 7.1 funcion para obtener una muestra de los datos
def obtener_muestra(datos, porcentaje):
    return datos.sample(frac=porcentaje, random_state=random.randint(0, 9999)).index

# 7.2 funcion auxiliar para cambiar valores de un texto
def escribir_mal(texto):
    variantes=[texto.lower(),texto.title(), texto.capitalize(), f" {texto} ", "Andres"]
    return random.choice(variantes)

# 7.3 funcion auxiliar para cambiar los booleanos
def convertir_booleano(valor):
    if valor:
        return random.choice(["SI", "1"])
    else:
        return random.choice(["No", "0"])

# 7.4 funcion principal para ensuciar los datos simulados
def ensuciar(datos_df):
    datos_df = datos_df.copy()

    # Nombre: 10% espacios sobrantes, 15% MAYUSCULAS
    filas_espacios = obtener_muestra(datos_df, 0.10)
    datos_df.loc[filas_espacios, "nombre"] = " " + datos_df.loc[filas_espacios, "nombre"] + " "
    
    filas_mayus = obtener_muestra(datos_df, 0.15)
    datos_df.loc[filas_mayus, "nombre"] = datos_df.loc[filas_mayus, "nombre"].str.upper()

    # NIT: mitad con formato 900.123.456-7 y mitad sin nada (9001234567)
    datos_df["nit"] = datos_df["nit"].str.replace(r'[^0-9]', '', regex=True)
    filas_nit_formato = obtener_muestra(datos_df, 0.50)
    
    def formatear_nit(nit):
        if pd.isna(nit): return nit
        nit = str(nit)
        if len(nit) >= 10:
            return f"{nit[:3]}.{nit[3:6]}.{nit[6:9]}-{nit[9]}"
        return nit
        
    datos_df.loc[filas_nit_formato, "nit"] = datos_df.loc[filas_nit_formato, "nit"].apply(formatear_nit)

    # Sector: variantes del mismo sector
    filas_sector = obtener_muestra(datos_df, 0.20)
    def variar_sector(sector):
        if pd.isna(sector): return sector
        variantes = [sector, sector.upper(), f" {sector.lower()} "]
        return random.choice(variantes)
    datos_df.loc[filas_sector, "sector"] = datos_df.loc[filas_sector, "sector"].apply(variar_sector)

    # Contacto: 8% en None (nulos)
    filas_contacto = obtener_muestra(datos_df, 0.08)
    datos_df.loc[filas_contacto, "contacto"] = None

    # Correo: 6% sin arroba
    filas_correo = obtener_muestra(datos_df, 0.06)
    datos_df.loc[filas_correo, "correo"] = datos_df.loc[filas_correo, "correo"].str.replace("@", "")

    # Telefono: 3 formatos mezclados ('3001234567', '300 123 4567', '+57 300-123-4567')
    def formatear_telefono(tel):
        if pd.isna(tel): return tel
        tel = str(tel)
        formatos = [tel, f"{tel[:3]} {tel[3:6]} {tel[6:]}", f"+57 {tel[:3]}-{tel[3:6]}-{tel[6:]}"]
        return random.choice(formatos)
    datos_df["telefono"] = datos_df["telefono"].apply(formatear_telefono)

    # Activa: a veces como texto
    datos_df["activa"] = datos_df["activa"].astype(object)
    filas_activa = obtener_muestra(datos_df, 0.20)
    datos_df.loc[filas_activa, "activa"] = datos_df.loc[filas_activa, "activa"].map(convertir_booleano)

    # 3% NIT repetidos entre empresas distintas
    filas_nit_dup = obtener_muestra(datos_df, 0.03)
    if len(filas_nit_dup) > 0:
        nit_al_azar = random.choice(datos_df["nit"].dropna().tolist())
        datos_df.loc[filas_nit_dup, "nit"] = nit_al_azar

    # 5% de filas repetidas tal cual (duplicados exactos)
    num_duplicados = int(len(datos_df) * 0.05)
    filas_duplicadas = datos_df.sample(n=num_duplicados, random_state=random.randint(0, 9999))
    datos_df = pd.concat([datos_df, filas_duplicadas], ignore_index=True)

    return datos_df

# 4. Funcion generadora
def generar_empresas(n=300):
    empresas = []
    for _ in range(n):
        empresas.append({
            "id": str(uuid.uuid4()),
            "nombre": FAKE.company(),
            "nit": FAKE.numerify("##########"), # Base de 10 numeros
            "sector": random.choice(SECTORES),
            "contacto": FAKE.name(),
            "correo": FAKE.company_email(),
            "telefono": FAKE.numerify("3#########"),
            "activa": random.choice([True, False]),
        })

    # 5. Conviertiendo los datos generados en un dataframe con pandas 
    df_limpio = pd.DataFrame(empresas)
    df_sucio = ensuciar(df_limpio)
    
    return df_sucio

# 6. probar la funcion
if __name__ == "__main__":
    df = generar_empresas(FILAS)
    print("--- FORMA DEL DATAFRAME ---")
    print(df.shape)
    
    print("\n--- PRIMEROS REGISTROS ---")
    print(df.head())
    
    print("\n--- VALORES NULOS POR COLUMNA ---")
    print(df.isna().sum())
