'''
El elemento central: la necesidad que publica la empresa. Crea el script `src/simular_retos.py`. 
Con la libreria **Faker** genera 500 filas falsas de la tabla `retos`, con las MISMAS columnas que usa Backend II.
Despues **ensucia los datos a proposito**: nulos, duplicados, espacios sobrantes, mayusculas mezcladas y formatos 
distintos. Esos errores son los que vas a arreglar en la etapa de limpieza, asi que tienen que quedar bien puestos.

Usa `Faker("es_CO")` y fija la semilla con `Faker.seed(42)` y `random.seed(42)` para que el resultado sea SIEMPRE el
mismo y tu compañero pueda reproducirlo.
'''

import random
import uuid
import pandas as pd
from datetime import datetime, timedelta
from faker import Faker


#1. Sembrar semillas para los datos a simular
random.seed(42)
Faker.seed(42)

#2. Identificar los datos a simular con su tipo de dato
'''
 id (texto (UUID)), 
 fecha_registro (fecha), 
 observacion (texto), 
 estado (texto),
id_usuario (texto (UUID)), 
id_reto (texto (UUID))
'''

#3. Establecer una constante para el número de simulaciones
FILAS=800
ESTADOS=["Activo","No Activo","Bloqueado","En revisión","en_curso","EN CURSO","Cerrado"]
IDS_USUARIO=[321,123,456,654,789]
IDS_RETO=[1,2,3,4,5]
falsito=Faker("es_CO")
fecha_inicio=falsito.date_time_between(start_date="-1y", end_date="+3m")

#4. Funcion generadora
def generar_datos(numero_filas=800):
    registros=[]
    for _ in range(numero_filas):
        registros.append({
            "id":str(uuid.uuid4()),
            "fecha_registro":falsito.date_time_between(start_date="-1y", end_date="now"),
            "observacion":falsito.sentence(nb_words=10),
            "estado":random.choice(ESTADOS),
            "id_empresa":random.choice(IDS_USUARIO),
            "id_categoria":random.choice(IDS_RETO)
            })
    return registros

#5. Convirtiendo los datos generados en un dataFrame con PANDAS
tabla_ordenada_registros=pd.DataFrame(generar_datos())

#Probar la funcionón
print(tabla_ordenada_registros)