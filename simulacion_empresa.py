'''Organizacion que registra o propone retos. Crea el script `src/simular_empresas.py`. Con la libreria **Faker** genera 300 filas falsas de la tabla `empresas`, con las MISMAS columnas que usa Backend II. Despues **ensucia los datos a proposito**: nulos, duplicados, espacios sobrantes, mayusculas mezcladas y formatos distintos. Esos errores son los que vas a arreglar en la etapa de limpieza, asi que tienen que quedar bien puestos.

Usa `Faker("es_CO")` y fija la semilla con `Faker.seed(42)` y `random.seed(42)` para que el resultado sea SIEMPRE el mismo y tu compañero pueda reproducirlo.'''

import random
import uuid
import pandas as pd
from faker import Faker

#1. Sembrar Semillas para los datos a simular
random.seed(42)
Faker.seed(42)

#2. identificar los datos a similiar con su tipo de dato
#id (texto (UUID)),
#nombre (texto),
#nit (texto),
#sector (texto)***********,
#contacto (texto),
#correo (texto),
#telefono (texto),
#activa (booleano).

#3 establecer una constante para el numero de simulaciones
FILAS=300
SECTORES=["Comunicaciones","Retail","Logistica","Agro","Alimentos","Tecnologia"]
FAKE= Faker("es_CO")

#funcion generadora
def generar_datos(numero_filas=300):
    empresas=[]
    for _ in range(numero_filas):
        empresas.append({
            "id": str(uuid.uuid4()),
            "nombre": FAKE.company(),
            "nit":FAKE.numerify("########-#"),
            "sector": random.choice(SECTORES),
            "contacto":FAKE.name(),
            "correo":FAKE.company_email(),
            "telefono":FAKE.numerify("3#########"),
            "activo":random.choice([True,False]),
            
        })

    return empresas

tabla_ordenada_empresa=pd.DataFrame(generar_datos())

print(tabla_ordenada_empresa) 
