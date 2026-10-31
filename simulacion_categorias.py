'''
Clasifica tematicamente los retos. Crea el script `src/simular_categorias.py`. Con la libreria **Faker** genera 250 filas falsas de la tabla `categorias`, con las MISMAS columnas que usa Backend II. Despues **ensucia los datos a proposito**: nulos, duplicados, espacios sobrantes, mayusculas mezcladas y formatos distintos. Esos errores son los que vas a arreglar en la etapa de limpieza, asi que tienen que quedar bien puestos.

Usa `Faker("es_CO")` y fija la semilla con `Faker.seed(42)` y `random.seed(42)` para que el resultado sea SIEMPRE el mismo y tu compañero pueda reproducirlo.

OJO: `area_responsable` NO esta en el modelo de Backend II: es una columna EXTRA solo para este ejercicio de analisis, para poder agrupar. Dejala anotada como tal en el script.
'''

import random
import uuid
import pandas as pd
from faker import Faker

# 1. Sembrar semillas para los datos a simular
random.seed(42)
Faker.seed(42)

# 2. Identificar los datos a simular con su tipo de dato
# id (texto (UUID)),
# nombre (texto),
# descripcion (texto),
# area_responsable (texto) [COLUMNA EXTRA PARA ANALISIS]

# 3. Establecer una constante para EL NUMERO DE SIMULACIONES
FILAS = 250
AREAS = ["Marketing", "Ventas", "Desarrollo", "Soporte", "Innovacion", "Operaciones"]
NOMBRES_CATEGORIAS = [
    "Tecnologia e Innovacion",
    "Sostenibilidad Ambiental",
    "Transformacion Digital",
    "Optimizacion de Procesos",
    "Inteligencia Artificial",
    "Experiencia del Cliente",
    "Ciberseguridad",
    "Comercio Electronico",
    "Logistica y Operaciones",
    "Finanzas y Fintech",
    "Gestion del Talento Humano",
    "Marketing Digital",
]
FALSITO = Faker("es_CO")


# 4. Funcion generadora
def generar_datos(numero_filas=FILAS):
    categorias = []
    for _ in range(numero_filas):
        categorias.append({
            "id": str(uuid.uuid4()),
            "nombre": random.choice(NOMBRES_CATEGORIAS),
            "descripcion": FALSITO.sentence(nb_words=10),
            "area_responsable": random.choice(AREAS),
        })
    return categorias


# 7. Preparar la simulacion para ensuciar mis datos

# 7.1 Funcion para obtener una muestra de los datos
def obtener_muestra(datos, porcentaje):
    return datos.sample(frac=porcentaje, random_state=random.randint(0, 9999)).index


# 7.2 Funcion auxiliar para cambiar valores de un texto
def escribir_mal(texto):
    if pd.isna(texto):
        return texto
    txt = str(texto)
    variantes = [txt.lower(), txt.title(), txt.upper(), f"  {txt}  ", f" {txt.lower()} "]
    return random.choice(variantes)


# 7.4 Funcion principal para ensuciar los datos simulados
def ensuciar(datos_df):
    datos_df = datos_df.copy()

    # 1. Nombre: 25% con errores de escritura (casing y espacios)
    filas_nombre = obtener_muestra(datos_df, 0.25)
    datos_df.loc[filas_nombre, "nombre"] = datos_df.loc[filas_nombre, "nombre"].apply(escribir_mal)

    # 2. Descripcion: 15% en None (nulos)
    filas_desc = obtener_muestra(datos_df, 0.15)
    datos_df.loc[filas_desc, "descripcion"] = None

    # 3. Area Responsable: 10% en None (nulos) y 15% con espacios/casing
    filas_area_nula = obtener_muestra(datos_df, 0.10)
    datos_df.loc[filas_area_nula, "area_responsable"] = None

    filas_area_mal = obtener_muestra(datos_df, 0.15)
    datos_df.loc[filas_area_mal, "area_responsable"] = datos_df.loc[filas_area_mal, "area_responsable"].apply(escribir_mal)

    # 4. 5% de duplicados exactos
    num_duplicados = int(len(datos_df) * 0.05)
    filas_duplicadas = datos_df.sample(n=num_duplicados, random_state=random.randint(0, 9999))
    datos_df = pd.concat([datos_df, filas_duplicadas], ignore_index=True)

    return datos_df


def generar_categorias(numero_filas=FILAS):
    """Genera DataFrame sucio de categorias listo para exportar a crudos."""
    df_limpio = pd.DataFrame(generar_datos(numero_filas))
    df_sucio = ensuciar(df_limpio)
    return df_sucio


if __name__ == "__main__":
    df = generar_categorias(FILAS)
    print("--- FORMA DEL DATAFRAME ---")
    print(df.shape)
    print("\n--- PRIMEROS REGISTROS ---")
    print(df.head())
    print("\n--- VALORES NULOS ---")
    print(df.isna().sum())
