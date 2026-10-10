'''

Clasifica tematicamente los retos. Crea el script `src/simular_categorias.py`. Con la libreria **Faker** genera 250 filas falsas de la tabla `categorias`, con las MISMAS columnas que usa Backend II. Despues **ensucia los datos a proposito**: nulos, duplicados, espacios sobrantes, mayusculas mezcladas y formatos distintos. Esos errores son los que vas a arreglar en la etapa de limpieza, asi que tienen que quedar bien puestos.

Usa `Faker("es_CO")` y fija la semilla con `Faker.seed(42)` y `random.seed(42)` para que el resultado sea SIEMPRE el mismo y tu compañero pueda reproducirlo.

OJO: `area_responsable` NO esta en el modelo de Backend II: es una columna EXTRA solo para este ejercicio de analisis, para poder agrupar. Dejala anotada como tal en el script.

'''
import random
import uuid
import pandas as pd
from faker import Faker

#1. Sembrar semillas para los datos a simular
random.seed(42)

#2. Identificar los datos a simular con su tipo de dato
#id (texto (UUID)),
# nombre (texto),
# descripcion (texto),
# area_responsable (texto)

#3 Establecer una constante para EL NUMERO DE SIMULACIONES
FILAS=250
CATEGORIAS=[]
AREAS=["Marketing", "Ventas", "Desarrollo", "Soporte"]
FALSITO = Faker("es_CO")


#4. Funcion generadora
def generar_datos(numero_filas=250):
    categorias=[]
    for _ in range(numero_filas):
        categorias.append({
            "id":str(uuid.uuid4()),
            "nombre":FALSITO.name(),
            "descripcion":FALSITO.sentence(nb_words=8),
            "area_responsable":random.choice(AREAS),
        })
    return categorias

#5. Convirtiendo los datos generados en un dataframe con PANDAS
tabla_ordenada_categorias=pd.DataFrame(generar_datos())

#6. Probar la funcion
print(tabla_ordenada_categorias)

#7. Preparar la simulación para ensuciar mis datos

#7.1 Funcion para obtener una muestra de los datos
def obtener_muestra(datos, porcentaje):
    return datos.sample(fraccion=porcentaje,random_state=random.randint(0, 9999)).index

#7.2 Funcion auxiliar para cambiar valores de un texto
def escribir_mal(texto):
    variantes=[texto.lower(),texto.title(),texto.capitalize(),f" {texto} ", "Juan Jose"]
    return random.choice(variantes)

#7.3 Funcion auxilixar para cambiar los booleanos
def covertir_booleanos(valor):
    if valor:
        return random.choice(["SI", "1"])
    else: 
        return random.choice(["NO", "0"])

#7.4 Funcion principal para ensuciar los datos simulados
def ensuciar_datos(datos_df):
    datos_df=datos_df.copy()

    filas_elegidas = obtener_muestra(datos_df, 0.4) 
    datos_df.loc[filas_elegidas, "nombre"] = datos_df.loc[filas_elegidas, "nombre"].apply(escribir_mal)

    filas_elegidas = obtener_muestra(datos_df, 0.15)
    datos_df.loc[filas_elegidas, "descripcion"] = None

    filas_elegidas = obtener_muestra(datos_df, 0.10)
    datos_df.loc[filas_elegidas, "area_responsable"] = None