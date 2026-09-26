import random
import uuid
import pandas as pd
from faker import Faker

#1. Sembrar Semillas para los datos a simular
random.seed(42)
Faker.seed(42)

FILAS=200
NIVELES={"bajo": 1,    "medio": 2,    "alto": 3}
DIAS={1: 5,  2: 3, 3: 1}

#2. identificar los datos a similiar con su tipo de dato
#id (texto (UUID)), 
#nombre (texto), 
#nivel (entero), 
#dias_max_respuesta (entero).


def generar_datos(numero_filas=200):
    prioridades=[]
    for _ in range(numero_filas):
        prioridades.append({
            "id":str(uuid.uuid4()),
            "nombre":random.choice(list(NIVELES.keys())),
            "nivel":'NIVELES[nombre]',
            "dias_max_respuesta":'DIAS[nivel]',
        })
    return prioridades

tabla_ordenada_prioridades=pd.DataFrame(generar_datos())

print(tabla_ordenada_prioridades) 
    