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